# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TipoPersonas(models.Model):
    _name = "tipo.personas"
    _description = "Person Type"

    id = fields.Char(string="Code")
    name = fields.Char(string="Description", translate=True, required=True)
    tabulador = fields.One2many("tabulador.islr", "tipo_persona_id", string="Tabulador")


class TabuladorISLR(models.Model):
    _name = "tabulador.islr"
    _description = "ISRL Concepts"

    concept_id = fields.Many2one('conceptos.islr', string="ISRL Concepts",  required=True)
    code_concept = fields.Char(string="Code", related="concept_id.code")
    percentage_base = fields.Float(string="% Base Imp.",
                               default=0.0)
    percentage_reten = fields.Float(string="% Retention",
                               default=0.0)
    subtracting = fields.Float(string="Subtracting",
                               default=0.0)
    tipo_persona_id = fields.Many2one("tipo.personas", string="Person Type", readonly=True)
