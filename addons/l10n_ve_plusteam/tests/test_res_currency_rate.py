# -*- coding: utf-8 -*-

import datetime

from odoo.tests.common import TransactionCase


class TestResCurrencyRate(TransactionCase):
    def test_name_is_datetime(self):
        vef_currency = self.env.ref("base.VEF")
        first_datetime = datetime.datetime.now()
        second_datetime = first_datetime + datetime.timedelta(seconds=1)
        first_rate = self.env["res.currency.rate"].create({
            "name": first_datetime,
            "exchange_rate": 1 / 2.123,
            "currency_id": vef_currency.id
        })
        second_rate = self.env["res.currency.rate"].create({
            "name": second_datetime,
            "exchange_rate": 1 / 3.123,
            "currency_id": vef_currency.id
        })
        self.assertEqual(
            first_rate.name, first_datetime,
            msg="First rate date must have date and time according to initialization"
        )
        self.assertEqual(
            first_rate.rate, 2.123,
            msg="First rate value must be the same as initialization, including decimals"
        )
        self.assertEqual(
            second_rate.name, second_datetime,
            msg="Second rate date must have date and time according to initialization, "
                "and should've been created with no unique constraint errors"
        )
        self.assertEqual(
            second_rate.rate, 3.123,
            msg="Second rate value must be the same as initialization, including decimals"
        )
