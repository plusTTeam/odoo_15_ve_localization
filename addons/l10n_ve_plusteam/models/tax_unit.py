# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TaxUnit(models.Model):
    _name = "tax.unit"
    _description = "Tax Unit"
    _rec_name = "complete_name_with_code"

    date_day = fields.Date(string="Day date", required=True)
    code = fields.Char(string="Gaceta", required=True, index=True)
    date_publication = fields.Date(string="Publication Date", required=True)
    value = fields.Float(string="Value", default=0.00, required=True)

    complete_name_with_code = fields.Char(
        "Complete Name with Code",
        compute="_compute_complete_name_with_code",
        store=True
    )

    @api.depends("value", "code")
    def _compute_complete_name_with_code(self):
        for tax in self:
            tax.complete_name_with_code = f'[{tax.code}] {tax.value}'
