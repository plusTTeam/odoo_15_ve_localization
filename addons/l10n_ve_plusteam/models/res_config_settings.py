# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Resconfigsettings(models.TransientModel):
    _inherit = "res.config.settings"

    purchase_account_iva_id = fields.Many2one("account.account", string="VAT accounting account for suppliers")
    sale_account_iva_id = fields.Many2one("account.account", string="VAT accounting account for customer")
    purchase_account_islr_id = fields.Many2one("account.account", string="ISLR accounting account for suppliers")
    sale_account_islr_id = fields.Many2one("account.account", string="ISLR accounting account for customer")


    def set_values(self):
        super(Resconfigsettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('l10n_ve_plusteam.purchase_account_iva_id', int(self.purchase_account_iva_id.id))
        set_param('l10n_ve_plusteam.sale_account_iva_id', int(self.sale_account_iva_id.id))
        set_param('l10n_ve_plusteam.purchase_account_islr_id', int(self.purchase_account_islr_id.id))
        set_param('l10n_ve_plusteam.sale_account_islr_id', int(self.sale_account_islr_id.id))

    @api.model
    def get_values(self):
        res = super(Resconfigsettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res['purchase_account_iva_id'] = int(get_param('l10n_ve_plusteam.purchase_account_iva_id'))
        res['sale_account_iva_id'] = int(get_param('l10n_ve_plusteam.sale_account_iva_id'))
        res['purchase_account_islr_id'] = int(get_param('l10n_ve_plusteam.purchase_account_islr_id'))
        res['sale_account_islr_id'] = int(get_param('l10n_ve_plusteam.sale_account_islr_id'))
        return res