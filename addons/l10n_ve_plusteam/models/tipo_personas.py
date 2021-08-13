# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TipoPersonas(models.Model):
    _name = "tipo.personas"

    id = fields.Char(string="Codigo")
    name = fields.Char(string="Descripcion", translate=True, required=True)
    tabulador = fields.One2many("tabulador.islr", "tipo_persona_id", string="Tabulador")


class TabuladorISLR(models.Model):
    _name = "tabulador.islr"

    concept_id = fields.Many2one('conceptos.islr', string="Concepts",  required=True)
    code_concept = fields.Char(string="Code", related="concept_id.code")
    percentage_base = fields.Float(string="% Base Imp.",
                               default=0.0)
    percentage_reten = fields.Float(string="% Retention",
                               default=0.0)
    subtracting = fields.Float(string="Sustraendo",
                               default=0.0)
    tipo_persona_id = fields.Many2one("tipo.personas", string=" ", readonly=True)
