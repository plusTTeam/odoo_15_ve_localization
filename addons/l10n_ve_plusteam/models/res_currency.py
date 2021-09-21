# -*- coding: utf-8 -*-

import datetime

from odoo import models


class ResCurrency(models.Model):
    _inherit = "res.currency"

    def _get_rates(self, company, date):
        now_time = datetime.datetime.now().time()
        now_datetime = datetime.datetime.combine(date, now_time)
        return super()._get_rates(company, now_datetime)
