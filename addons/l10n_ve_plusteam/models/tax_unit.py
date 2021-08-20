# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TaxUnit(models.Model):
    _name = "tax.unit"
    _description = "Tax Unit"
    _rec_name = "complete_name_with_code"

    date = fields.Date(string="Date", required=True)
    gazette = fields.Char(string="Gazette", required=True, index=True)
    publication_date = fields.Date(string="Publication Date", required=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    value = fields.Monetary(string="Value", default=0.00, required=True, currency_field='currency_id')

    complete_name_with_code = fields.Char(
        "Complete Name with Code",
        compute="_compute_complete_name_with_code",
        store=True
    )

    @api.depends("value", "gazette")
    def _compute_complete_name_with_code(self):
        for tax in self:
            tax.complete_name_with_code = f"{'Gaceta Nro'} {tax.gazette} "
