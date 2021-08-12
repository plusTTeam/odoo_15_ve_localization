# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TabuladorISLR(models.Model):
    _name = "tabulador.islr"

    conceptos = fields.Many2one('conceptos.islr', 'code', string="Conceptos")
    tip_person = fields.Char(string="Persona")
    porcentaje1 = fields.Float(string="Por1",
                               default=0.0)
    porcentaje2 = fields.Float(string="Por2",
                               default=0.0)

