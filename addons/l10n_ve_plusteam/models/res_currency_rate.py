# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCurrencyRate(models.Model):
    _inherit = "res.currency.rate"

    name = fields.Datetime(index=True, string="Date", default=fields.Datetime.now)
