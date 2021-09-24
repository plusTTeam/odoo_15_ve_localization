# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCurrencyRate(models.Model):
    _inherit = "res.currency.rate"

    name = fields.Datetime(index=True, string="Date", default=fields.Datetime.now)
    exchange_rate = fields.Float(
        digits=0, default=1.0,
        string="Rate",
        help="The rate of the currency multiplied by the currency of rate 1"
    )
    rate = fields.Float(compute="_compute_rate", store=True)

    @api.depends("exchange_rate")
    def _compute_rate(self):
        for currency_rate in self:
            currency_rate.rate = 1 / currency_rate.exchange_rate
