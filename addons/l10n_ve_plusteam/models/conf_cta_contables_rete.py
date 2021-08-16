# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ConfResconfigsettings(models.TransientModel):
    _inherit = "res.config.settings"

    purchase_account_id_iva = fields.Many2one("account.account", string="Accounting Account VAT Purchase")
    sale_account_id_iva = fields.Many2one("account.account", string="Accounting Account VAT Sales")
    purchase_account_id_islr = fields.Many2one("account.account", string="ISLR Purchase Account Account")
    sale_account_id_islr = fields.Many2one("account.account", string="ISLR Sale Accounting Account")
