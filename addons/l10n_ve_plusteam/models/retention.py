# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools import float_compare, date_utils
from odoo.tools.misc import format_date



class Retention(models.Model):
    _name = "retention"
    
    today = fields.Date.today()

    # == Business fields ==
    code = fields.Char(string="Code", default=_("New"))
    issue_date = fields.Date(string="Issue Date", required=True, default = fields.Date.context_today)
    deliver_date = fields.Date(string="Deliver Date", required=True)
    month_fiscal_period = fields.Char(string="Month", compute ='_compute_month_fiscal_char', store=True, readonly=False)
    year_fiscal_period = fields.Char(string="Year", default = str(today.year))
    is_iva = fields.Boolean(string='Is IVA', default=False,
        help="Check if the contact is a company, otherwise it is a person")
    retention_type = fields.Selection(string='Retention Type',
        selection=[('Iva', 'IVA'), ('islr', 'ISLR')],
        compute='_compute_retention_type', inverse='_write_retention_type', default='Iva')
    destination_account_id = fields.Char(string='Destination Account', compute ='_compute_destination_account_id')  
    state = fields.Selection(selection=[
            ('draft', 'Draft'),
            ('posted', 'Posted'),
            ('cancel', 'Cancelled'),
        ], string='Status', required=True, readonly=True, copy=False, tracking=True,
        default='draft')
    # === partner fields ===
    company_id = fields.Many2one(comodel_name='res.company', string='Company',
                                 store=True, readonly=True,
                                 compute='_compute_company_id')
    partner_type = fields.Selection([
        ('customer', 'Customer'),
        ('supplier', 'Vendor'),
    ], default='supplier', tracking=True, required=True)
    partner_id = fields.Many2one("res.partner", string="Name",
                                     domain="[('supplier_rank', '=', 1 )]")
    rif = fields.Char(string="RIF", related="partner_id.vat")
    vat_withholding_percentage = fields.Float(string="vat withholding percentage", store=True, readonly=False,
                                              related="partner_id.vat_withholding_percentage")
    # === invoice fields ===
    invoice_number = fields.Many2one("account.move", string="Invoice Number",
                                     domain="[('state', '=', 'posted'),('partner_id', '=', partner_id )]")
    company_currency_id = fields.Many2one(related='invoice_number.company_currency_id', string='Company Currency',
                                          readonly=True, help='Utility field to express amount currency')
    amount_tax = fields.Monetary(string="Amount tax", related="invoice_number.amount_tax",
                                 currency_field='company_currency_id')
    amount_untaxed = fields.Monetary(string="Amount tax", related="invoice_number.amount_untaxed",
                                 currency_field='company_currency_id')
    amount_total = fields.Monetary(string="Amount total", related="invoice_number.amount_total",
                                   currency_field='company_currency_id')
    amount_base_taxed = fields.Monetary(string="Amount base taxed", related="invoice_number.amount_base_taxed",
                                        currency_field='company_currency_id')
    amount_retetion = fields.Float(string="Amount Retention", compute='_compute_amount_retention')
    amount_base_untaxed = fields.Float(string="Amount Retention", compute='_compute_amount_base_untaxed')

    @api.depends(
        'vat_withholding_percentage',
        'amount_tax')
    def _compute_amount_retention(self):
        for retention in self:
            amount_retetion = retention.amount_tax * retention.vat_withholding_percentage / 100
            retention.amount_retetion = amount_retetion

    @api.depends('amount_untaxed')
    def _compute_amount_base_untaxed(self):
        for retention in self:
            retention.amount_base_untaxed = retention.amount_untaxed-retention.amount_base_taxed

    @api.onchange('vat_withholding_percentage')
    def _onchange_value_withholding_percentage(self):
        for retention in self:
              retention.amount_retetion = retention.amount_tax * retention.vat_withholding_percentage / 100

    @api.depends('issue_date')
    def _compute_month_fiscal_char(self):
        for retention in self:    
            month_char= str(retention.issue_date.month)
            if len(month_char)== 1: month_char= '0'+str(retention.issue_date.month)
            retention.month_fiscal_period = month_char     
      
    @api.depends('is_iva')
    def _compute_retention_type(self):
        for partner in self:
            partner.retention_type = 'iva' if partner.is_iva else 'islr'

    def _write_retention_type(self):
        for partner in self:
            partner.is_iva = partner.retention_type == 'iva'      

    def _get_starting_sequence(self):
        self.ensure_one()
        starting_sequence = "%s/%04d/%02d/0000" % (self.journal_id.code, self.date.year, self.date.month)
        if self.journal_id.refund_sequence and self.move_type in ('out_refund', 'in_refund'):
            starting_sequence = "R" + starting_sequence
        return starting_sequence            

    @api.depends('partner_type', 'is_iva')
    def _compute_destination_account_id(self):
        for retention in self:
            if retention.partner_type == 'customer':
                # Clientes Venta.
                if retention.is_iva:
                    retention.destination_account_id = retention.iva_account_sale_id
                else:
                    retention.destination_account_id = retention.islr_account_sale_id
            elif retention.partner_type == 'supplier':
                # Cuando es proveedor.
                if retention.is_iva:
                    retention.destination_account_id = retention.iva_account_purchase_id
                else:
                    retention.destination_account_id = retention.islr_account_purchase_id
            else:   
                retention.destination_account_id = 'ninguno'   

    @api.depends('partner_id')
    def _compute_company_id(self):
        for retention in self:
            retention.company_id = retention.partner_id.company_id or retention.company_id or self.env.company

    @api.model
    def create(self, values):
        if values['partner_type'] == 'supplier' and (values['code'] == " " or values['code'] =="New"):
            values['code'] = self.env["ir.sequence"].next_by_code("retention.sequence")
        values['state'] =  'posted'  
        return super(Retention, self).create(values)
