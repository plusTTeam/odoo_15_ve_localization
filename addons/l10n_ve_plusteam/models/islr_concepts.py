# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ISLRConcepts(models.Model):
    _name = "islr.concepts"
    _description = "ISLR Concepts"
    _rec_name = "complete_name_with_code"

    code = fields.Char(string="Code", required=True, index=True)
    name = fields.Char(string="Description", translate=True, required=True)
    description = fields.Char(string="Complete Description", translate=True)
    literal = fields.Char(string="Literal")
    numeral = fields.Integer(string="Numeral")
    complete_name_with_code = fields.Char(
        string="Complete Name with Code",
        compute="_compute_complete_name_with_code",
        store=True
    )

    @api.depends("name", "code")
    def _compute_complete_name_with_code(self):
        for concepts in self:
            concepts.complete_name_with_code = f'[{concepts.code}] {concepts.name}'
