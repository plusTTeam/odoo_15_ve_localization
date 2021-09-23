# -*- coding: utf-8 -*-

import re
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    vat = fields.Char(required=True)
    person_type = fields.Many2one('person.type', string="Person Type")
    taxpayer = fields.Boolean(
        string="Taxpayer",
        default=True,
        help=_("It is used to filter the contributors for the sales book report")
    )
    special_taxpayer = fields.Boolean(
        string="Special Taxpayer",
        default=False,
        help=_("It is used to know if the person is a taxpayer or not and to apply withholding.")
    )
    vat_withholding_percentage = fields.Float(
        string="VAT Withholding Percentage",
        digits="2",
        help=_("Withholding percentage applied to the supplier")
    )

    @api.onchange("taxpayer")
    def _onchange_taxpayer_field(self):
        for record in self:
            if record.taxpayer is False:
                record.special_taxpayer = False

    @api.constrains('vat')
    def _check_rif_field(self):
        for record in self:
            if record.vat and re.match(r"^[V|E|J|P][0-9]{7,9}$", record.vat.upper()) is None:
                raise ValidationError(_("The RIF/Identification Card format is invalid. "
                                        "Must start with a letter (V, J, E, P) followed by 7 or 9 numbers"))

    @api.constrains("vat_withholding_percentage")
    def _check_vat_withholding_percentage(self):
        for record in self:
            if record.vat_withholding_percentage < 0 or record.vat_withholding_percentage > 100:
                raise ValidationError(
                    _("The retention percentage must be between 0 and 100, "
                      "please verify that the value is in this range")
                )
