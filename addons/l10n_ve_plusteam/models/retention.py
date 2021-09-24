# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Retention(models.Model):
    _name = "retention"
    _description = "Retention"
    _inherits = {"account.move": "move_id"}
    _rec_name = "complete_name_with_code"

    complete_name_with_code = fields.Char(string="Complete Name with Code", compute="_compute_complete_name_with_code",
                                          store=True)
    move_type = fields.Selection(selection=[
        ("out_invoice", "Customer Invoice"),
        ("out_refund", "Customer Credit Note"),
        ("in_invoice", "Vendor Bill"),
        ("in_refund", "Vendor Credit Note"),
    ], string="Type", required=True, store=True, index=True, readonly=True, tracking=True,
        related="invoice_id.move_type")
    move_id = fields.Many2one(
        comodel_name="account.move", string="Journal Entry", required=True, readonly=True, ondelete="cascade",
        check_company=True)
    retention_code = fields.Char(string="Retention Number", default=_("New"), store=True)
    retention_date = fields.Date(string="Date", required=True, default=fields.Date.context_today)
    receipt_date = fields.Date(string="Receipt Date", required=True, default=fields.Date.context_today)
    month_fiscal_period = fields.Char(string="Month", store=True, readonly=False,
                                      default=fields.Date.today().strftime('%m'))
    year_fiscal_period = fields.Char(string="Year", default=fields.Date.today().year)
    is_iva = fields.Boolean(string="Is IVA", default=False,
                            help="Check if the retention is a iva, otherwise it is islr")
    retention_type = fields.Selection(string="Retention Type",
                                      selection=[("iva", "IVA"), ("islr", "ISLR")],
                                      compute="_compute_retention_type", inverse="_write_retention_type", default="iva")
    destination_account_id = fields.Many2one(comodel_name="account.account", string="Destination Account", store=True,
                                             readonly=False, check_company=True)
    state = fields.Selection(selection=[
        ("draft", "Draft"),
        ("posted", "Posted"),
        ("cancel", "Cancelled"),
    ], string="Status", required=True, readonly=True, copy=False, tracking=True,
        default="draft")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 store=True, readonly=True,
                                 compute="_compute_company_id")
    partner_type = fields.Selection([
        ("customer", "Customer"),
        ("supplier", "Vendor"),
    ], string="partner type", default="supplier", tracking=True)
    partner_id = fields.Many2one("res.partner", string="Customer/Vendor", domain="[('parent_id','=', False)]",
                                 check_company=True)
    rif = fields.Char(string="RIF", related="partner_id.vat")
    vat_withholding_percentage = fields.Float(string="vat withholding percentage", store=True, readonly=False,
                                              related="partner_id.vat_withholding_percentage", required=True)
    invoice_id = fields.Many2one("account.move", string="Invoice", required=True,
                                 domain="[('move_type', 'in', ('out_invoice', 'in_invoice', 'in_refund', "
                                            "'out_refund')), ('retention_state', '!=', 'with_both_retentions'),"
                                        "('state', '=', 'posted'),('partner_id', '=', partner_id )]")
    original_document_number = fields.Char(string="Original Document Number", related="invoice_id.document_number")
    invoice_date = fields.Date(string="Invoice Date", required=True, related="invoice_id.date")
    document_type = fields.Char(string="Document Type", compute="_compute_document_type")
    control_number = fields.Char(string="Control Number", related="invoice_id.control_number")
    ref = fields.Char(string="Reference", related="invoice_id.ref")
    company_currency_id = fields.Many2one(related="invoice_id.company_currency_id", string="Company Currency",
                                          readonly=True, help="Utility field to express amount currency")
    currency_id = fields.Many2one(related="invoice_id.currency_id", string="Currency", readonly=True,
                                  help="Invoice currency")
    amount_tax = fields.Monetary(string="Amount tax", related="invoice_id.amount_tax",
                                 currency_field="currency_id")
    amount_untaxed = fields.Monetary(string="Amount untaxed", related="invoice_id.amount_untaxed",
                                     currency_field="currency_id")
    amount_total = fields.Monetary(string="Amount total", related="invoice_id.amount_total",
                                   currency_field="currency_id")
    amount_base_taxed = fields.Monetary(string="Amount base taxed", related="invoice_id.amount_base_taxed",
                                        currency_field="currency_id")
    amount_retention = fields.Monetary(string="Withholding Amount", compute="_compute_amount_retention",
                                       currency_field="currency_id")
    amount_retention_company_currency = fields.Monetary(string="Withholding Amount in Company Currency",
                                                        compute="_compute_amount_retention",
                                                        currency_field="company_currency_id")
    amount_base_untaxed = fields.Monetary(string="Amount base untaxed", compute="_compute_amount_base_untaxed",
                                          currency_field="currency_id")

    @api.constrains("partner_id")
    def _check_partner_id(self):
        for record in self:
            if record.partner_id != record.invoice_id.partner_id:
                raise ValidationError(
                    _("The selected contact is different from the invoice contact, "
                      "they must be the same, please correct it")
                )

    @api.constrains("vat_withholding_percentage")
    def _check_vat_withholding_percentage(self):
        for record in self:
            if record.vat_withholding_percentage <= 0 or record.vat_withholding_percentage > 100:
                raise ValidationError(
                    _("The retention percentage must be between 1 and 100, "
                      "please verify that the value is in this range")
                )

    @api.constrains("retention_type")
    def _check_retention_type(self):
        retention_already_created = False
        retentions = self.read_group([("retention_type", "=", "iva")], ["invoice_id"], ["invoice_id"])
        for retention in retentions:
            if retention.get("invoice_id_count", 0) > 1:
                retention_already_created = True
        retentions = self.read_group([("retention_type", "=", "islr")], ["invoice_id"], ["invoice_id"])
        for retention in retentions:
            if retention.get("invoice_id_count", 0) > 1:
                retention_already_created = True
        if retention_already_created:
            raise ValidationError(_("This type was already generated"))

    @api.constrains("move_type")
    def _check_move_type(self):
        for retention in self:
            if retention.move_type not in ("out_invoice", "in_invoice", "in_refund", "out_refund"):
                raise ValidationError(
                    _("You are trying to create a withholding from an illegal journal entry type (%s)",
                      retention.invoice_id.move_type))

    @api.depends("vat_withholding_percentage", "amount_tax", "company_id", "currency_id", "retention_date")
    def _compute_amount_retention(self):
        for retention in self:
            retention.amount_retention = retention.amount_tax * retention.vat_withholding_percentage / 100
            retention.amount_retention_company_currency = retention.currency_id._convert(
                retention.amount_retention, retention.company_id.currency_id, retention.company_id,
                retention.retention_date)

    @api.depends("amount_untaxed")
    def _compute_amount_base_untaxed(self):
        for retention in self:
            retention.amount_base_untaxed = retention.amount_untaxed - retention.amount_base_taxed

    @api.onchange("vat_withholding_percentage")
    def _onchange_value_withholding_percentage(self):
        for retention in self:
            retention.amount_retention = retention.amount_tax * retention.vat_withholding_percentage / 100

    @api.depends("is_iva")
    def _compute_retention_type(self):
        for partner in self:
            partner.retention_type = "iva" if partner.is_iva else "islr"

    def _write_retention_type(self):
        for partner in self:
            partner.is_iva = partner.retention_type == "iva"

    def _get_destination_account_id(self):
        self.ensure_one()
        account = self.company_id.iva_account_sale_id
        if self.move_type in ("in_invoice", "in_refund") and self.is_iva:
            account = self.company_id.iva_account_purchase_id
        if not account:
            raise ValidationError(
                _("There is no configuration of withholding accounting accounts for this company, please go to "
                  "configurations and define the accounts to continue with the process."))
        return account.id

    @api.depends("partner_id")
    def _compute_company_id(self):
        for retention in self:
            retention.company_id = retention.partner_id.company_id or retention.company_id or self.env.company

    @api.depends("invoice_id")
    def _compute_document_type(self):
        for retention in self:
            if retention.invoice_id.move_type in ("out_invoice", "in_invoice"):
                if retention.invoice_id.debit_origin_id:
                    retention.document_type = _('D/N')
                else:
                    retention.document_type = _('Invoice')
            elif retention.invoice_id.move_type in ("in_refund", "out_refund"):
                retention.document_type = _('C/N')
            else:
                retention.document_type = _('Other')

    @api.model
    def create(self, values):
        if values.get("retention_code", "").strip().lower() in ["", "nuevo", "new"]:
            values["retention_code"] = self.env["ir.sequence"].next_by_code("retention.sequence")
        values["state"] = "posted"
        if values.get("retention_type", False) == "iva":
            retention_state = "with_retention_iva"
        else:
            retention_state = "with_retention_islr"
        invoice = self.env["account.move"].browse([values["invoice_id"]])
        if invoice.retention_state == "without_retention":
            invoice.write({
                "retention_state": retention_state
            })
        elif invoice.retention_state != retention_state and invoice.retention_state != "with_both_retentions":
            invoice.write({
                "retention_state": "with_both_retentions"
            })
        retention = super(Retention, self).create(values)
        retention.write({
            "destination_account_id": retention._get_destination_account_id()
        })
        retention.move_id.write(retention._update_move_id())
        to_write = {"line_ids": [(0, 0, line_values) for line_values in retention._prepare_move_lines()]}
        retention.move_id.write(to_write)
        return retention

    def _update_move_id(self):
        self.ensure_one()
        return {
            "journal_id": self._get_default_journal().id,
            "ref": _("%s withholding from %s invoice", self.retention_type, self.invoice_id.name),
            "date": self.retention_date,
            "move_type": "entry",
            "partner_id": self.partner_id.id,
            "state": "posted"
        }

    def _prepare_move_lines(self):
        self.ensure_one()
        default_line_name = self.retention_code
        # signed equals to 1 when self.move_type in ("in_invoice", "out_refund")
        signed = 1
        if self.move_type in ("out_invoice", "in_refund"):
            signed = -1
        counterpart_amount = signed * self.amount_retention
        balance = self.currency_id._convert(
            counterpart_amount, self.company_id.currency_id, self.company_id, self.retention_date)
        counterpart_account = self._get_counterpart_account()
        line_ids = [{
            "name": default_line_name,
            "date_maturity": self.retention_date,
            "amount_currency": -counterpart_amount,
            "currency_id": self.currency_id.id,
            "debit": balance < 0.0 and -balance or 0.0,
            "credit": balance > 0.0 and balance or 0.0,
            "partner_id": self.partner_id.id,
            "account_id": self.destination_account_id.id
        }, {
            "name": default_line_name,
            "date_maturity": self.retention_date,
            "amount_currency": counterpart_amount,
            "currency_id": self.currency_id.id,
            "debit": balance > 0.0 and balance or 0.0,
            "credit": balance < 0.0 and -balance or 0.0,
            "partner_id": self.partner_id.id,
            "account_id": counterpart_account.account_id.id
        }]
        return line_ids

    def _get_counterpart_account(self):
        self.ensure_one()
        lines = []
        for line in self.invoice_id.line_ids:
            if line.account_id.internal_type in ("receivable", "payable"):
                lines.append(line)
        return lines[0]

    @api.model
    def _get_default_journal(self):
        """ Get the default journal.
        It could either be passed through the context using the 'default_journal_id' key containing its id,
        either be determined by the default type.
        """
        if self._context.get("default_journal_id"):
            journal = self.env["account.journal"].browse(self._context["default_journal_id"])
        else:
            journal = self._search_company_journal()
        return journal

    @api.model
    def _search_company_journal(self):
        company_journal = self.env.company.withholding_journal_id
        if company_journal:
            return company_journal
        journal = self.env.ref("l10n_ve_plusteam.journal_withholding", raise_if_not_found=False)
        if journal and journal.active:
            return journal
        raise ValidationError(_("The company does not have a journal configured for withholding, please go to"
                                " the configuration section to add one"))

    @api.depends("original_document_number", "retention_code")
    def _compute_complete_name_with_code(self):
        for retention in self:
            retention.complete_name_with_code = f"[{retention.retention_code}] {retention.original_document_number}"

    def button_cancel(self):
        self.write({"state": "cancel"})
        self.move_id.button_draft()
        self.move_id.button_cancel()
