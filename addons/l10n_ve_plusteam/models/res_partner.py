# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import re


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # vat = fields.Char(_sql_constraints = [('chequeo', 'check(*^(V,J,E,G,P,v,j,e,g,p)+[0-9]+$)', 'error en el formato')])

    sale_tips = fields.Many2one('tipo.personas', string="Tipo de Persona")
    taxpayer = fields.Boolean(
        string="Taxpayer",
        default=True,
        help=_("It is used to filter the contributors for the sales book report")
    )

    @api.constrains('vat')
    def _check_something(self):
        for record in self:
            if re.match(r"^[V|E|J|P][0-9]{7,9}$", record.vat) is None:
                raise ValidationError("Error en el formato del RIF")

