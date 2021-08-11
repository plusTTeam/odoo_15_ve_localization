# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError
import re



class ResPartner(models.Model):
    _inherit = 'res.partner'

    sale_tips = fields.Many2one('tipo.personas', string="Tipo de Persona")

    @api.constrains('vat')
    def _check_something(self):
        for record in self:
            if re.match(r"^[V|E|J|P][0-9]{7,9}$", record.vat) is None:
                raise ValidationError("Formato RIF/Cédula Invalido. Debe comenzar con una letra (V,J,E,P) seguido de 7 o 9 números")

