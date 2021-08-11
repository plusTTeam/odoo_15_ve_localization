# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ConceptosISLR(models.Model):
    _name = "conceptos.islr"

    code = fields.Char(string="Codigo", translate=True)
    name = fields.Char(string="Descripcion", translate=True)
    namelarge = fields.Char(string="Descripcion Ampliada", translate=True)
    literal = fields.Char(string="Literal", translate=True)
    numeral = fields.Char(string="Numeral", translate=True)
