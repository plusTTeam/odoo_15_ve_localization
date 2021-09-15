# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class Retention(models.Model):
    _name = "retention"
    _description = "Retention"
    _rec_name = "complete_name_with_code"

    @api.model
    def _get_default_journal(self):
        """ Get the default journal.
        It could either be passed through the context using the 'default_journal_id' key containing its id,
        either be determined by the default type.
        """
        move_type = self._context.get("default_move_type", "entry")
        if move_type in self.get_sale_types(include_receipts=True):
            journal_types = ["sale"]
        elif move_type in self.get_purchase_types(include_receipts=True):
            journal_types = ["purchase"]
        else:
            journal_types = self._context.get("default_move_journal_types", ["general"])

        if self._context.get("default_journal_id"):
            journal = self.env["account.journal"].browse(self._context["default_journal_id"])

            if move_type != "entry" and journal.type not in journal_types:
                raise ValidationError(_(
                    "Cannot create an invoice of type %(move_type)s with a journal having %(journal_type)s as type.",
                    move_type=move_type,
                    journal_type=journal.type,
                ))
        else:
            journal = self._search_default_journal(journal_types)

        return journal

    today = fields.Date.today()
    complete_name_with_code = fields.Char(
        string="Complete Name with Code",
        compute="_compute_complete_name_with_code",
        store=True
    )
    move_type = fields.Selection(selection=[
        ("entry", "Journal Entry"),
        ("out_invoice", "Customer Invoice"),
        ("out_refund", "Customer Credit Note"),
        ("in_invoice", "Vendor Bill"),
        ("in_refund", "Vendor Credit Note"),
    ], string="Type", required=True, store=True, index=True, readonly=True, tracking=True,
        default="entry", change_default=True, related="invoice_number.move_type")

    # == Business fields ==
    code = fields.Char(string="Retention Number", default=_("New"), store=True)
    date = fields.Date(string="Date", required=True, default=fields.Date.context_today)
    receipt_date = fields.Date(string="Receipt Date", required=True, default=fields.Date.context_today)
    month_fiscal_period = fields.Char(string="Month", compute="_compute_month_fiscal_char", store=True, readonly=False)
    year_fiscal_period = fields.Char(string="Year", default=str(today.year))
    is_iva = fields.Boolean(string="Is IVA", default=False,
                            help="Check if the retention is a iva, otherwise it is islr")
    retention_type = fields.Selection(string="Retention Type",
                                      selection=[("iva", "IVA"), ("islr", "ISLR")],
                                      compute="_compute_retention_type", inverse="_write_retention_type", default="iva")
    destination_account_id = fields.Many2one(
        comodel_name="account.account",
        string="Destination Account",
        store=True, readonly=False,
        compute="_get_destination_account_id",
        check_company=True)
    state = fields.Selection(selection=[
        ("draft", "Draft"),
        ("posted", "Posted"),
        ("cancel", "Cancelled"),
    ], string="Status", required=True, readonly=True, copy=False, tracking=True,
        default="draft")
    # === partner fields ===
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 store=True, readonly=True,
                                 compute="_compute_company_id")
    partner_type = fields.Selection([
        ("customer", "Customer"),
        ("supplier", "Vendor"),
    ],string="partner type", default="supplier", tracking=True)
    partner_id = fields.Many2one("res.partner", string="Customer/Vendor", domain="[('parent_id','=', False)]",
                                 check_company=True)
    rif = fields.Char(string="RIF", related="partner_id.vat")
    vat_withholding_percentage = fields.Float(string="vat withholding percentage", store=True, readonly=False,
                                              related="partner_id.vat_withholding_percentage", required=True)
    # === invoice fields ===
    invoice_number = fields.Many2one("account.move", string="Invoice Number", required=True,
                                     domain="[('move_type', 'in', ('out_invoice', 'in_invoice', 'in_refund', "
                                            "'out_refund')), ('retention_state', '!=', 'with_retention_Both'),"
                                            "('state', '=', 'posted'),('partner_id', '=', partner_id )]")
    original_document_number = fields.Char(string="Original Document Number", related="invoice_number.document_number")                                        
    invoice_date = fields.Date(string="Invoice Date", required=True, related="invoice_number.date")
    type_document = fields.Char(string="Type Document", compute="_compute_type_document")
    control_number = fields.Char(string="Control Number", related="invoice_number.control_number")
    ref = fields.Char(string="Reference", related="invoice_number.ref")
    company_currency_id = fields.Many2one(related="invoice_number.company_currency_id", string="Company Currency",
                                          readonly=True, help="Utility field to express amount currency")
    amount_tax = fields.Monetary(string="Amount tax", related="invoice_number.amount_tax",
                                 currency_field="company_currency_id")
    amount_untaxed = fields.Monetary(string="Amount untaxed", related="invoice_number.amount_untaxed",
                                     currency_field="company_currency_id")
    amount_total = fields.Monetary(string="Amount total", related="invoice_number.amount_total",
                                   currency_field="company_currency_id")
    amount_base_taxed = fields.Monetary(string="Amount base taxed", related="invoice_number.amount_base_taxed",
                                        currency_field="company_currency_id")
    amount_retention = fields.Monetary(string="Amount Retention", compute="_compute_amount_retention",
                                    currency_field="company_currency_id")
    amount_base_untaxed = fields.Monetary(string="Amount base untaxed", compute="_compute_amount_base_untaxed",
                                       currency_field="company_currency_id")

    @api.depends(
        "vat_withholding_percentage",
        "amount_tax")
    def _compute_amount_retention(self):
        for retention in self:
            amount_retention = retention.amount_tax * retention.vat_withholding_percentage / 100
            retention.amount_retention = amount_retention

    @api.depends("amount_untaxed")
    def _compute_amount_base_untaxed(self):
        for retention in self:
            retention.amount_base_untaxed = retention.amount_untaxed - retention.amount_base_taxed

    @api.onchange("vat_withholding_percentage")
    def _onchange_value_withholding_percentage(self):
        for retention in self:
            retention.amount_retention = retention.amount_tax * retention.vat_withholding_percentage / 100

    @api.depends("date")
    def _compute_month_fiscal_char(self):
        for retention in self:
            month_char = str(retention.date.month)
            if len(month_char) == 1:
                month_char = "0" + str(retention.date.month)
            retention.month_fiscal_period = month_char

    @api.depends("is_iva")
    def _compute_retention_type(self):
        for partner in self:
            partner.retention_type = "iva" if partner.is_iva else "islr"

    def _write_retention_type(self):
        for partner in self:
            partner.is_iva = partner.retention_type == "iva"

    @api.model
    def _get_destination_account_id(self):
        get_param = self.env["ir.config_parameter"].sudo().get_param
        for retention in self:
            account = "l10n_ve_plusteam.iva_account_sale_id"
            if retention.partner_type == "customer":
                account = "l10n_ve_plusteam.iva_account_sale_id" if retention.is_iva else \
                    "l10n_ve_plusteam.islr_account_sale_id"
            elif retention.partner_type == "supplier":
                account = "l10n_ve_plusteam.iva_account_purchase_id" if retention.is_iva else \
                    "l10n_ve_plusteam.islr_account_purchase_id"
            retention.destination_account_id = int(get_param(account))

    @api.depends("partner_id")
    def _compute_company_id(self):
        for retention in self:
            retention.company_id = retention.partner_id.company_id or retention.company_id or self.env.company

    @api.depends("invoice_number")
    def _compute_type_document(self):
        for retention in self:
            if retention.invoice_number.move_type in ('out_invoice', 'in_invoice'):
                if retention.invoice_number.debit_origin_id:
                    retention.type_document = 'N/D'
                else:
                    retention.type_document = 'Factura'
            elif retention.invoice_number.move_type in ('in_refund', 'out_refund'):
                retention.type_document = 'N/C'
            else:
                retention.type_document = 'Otro'

    @api.model
    def create(self, values):
        if values.get("code", "").strip() in [_("New"), "", "Nuevo"]:
            values["code"] = self.env["ir.sequence"].next_by_code("retention.sequence")
        values["state"] = "posted"
        if values.get("retention_type", False) == "iva":
            retention_state = "with_retention_iva"
        else:
            retention_state = "with_retention_islr"
        invoice = self.env["account.move"].browse([values["invoice_number"]])
        if invoice.retention_state == "without_retention":
            invoice.write({
                "retention_state": retention_state
            })
        else:
            if invoice.retention_state == retention_state:
               raise ValidationError(_("This type was already generated"))

            invoice.write({
                "retention_state": "with_retention_Both"
            })

        return super(Retention, self).create(values)


    @api.depends("ref", "code")
    def _compute_complete_name_with_code(self):
        for retention in self:
            retention.complete_name_with_code = f"[{retention.code}] {retention.ref}"
