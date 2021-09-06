# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountRetentionRegister(models.TransientModel):
    _name = 'account.retention.register'
    _description = 'Register Retention'
    
    today = fields.Date.today()
    # == Business fields ==
    code = fields.Char(string="Retention Number", default=_("New"))
    date = fields.Date(string="Date", required=True, default=fields.Date.context_today)
    invoice_date = fields.Date(string="Invoice Date", required=True, compute = "_get_data_invoice")
    month_fiscal_period = fields.Char(string="Month", compute ='_compute_month_fiscal_char', store=True, readonly=False)
    year_fiscal_period = fields.Char(string="Year", default = str(today.year))
    is_iva = fields.Boolean(string='Is IVA', default=False,
        help="Check if the retention is a iva, otherwise it is islr")
    retention_type = fields.Selection(string='Retention Type',
        selection=[('iva', 'IVA'), ('islr', 'ISLR')],
        compute='_compute_retention_type', inverse='_write_retention_type', default='iva')
  
     # === partner fields ===
    partner_id = fields.Many2one("res.partner", string="Name",domain="[('parent_id','=', False)]",
        check_company=True, compute = "_get_data_invoice")
    rif = fields.Char(string="RIF", related="partner_id.vat")
    vat_withholding_percentage = fields.Float(string="vat withholding percentage", store=True, readonly=False,
                                              related="partner_id.vat_withholding_percentage")
    # === invoice fields ===
    invoice_number = fields.Many2one("account.move", string="Invoice Number",
                                     domain="[('partner_id', '=', partner_id )]")
    
    currency_id = fields.Many2one('res.currency', string='Currency', store=True, readonly=False,
        help="The payment's currency.")    
    company_id =  fields.Char(string="Company", compute = "_get_data_invoice")
    move_type =  fields.Char(string="Move Type", compute = "_get_data_invoice")
    # == Fields given through the context ==
    document = fields.Char(string="Document Number", compute = "_get_data_invoice")    
    amount_tax = fields.Monetary(currency_field='currency_id',  compute = "_get_data_invoice") 
    amount_total = fields.Monetary(string="Amount total", compute = "_get_data_invoice",currency_field='currency_id')
    amount_base_taxed = fields.Monetary(string="Amount base taxed", compute = "_get_data_invoice",
                                        currency_field='currency_id')
    amount_base_untaxed = fields.Monetary(string="Amount base untaxed", compute = "_get_data_invoice",
                                        currency_field='currency_id')
    amount_retention = fields.Float(string="Amount Retention", compute='_compute_amount_retention')

    can_edit_wizard = fields.Boolean(store=True, copy=False, default=True, 
        help="Technical field used to indicate the user can edit the wizard content such as the amount.")
   
    # -------------------------------------------------------------------------
    # HELPERS
    # -------------------------------------------------------------------------
    @api.depends('date')
    def _get_data_invoice(self):
       
        lines = self.env['account.move'].browse(self._context.get('active_ids', []))   
        for wizard in self:
            if lines:
                wizard.document = lines.name + ' _ ' + lines.ref
                wizard.amount_tax = lines.amount_tax
                wizard.amount_base_taxed = lines.amount_base_taxed
                wizard.amount_total = lines.amount_total
                wizard.partner_id = lines.partner_id
                wizard.amount_base_untaxed = lines.amount_untaxed-lines.amount_base_taxed
                wizard.invoice_date = lines.date
                wizard.company_id = lines.company_id.id
                wizard.move_type = lines.move_type
            else:    
                wizard.communication = "Sin relacion"

    @api.depends(
        'vat_withholding_percentage',
        'amount_tax')
    def _compute_amount_retention(self):
        for retention in self:
            amount_retention = retention.amount_tax * retention.vat_withholding_percentage / 100
            retention.amount_retention = amount_retention

    @api.depends('is_iva')
    def _compute_retention_type(self):
        for partner in self:
            partner.retention_type = 'iva' if partner.is_iva else 'islr'

    def _write_retention_type(self):
        for partner in self:
            partner.is_iva = partner.retention_type == 'iva' 

    @api.onchange('vat_withholding_percentage')
    def _onchange_value_withholding_percentage(self):
        for retention in self:
              retention.amount_retention = retention.amount_tax * retention.vat_withholding_percentage / 100

    @api.depends('date')
    def _compute_month_fiscal_char(self):
        for retention in self:    
            month_char= str(retention.date.month)
            if len(month_char)== 1: month_char= '0'+str(retention.date.month)
            retention.month_fiscal_period = month_char

    def _create_retention_vals_from_wizard(self):
        retention_vals = {
             'date': self.date,
             'month_fiscal_period':self.month_fiscal_period,
             'year_fiscal_period':self.year_fiscal_period,
             'retention_type':self.retention_type,
             'move_type':self.move_type,
             'code':self.code,
             'company_id':self.company_id,
             'partner_id':self.partner_id.id,
             'vat_withholding_percentage':self.vat_withholding_percentage,
             'invoice_number':self.invoice_number,
             'amount_retention':self.amount_retention,
             'amount_base_untaxed':self.amount_base_untaxed
        }

        return retention_vals

    def _create_retentions(self):
        self.ensure_one()
        edit_mode = self.can_edit_wizard

        if edit_mode:
            retention_vals = self._create_retention_vals_from_wizard()
            retention_vals_list = [retention_vals]

        retentions = self.env['retention'].create(retention_vals_list)
        
        return retentions

    def action_create_retention(self):
        retentions = self._create_retentions()

        if self._context.get('dont_redirect_to_retentions'):
            return True

        action = {
            'name': _('Retention'),
            'type': 'ir.actions.act_window',
            'res_model': 'retention',
            'context': {'create': True},
        }
        if len(retentions) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': retentions.id,
            })
        else:
            action.update({
                'view_mode': 'tree,form',
                'domain': [('id', 'in', retentions.ids)],
            })
        return action


        