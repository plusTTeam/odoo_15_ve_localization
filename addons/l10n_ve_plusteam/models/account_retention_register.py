# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountRetentionRegister(models.TransientModel):
    _name = 'account.retention.register'
    _description = 'Register Retention'
    
    today = fields.Date.today()
    # == Business fields ==
    issue_date = fields.Date(string="Issue Date", required=True,default=fields.Date.context_today)
    deliver_date = fields.Date(string="Deliver Date", required=True)
    month_fiscal_period = fields.Char(string="Month", compute ='_compute_month_fiscal_char', store=True, readonly=False)
    year_fiscal_period = fields.Char(string="Year", default = str(today.year))
    is_iva = fields.Boolean(string='Is a Company', default=False,
        help="Check if the contact is a company, otherwise it is a person")
    retention_type = fields.Selection(string='Retention Type',
        selection=[('Iva', 'IVA'), ('islr', 'ISLR')],
        compute='_compute_retention_type', inverse='_write_retention_type', default='Iva')
  
     # === partner fields ===
    partner_id = fields.Many2one("res.partner", string="Name", compute = "_get_data_invoice")
    rif = fields.Char(string="RIF", related="partner_id.vat")
    vat_withholding_percentage = fields.Float(string="vat withholding percentage", store=True, readonly=False,
                                              related="partner_id.vat_withholding_percentage")
    # === invoice fields ===
    invoice_number = fields.Many2one("account.move", string="Invoice Number",
                                     domain="[('partner_id', '=', partner_id )]")
    
    currency_id = fields.Many2one('res.currency', string='Currency', store=True, readonly=False,
        help="The payment's currency.")    
   
    # == Fields given through the context ==
    document = fields.Char(string="Document Number", compute = "_get_data_invoice")    
    amount_tax = fields.Monetary(currency_field='currency_id',  compute = "_get_data_invoice") 
    amount_total = fields.Monetary(string="Amount total", compute = "_get_data_invoice",currency_field='currency_id')
    amount_base_taxed = fields.Monetary(string="Amount base taxed", compute = "_get_data_invoice",
                                        currency_field='currency_id')
    amount_base_untaxed = fields.Monetary(string="Amount base untaxed", compute = "_get_data_invoice",
                                        currency_field='currency_id')
    amount_retetion = fields.Float(string="Amount Retention", compute='_compute_amount_retention')  

    can_edit_wizard = fields.Boolean(store=True, copy=False, default=True, 
        help="Technical field used to indicate the user can edit the wizard content such as the amount.")
   
    # -------------------------------------------------------------------------
    # HELPERS
    # -------------------------------------------------------------------------
    @api.depends('issue_date')
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
            else:    
                wizard.communication = "Sin relacion"

    @api.depends(
        'vat_withholding_percentage',
        'amount_tax')
    def _compute_amount_retention(self):
        for retention in self:
            amount_retetion = retention.amount_tax * retention.vat_withholding_percentage / 100
            retention.amount_retetion = amount_retetion

    @api.depends('is_iva')
    def _compute_company_type(self):
        for partner in self:
            partner.retention_type = 'iva' if partner.is_iva else 'islr'

    def _write_company_type(self):
        for partner in self:
            partner.is_iva = partner.retention_type == 'iva'

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

    def action_create_retention(self):
        retentions = self._create_retentions()

        if self._context.get('dont_redirect_to_retentions'):
            return True

        action = {
            'name': _('Retention'),
            'type': 'ir.actions.act_window',
            'res_model': 'retention',
            'context': {'create': False},
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

    def _create_payment_vals_from_wizard(self):
        payment_vals = {
            'date': self.payment_date,
            'amount': self.amount,
            'payment_type': self.payment_type,
            'partner_type': self.partner_type,
            'ref': self.communication,
            'journal_id': self.journal_id.id,
            'currency_id': self.currency_id.id,
            'partner_id': self.partner_id.id,
            'partner_bank_id': self.partner_bank_id.id,
            'payment_method_id': self.payment_method_id.id,
            'destination_account_id': self.line_ids[0].account_id.id
        }

        if not self.currency_id.is_zero(self.payment_difference) and self.payment_difference_handling == 'reconcile':
            payment_vals['write_off_line_vals'] = {
                'name': self.writeoff_label,
                'amount': self.payment_difference,
                'account_id': self.writeoff_account_id.id,
            }
        return payment_vals
        