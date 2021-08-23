# -*- coding: utf-8 -*-

from odoo import fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.company'

    vat_withholding_percentage = fields.Float(
        string="VAT Withholding Percentage",
        digits="2",
        help=_("Withholding percentage applied to the company")
    )
