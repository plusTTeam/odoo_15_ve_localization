# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    iva_account_purchase_id = fields.Many2one("account.account", string="VAT accounting account for suppliers",
                                              related="company_id.iva_account_purchase_id",
                                              domain="[('company_id', '=', company_id)]", readonly=False)
    iva_account_sale_id = fields.Many2one("account.account", string="VAT accounting account for customer",
                                          related="company_id.iva_account_sale_id",
                                          domain="[('company_id', '=', company_id)]", readonly=False)
    islr_account_purchase_id = fields.Many2one("account.account", string="ISLR accounting account for suppliers",
                                               related="company_id.islr_account_purchase_id",
                                               domain="[('company_id', '=', company_id)]", readonly=False)
    islr_account_sale_id = fields.Many2one("account.account", string="ISLR accounting account for customer",
                                           related="company_id.islr_account_sale_id",
                                           domain="[('company_id', '=', company_id)]", readonly=False)

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        keys = [
            "iva_account_purchase_id",
            "iva_account_sale_id",
            "islr_account_purchase_id",
            "islr_account_sale_id"
        ]
        for key in keys:
            if self.env.company == self.company_id and self[key] and \
                    self[key] != self.company_id[key]:
                self.company.write({
                    key: self[key]
                })
