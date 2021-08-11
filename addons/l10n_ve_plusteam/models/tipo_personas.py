# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TipoPersonas(models.Model):
    _name = "tipo.personas"

    id = fields.Char(string="Codigo", translate=True)
    name = fields.Char(string="Descripcion", translate=True)

class TabuladorISLR(models.Model):
    _name = "tabulador.islr"

    conceptos = fields.Many2one('conceptos.islr', 'code', string="Conceptos")
    tip_person = fields.Char(string="Persona")
    porcentaje1 = fields.Float(string="Por1",
                               default=0.0)
    porcentaje2 = fields.Float(string="Por2",
                               default=0.0)
