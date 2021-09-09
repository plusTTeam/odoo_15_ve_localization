# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    iva_account_purchase_id = fields.Many2one("account.account", string="VAT accounting account for suppliers",
                                              default=lambda self: self.env.company.iva_account_purchase_id)
    iva_account_sale_id = fields.Many2one("account.account", string="VAT accounting account for customer",
                                          default=lambda self: self.env.company.iva_account_sale_id)
    islr_account_purchase_id = fields.Many2one("account.account", string="ISLR accounting account for suppliers",
                                               default=lambda self: self.env.company.islr_account_purchase_id)
    islr_account_sale_id = fields.Many2one("account.account", string="ISLR accounting account for customer",
                                           default=lambda self: self.env.company.islr_account_sale_id)

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('l10n_ve_plusteam.iva_account_purchase_id', int(self.iva_account_purchase_id.id))
        set_param('l10n_ve_plusteam.iva_account_sale_id', int(self.iva_account_sale_id.id))
        set_param('l10n_ve_plusteam.islr_account_purchase_id', int(self.islr_account_purchase_id.id))
        set_param('l10n_ve_plusteam.islr_account_sale_id', int(self.islr_account_sale_id.id))

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res['iva_account_purchase_id'] = int(get_param('l10n_ve_plusteam.iva_account_purchase_id'))
        res['iva_account_sale_id'] = int(get_param('l10n_ve_plusteam.iva_account_sale_id'))
        res['islr_account_purchase_id'] = int(get_param('l10n_ve_plusteam.islr_account_purchase_id'))
        res['islr_account_sale_id'] = int(get_param('l10n_ve_plusteam.islr_account_sale_id'))
        return res
