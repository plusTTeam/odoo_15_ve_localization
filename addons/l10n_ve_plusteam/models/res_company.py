# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.company'

    vat_withholding_percentage = fields.Float(
        string="VAT Withholding Percentage",
        digits="2",
        help=_("Withholding percentage applied to the company")
    )

    @api.constrains("vat_withholding_percentage")
    def _check_vat_withholding_percentage(self):
        for record in self:
            if record.vat_withholding_percentage < 0 or record.vat_withholding_percentage > 100:
                raise ValidationError(
                    _("The retention percentage must be between the the values 0 and 100, "
                      "please verify that the value is in this range")
                )
