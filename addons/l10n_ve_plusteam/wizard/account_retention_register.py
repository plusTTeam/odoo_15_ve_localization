# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class AccountRetentionRegister(models.TransientModel):
    _name = "account.retention.register"
    _description = "Register Retention"

    retention_code = fields.Char(string="Retention Number", default=_("New"))
    retention_date = fields.Date(string="Date", required=True, default=fields.Date.context_today)
    invoice_date = fields.Date(string="Invoice Date", required=True, compute="_compute_data_invoice")
    month_fiscal_period = fields.Char(string="Month", store=True, readonly=False, required=True,
                                      default=fields.Date.today().strftime('%m'))
    year_fiscal_period = fields.Char(string="Year", default=fields.Date.today().year, required=True)
    is_iva = fields.Boolean(string="Is IVA", default=False,
                            help="Check if the retention is a iva, otherwise it is islr")
    retention_type = fields.Selection(string="Retention Type",
                                      selection=[("iva", "IVA"), ("islr", "ISLR")],
                                      compute="_compute_retention_type", inverse="_write_retention_type", default="iva")
    partner_id = fields.Many2one("res.partner", string="Name", domain="[('parent_id','=', False)]",
                                 check_company=True, compute="_compute_data_invoice", required=True)
    rif = fields.Char(string="RIF", related="partner_id.vat")
    vat_withholding_percentage = fields.Float(string="vat withholding percentage", store=True, readonly=False,
                                              related="partner_id.vat_withholding_percentage", required=True)
    invoice_id = fields.Many2one("account.move", string="Invoice", compute="_compute_data_invoice",
                                 domain="[('partner_id', '=', partner_id )]")
    currency_id = fields.Many2one("res.currency", string="Currency", store=True, readonly=True,
                                  help="The invoice's currency.", related="invoice_id.currency_id")
    company_id = fields.Char(string="Company", compute="_compute_data_invoice")
    move_type = fields.Char(string="Move Type", compute="_compute_data_invoice")
    original_document_number = fields.Char(string="Original Invoice Number", compute="_compute_data_invoice")
    document_type = fields.Char(string="Type Document", compute="_compute_type_document")
    document = fields.Char(string="Document Number", compute="_compute_data_invoice")
    amount_tax = fields.Monetary(string="Amount tax", currency_field="currency_id", compute="_compute_data_invoice")
    amount_total = fields.Monetary(string="Amount total", compute="_compute_data_invoice", currency_field="currency_id")
    amount_base_taxed = fields.Monetary(string="Amount base taxed", compute="_compute_data_invoice",
                                        currency_field="currency_id")
    amount_base_untaxed = fields.Monetary(string="Amount base untaxed", compute="_compute_data_invoice",
                                          currency_field="currency_id")
    amount_retention = fields.Float(string="Withholding Amount", compute="_compute_amount_retention")
    can_edit_wizard = fields.Boolean(store=True, copy=False, default=True,
                                     help="Technical field used to indicate the user can edit the wizard content such "
                                          "as the amount.")

    @api.depends("retention_date")
    def _compute_data_invoice(self):
        invoice = self.env["account.move"].browse(self._context.get("active_ids", []))
        for wizard in self:
            if invoice:
                wizard.document = invoice.document_number
                wizard.invoice_id = invoice.id
                wizard.amount_tax = invoice.amount_tax
                wizard.amount_base_taxed = invoice.amount_base_taxed
                wizard.amount_total = invoice.amount_total
                wizard.partner_id = invoice.partner_id
                wizard.amount_base_untaxed = invoice.amount_untaxed - invoice.amount_base_taxed
                wizard.invoice_date = invoice.date
                wizard.company_id = invoice.company_id.id
                wizard.move_type = invoice.move_type
                wizard.original_document_number = invoice.document_number
            else:
                wizard.document = _("Without relationship")

    @api.depends("vat_withholding_percentage", "amount_tax")
    def _compute_amount_retention(self):
        for retention in self:
            retention.amount_retention = retention.amount_tax * retention.vat_withholding_percentage / 100

    @api.depends("is_iva")
    def _compute_retention_type(self):
        for retention in self:
            retention.retention_type = "iva" if retention.is_iva else "islr"

    def _write_retention_type(self):
        for retention in self:
            retention.is_iva = retention.retention_type == "iva"

    @api.onchange("vat_withholding_percentage")
    def _onchange_value_withholding_percentage(self):
        for retention in self:
            retention.amount_retention = retention.amount_tax * retention.vat_withholding_percentage / 100

    @api.depends("invoice_id")
    def _compute_type_document(self):
        for retention in self:
            if retention.move_type in ("out_invoice", "in_invoice"):
                if retention.invoice_id.debit_origin_id:
                    retention.document_type = _("D/N")
                else:
                    retention.document_type = _("Invoice")
            elif retention.move_type in ("in_refund", "out_refund"):
                retention.document_type = _("C/N")
            else:
                retention.document_type = _("Other")

    def _create_retention_values_from_wizard(self):
        return {
            "retention_date": self.retention_date,
            "month_fiscal_period": self.month_fiscal_period,
            "year_fiscal_period": self.year_fiscal_period,
            "retention_type": self.retention_type,
            "is_iva": self.is_iva,
            "move_type": self.move_type,
            "document_type": self.document_type,
            "original_document_number": self.original_document_number,
            "retention_code": self.retention_code,
            "company_id": self.company_id,
            "partner_id": self.partner_id.id,
            "vat_withholding_percentage": self.vat_withholding_percentage,
            "invoice_id": self.invoice_id.id,
            "invoice_date": self.invoice_date,
            "amount_retention": self.amount_retention,
            "amount_base_untaxed": self.amount_base_untaxed
        }

    def _create_retentions(self):
        self.ensure_one()
        retention_values = self._create_retention_values_from_wizard()
        self.env["retention"].create(retention_values)

    def action_create_retention(self):
        self._create_retentions()
        return True
