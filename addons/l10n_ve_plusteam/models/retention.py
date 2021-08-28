# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Retention(models.Model):
    _name = "retention"

    receipt_number= fields.Char(string="Receipt Number")
    issue_date = fields.Date(string="Issue Date", required=True)
    deliver_date = fields.Date(string="Deliver Date", required=True)
    month_fiscal_period = fields.Integer(string="Month")
    year_fiscal_period = fields.Integer(string="Year")
     # === partner fields ===
    name = fields.Many2one("res.partner", string="Name")
    rif = fields.Char(string="RIF", related="name.vat")
    vat_withholding_percentage= fields.Float(string="vat_withholding_percentage", related="name.vat_withholding_percentage")
     # === invoice fields ===
    invoice_number = fields.Many2one("account.move", string="Invoice Number", domain="[('partner_id', '=', name )]")
    company_currency_id= fields.Many2one(related='invoice_number.company_currency_id', string='Company Currency',
        readonly=True, help='Utility field to express amount currency')
    amount_tax = fields.Monetary(string="Amount tax", related="invoice_number.amount_tax", currency_field='company_currency_id')
    amount_total = fields.Monetary(string="Amount total", related="invoice_number.amount_total", currency_field='company_currency_id')
    amount_base_taxed = fields.Monetary(string="Amount base taxed", related="invoice_number.amount_base_taxed", currency_field='company_currency_id')
   