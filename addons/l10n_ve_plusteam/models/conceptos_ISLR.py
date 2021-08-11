# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ConceptosISLR(models.Model):
    _name = "conceptos.islr"
    _description = "Conceptos ISLR"

    code = fields.Char(string="Code", required=True)
    name = fields.Char(string="Description", translate=True, required=True)
    description = fields.Char(string="Description Complete", translate=True)
    literal = fields.Char(string="Literal")
    numeral = fields.Integer(string="Numeral")
