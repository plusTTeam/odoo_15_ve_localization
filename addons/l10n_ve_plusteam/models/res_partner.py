# -*- coding: utf-8 -*-

import re
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    person_type = fields.Many2one('person.type', string="Person Type")

    sale_tips = fields.Many2one('tipo.personas', string="Tipo de Persona")
    taxpayer = fields.Boolean(
        string="Taxpayer",
        default=True,
        help=_("It is used to filter the contributors for the sales book report")
    )

    @api.constrains('vat')
    def _check_rif_field(self):
        for record in self:
            if re.match(r"^[V|E|J|P][0-9]{7,9}$", record.vat) is None:
                raise ValidationError(_("The RIF/Identification Card format is invalid. "
                                        "Must start with a letter (V, J, E, P) followed by 7 or 9 numbers"))
