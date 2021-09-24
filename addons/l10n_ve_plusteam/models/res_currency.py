# -*- coding: utf-8 -*-

import datetime

from odoo import models, fields, api


class ResCurrency(models.Model):
    _inherit = "res.currency"

    exchange_rate = fields.Float(
        compute="_compute_current_exchange_rate", string="Current Rate", digits=0,
        help="The rate of the currency to the currency of rate 1"
    )

    def _get_rates(self, company, date):
        now_time = datetime.datetime.now().time()
        now_datetime = datetime.datetime.combine(date, now_time)
        return super()._get_rates(company, now_datetime)

    @api.depends('rate')
    def _compute_current_exchange_rate(self):
        for currency in self:
            currency.exchange_rate = 1.0 / (currency.rate or 1.0)
