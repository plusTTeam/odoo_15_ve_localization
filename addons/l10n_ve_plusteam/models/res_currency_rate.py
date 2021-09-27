# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCurrencyRate(models.Model):
    _inherit = "res.currency.rate"

    name = fields.Datetime(index=True, string="Date", default=fields.Datetime.now)
    exchange_rate = fields.Float(
        digits=[12, 4], default=1.0,
        string="Rate",
        help="The rate of the currency to the currency of rate 1"
    )
    rate = fields.Float(compute="_compute_rate", store=True)

    @staticmethod
    def _calculate_exchange_rate_from_rate(values):
        if "exchange_rate" not in values and "rate" in values:
            values["exchange_rate"] = 1 / (values["rate"] or 1.0)
        values.pop("rate", None)
        return values

    @api.depends("exchange_rate")
    def _compute_rate(self):
        for currency_rate in self:
            currency_rate.rate = 1 / currency_rate.exchange_rate

    @api.model
    def create(self, values):
        return super().create(self._calculate_exchange_rate_from_rate(values))

    @api.model
    def write(self, values):
        return super().write(self._calculate_exchange_rate_from_rate(values))
