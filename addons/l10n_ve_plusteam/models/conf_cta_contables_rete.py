# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ConfResconfigsettings(models.TransientModel):
    _inherit = "res.config.settings"

    purchase_account_id_iva = fields.Many2one("account.account", string="Accounting Account VAT Purchase")
    sale_account_id_iva = fields.Many2one("account.account", string="Accounting Account VAT Sales")
    purchase_account_id_islr = fields.Many2one("account.account", string="ISLR Purchase Account Account")
    sale_account_id_islr = fields.Many2one("account.account", string="ISLR Sale Accounting Account")

    def set_values(self):
        super(ConfResconfigsettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('l10n_ve_plusteam.purchase_account_id_iva', int(self.purchase_account_id_iva.id))
        set_param('l10n_ve_plusteam.sale_account_id_iva', int(self.sale_account_id_iva.id))
        set_param('l10n_ve_plusteam.purchase_account_id_islr', int(self.purchase_account_id_islr.id))
        set_param('l10n_ve_plusteam.sale_account_id_islr', int(self.sale_account_id_islr.id))

    @api.model
    def get_values(self):
        res = super(ConfResconfigsettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res['purchase_account_id_iva'] = int(get_param('l10n_ve_plusteam.purchase_account_id_iva'))
        res['sale_account_id_iva'] = int(get_param('l10n_ve_plusteam.sale_account_id_iva'))
        res['purchase_account_id_islr'] = int(get_param('l10n_ve_plusteam.purchase_account_id_islr'))
        res['sale_account_id_islr'] = int(get_param('l10n_ve_plusteam.sale_account_id_islr'))
        return res
