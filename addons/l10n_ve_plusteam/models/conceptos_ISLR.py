# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ConceptosISLR(models.Model):
    _name = "conceptos.islr"
    _description = "Conceptos ISLR"
    _rec_name = "complete_name_with_code"

    # _sql_constraints = [('code_unique', 'unique(code)', 'Name should be unique')]

    code = fields.Char(string="Code", required=True, index=True)
    name = fields.Char(string="Description", translate=True, required=True)
    description = fields.Char(string="Description Complete", translate=True)
    literal = fields.Char(string="Literal")
    numeral = fields.Integer(string="Numeral")

    complete_name_with_code = fields.Char(
        "Complete Name with Code",
        compute="_compute_complete_name_with_code",
        store=True
    )

    @api.depends("name", "code")
    def _compute_complete_name_with_code(self):
        for islr in self:
            islr.complete_name_with_code = f'[{islr.code}] {islr.name}'

