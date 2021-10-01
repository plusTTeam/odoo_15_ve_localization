# -*- coding: utf-8 -*-

import datetime

from odoo.tests.common import TransactionCase


class TestResCurrencyRate(TransactionCase):
    def setUp(self):
        super().setUp()
        self.usd_currency = self.env.ref("base.USD")

    def test_name_is_datetime(self):
        first_datetime = datetime.datetime.now()
        second_datetime = first_datetime + datetime.timedelta(seconds=1)
        first_rate = self.env["res.currency.rate"].create({
            "name": first_datetime,
            "rate": 0.0025,
            "currency_id": self.usd_currency.id
        })
        second_rate = self.env["res.currency.rate"].create({
            "name": second_datetime,
            "rate": 0.00025,
            "currency_id": self.usd_currency.id
        })
        self.assertEqual(
            first_rate.name, first_datetime,
            msg="First rate date must have date and time according to initialization"
        )
        self.assertEqual(
            first_rate.rate, 0.0025,
            msg="First rate value must be the same as initialization, including decimals"
        )
        self.assertEqual(
            second_rate.name, second_datetime,
            msg="Second rate date must have date and time according to initialization, "
                "and should've been created with no unique constraint errors"
        )
        self.assertEqual(
            second_rate.rate, 0.00025,
            msg="Second rate value must be the same as initialization, including decimals"
        )

    def test_create_with_rate_and_no_exchange_rate(self):
        currency_rate = self.env["res.currency.rate"].create({
            "name": datetime.datetime.now(),
            "rate": 0.0025,
            "currency_id": self.usd_currency.id
        })
        self.assertEqual(
            currency_rate.exchange_rate, 400,
            msg="Exchange Rate must be 1 / rate if not specified in create params"
        )

    def test_create_with_rate_and_exchange_rate(self):
        exchange_rate = 4000
        currency_rate = self.env["res.currency.rate"].create({
            "name": datetime.datetime.now(),
            "rate": 0.05,
            "exchange_rate": exchange_rate,
            "currency_id": self.usd_currency.id
        })
        self.assertEqual(
            currency_rate.exchange_rate, exchange_rate,
            msg="Exchange Rate must be the same as defined in create params"
        )
        self.assertEqual(
            currency_rate.rate, 1 / exchange_rate,
            msg="Rate param of create must be ignored and recalculated with 1 / exchange_rate"
        )

    def test_write_with_rate_and_no_exchange_rate(self):
        rate = 0.0025
        currency_rate = self.env["res.currency.rate"].create({
            "name": datetime.datetime.now(),
            "rate": 0.0035,
            "currency_id": self.usd_currency.id
        })
        currency_rate.write({
            "name": datetime.datetime.now(),
            "rate": rate,
            "currency_id": self.usd_currency.id
        })
        self.assertEqual(
            currency_rate.exchange_rate, 400,
            msg="Exchange Rate must be 1 / rate if not specified in write params"
        )

    def test_write_with_rate_and_exchange_rate(self):
        exchange_rate = 654
        currency_rate = self.env["res.currency.rate"].create({
            "name": datetime.datetime.now(),
            "exchange_rate": 6548,
            "currency_id": self.usd_currency.id
        })
        currency_rate.write({
            "name": datetime.datetime.now(),
            "rate": 5.458,
            "exchange_rate": exchange_rate,
            "currency_id": self.usd_currency.id
        })
        self.assertEqual(
            currency_rate.exchange_rate, exchange_rate,
            msg="Exchange Rate must be the same as defined in write params"
        )
        self.assertEqual(
            currency_rate.rate, 1 / exchange_rate,
            msg="Rate param of write must be ignored and recalculated with 1 / exchange_rate"
        )
