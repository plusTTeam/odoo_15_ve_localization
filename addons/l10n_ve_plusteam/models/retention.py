# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Retention(models.Model):
    _name = "retention"

    receipt_number = fields.Char(string="Receipt Number")
    issue_date = fields.Date(string="Issue Date", required=True)
    deliver_date = fields.Date(string="Deliver Date", required=True)
    month_fiscal_period = fields.Integer(string="Month")
    year_fiscal_period = fields.Integer(string="Year")
    islr = fields.Boolean(string="ISLR",readonly=True)
    iva = fields.Boolean(string="IVA")
    # === account_id Contable ===
    iva_account_purchase_id = fields.Many2one(ACCOUNT_MODEL, string="VAT accounting account for suppliers")
    # === partner fields ===
    partner_id = fields.Many2one("res.partner", string="Name")
    rif = fields.Char(string="RIF", related="partner_id.vat")
    vat_withholding_percentage = fields.Float(string="vat withholding percentage",
                                              related="partner_id.vat_withholding_percentage")
    withholding_percentage = fields.Float(string="withholding percentage")
    # === invoice fields ===
    invoice_number = fields.Many2one("account.move", string="Invoice Number",
                                     domain="[('partner_id', '=', partner_id )]")
    company_currency_id = fields.Many2one(related='invoice_number.company_currency_id', string='Company Currency',
                                          readonly=True, help='Utility field to express amount currency')
    amount_tax = fields.Monetary(string="Amount tax", related="invoice_number.amount_tax",
                                 currency_field='company_currency_id')
    amount_total = fields.Monetary(string="Amount total", related="invoice_number.amount_total",
                                   currency_field='company_currency_id')
    amount_base_taxed = fields.Monetary(string="Amount base taxed", related="invoice_number.amount_base_taxed",
                                        currency_field='company_currency_id')
    amount_retetion = fields.Float(string="Amount Retention", compute='_compute_amount_retention')

    @api.depends(
        'vat_withholding_percentage',
        'amount_tax')
    def _compute_amount_retention(self):
        for retention in self:
            amount_retetion = retention.amount_tax * retention.vat_withholding_percentage / 100
            retention.amount_retetion = amount_retetion

    @api.onchange('amount_tax','vat_withholding_percentage')
    def _onchange_show_value_withholding(self):
        for retention in self:
           if self.amount_tax>0:
              retention.withholding_percentage = self.vat_withholding_percentage

    @api.onchange('withholding_percentage')
    def _onchange_value_withholding_percentage(self):
        for retention in self:
              retention.amount_retetion = retention.amount_tax * self.withholding_percentage / 100
