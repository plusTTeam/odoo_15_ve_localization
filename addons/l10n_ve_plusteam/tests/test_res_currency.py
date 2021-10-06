# -*- coding: utf-8 -*-

import datetime
from unittest import mock

from odoo.tests.common import TransactionCase


class TestResCurrency(TransactionCase):
    def setUp(self):
        super(TestResCurrency, self).setUp()
        self.company = self.env["res.company"].create({"name": "company_1"})
        self.usd_currency = self.env.ref("base.USD")

    def test_get_rates_uses_datetime(self):
        self.env["res.currency.rate"].create({
            "name": datetime.datetime(year=2021, month=9, day=15, hour=11, minute=30, second=0),
            "rate": 0.0025,
            "currency_id": self.usd_currency.id,
            "company_id": self.company.id
        })
        self.env["res.currency.rate"].create({
            "name": datetime.datetime(year=2021, month=9, day=19, hour=11, minute=30, second=0),
            "rate": 0.00025,
            "currency_id": self.usd_currency.id,
            "company_id": self.company.id
        })
        self.env["res.currency.rate"].create({
            "name": datetime.datetime(year=2021, month=9, day=21, hour=15, minute=30, second=0),
            "rate": 0.0002,
            "currency_id": self.usd_currency.id,
            "company_id": self.company.id
        })
        now_datetime = datetime.datetime(year=2021, month=9, day=21, hour=12, minute=30, second=00)
        with mock.patch(
            "odoo.addons.l10n_ve_plusteam.models.res_currency.datetime",
            wraps=datetime
        ) as datetime_mock:
            datetime_mock.datetime.now = mock.Mock(return_value=now_datetime)
            currency_rates = self.usd_currency._get_rates(self.company, now_datetime)
        self.assertEqual(
            currency_rates.get(self.usd_currency.id), 0.00025,
            msg="Rate value must be the latest applicable according to now"
        )

    def test_compute_exchange_rate(self):
        vef_currency = self.env.ref("base.VEF")
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        self.env["res.currency.rate"].create({
            "name": yesterday,
            "rate": 1.555,
            "currency_id": vef_currency.id,
            "company_id": self.company.id
        })
        self.assertEqual(
            vef_currency.exchange_rate, 1 / vef_currency.rate,
            msg="Exchange rate must be 1 / rate"
        )
