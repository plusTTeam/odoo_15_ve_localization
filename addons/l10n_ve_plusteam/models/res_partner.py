# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import re


class ResPartner(models.Model):
    _inherit = 'res.partner'

    person_tips = fields.Many2one('tipo.personas', string="Person Type")

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
                raise ValidationError("Formato RIF/Cédula Invalido. Debe comenzar con una letra (V,J,E,P) seguido de 7 o 9 números")
