# -*- coding: utf-8 -*-

import datetime

from odoo.tests.common import TransactionCase


class TestResCurrencyRate(TransactionCase):
    def setUp(self):
        super(TestResCurrencyRate, self).setUp()
        self.company = self.env["res.company"].create({"name": "company_1"})

    def test_name_is_datetime(self):
        vef_currency = self.env.ref("base.VEF")
        first_datetime = datetime.datetime.now()
        second_datetime = first_datetime + datetime.timedelta(seconds=1)
        first_currency = self.env["res.currency.rate"].create({
            "name": first_datetime,
            "rate": 2.123,
            "currency_id": vef_currency.id
        })
        second_currency = self.env["res.currency.rate"].create({
            "name": second_datetime,
            "rate": 3.123,
            "currency_id": vef_currency.id
        })
        self.assertEqual(first_currency.name, first_datetime)
        self.assertEqual(first_currency.rate, 2.123)
        self.assertEqual(second_currency.name, first_datetime)
        self.assertEqual(second_currency.rate, 3.123)
