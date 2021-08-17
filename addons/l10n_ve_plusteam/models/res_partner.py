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
    special_taxpayer = fields.Boolean(
        string="Special Taxpayer",
        default=False,
        help=_("It is used to know if the person is a taxpayer or not and to apply withholding.")
    )
    IVA_retention_percentage = fields.Float(
        string="IVA Retention Percentage",
        digits="2",
        help=_("Retention percentage applied to the supplier")
    )

    @api.onchange("taxpayer")
    def _onchange_taxpayer_field(self):
        for record in self:
            if record.taxpayer is False:
                record.special_taxpayer = False

    @api.constrains('vat')
    def _check_rif_field(self):
        for record in self:
            if re.match(r"^[V|E|J|P][0-9]{7,9}$", record.vat) is None:
                raise ValidationError("Formato RIF/Cédula Invalido. Debe comenzar con una letra (V,J,E,P) seguido de 7 o 9 números")
