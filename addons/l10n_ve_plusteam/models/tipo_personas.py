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
                               default=0.0, help="Base Imp. percentage: This percentage is applied to the amount of the service according to the concept or type of person to determine the tax base.")
    percentage_retention = fields.Float(string="% Retention",
                               default=0.0, help="Retention percentage: it is the percentage that is applied to the tax base to calculate the withholding according to the concept and type of person.")
    subtracting = fields.Float(string="Subtracting",
                               default=0.0, help="Subtracting:This is the amount that is calculated from the resident natural persons as an exempt amount of tax, that is to say that this amount is subtracted from the withholding calculated to obtain the withholding for resident natural persons.")
    tipo_persona_id = fields.Many2one("tipo.personas", string="Person Type", readonly=True)
