# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from ..tools.constants import DOMAIN_COMPANY


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    iva_account_purchase_id = fields.Many2one("account.account", string="VAT accounting account for suppliers",
                                              related="company_id.iva_account_purchase_id",
                                              domain=DOMAIN_COMPANY, readonly=False)
    iva_account_sale_id = fields.Many2one("account.account", string="VAT accounting account for customer",
                                          related="company_id.iva_account_sale_id",
                                          domain=DOMAIN_COMPANY, readonly=False)
    islr_account_purchase_id = fields.Many2one("account.account", string="ISLR accounting account for suppliers",
                                               related="company_id.islr_account_purchase_id",
                                               domain=DOMAIN_COMPANY, readonly=False)
    islr_account_sale_id = fields.Many2one("account.account", string="ISLR accounting account for customer",
                                           related="company_id.islr_account_sale_id",
                                           domain=DOMAIN_COMPANY, readonly=False)
    igtf = fields.Float(string="IGTF", digits="2", related="company_id.igtf", domain=DOMAIN_COMPANY, readonly=False)
    igtf_account_id = fields.Many2one("account.account", string="ISLR accounting account",
                                      related="company_id.islr_account_sale_id", domain=DOMAIN_COMPANY, readonly=False)

    @api.constrains("igtf")
    def _check_igtf(self):
        for record in self:
            if record.igtf < 0 or record.igtf > 100:
                raise ValidationError(
                    _("The value of the tax on large financial transactions (IGTF) must be between 0 and 100, "
                      "please verify the information")
                )

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        keys = [
            "iva_account_purchase_id",
            "iva_account_sale_id",
            "islr_account_purchase_id",
            "islr_account_sale_id",
            "igtf",
            "igtf_account_id"
        ]
        for key in keys:
            if self.env.company == self.company_id and self[key] and \
                    self[key] != self.company_id[key]:
                self.company_id.write({
                    key: self[key]
                })
