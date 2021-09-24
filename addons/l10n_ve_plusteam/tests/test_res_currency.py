# -*- coding: utf-8 -*-

import datetime
from unittest import mock

from odoo.tests.common import TransactionCase


class TestResCurrency(TransactionCase):
    def setUp(self):
        super(TestResCurrency, self).setUp()
        self.company = self.env["res.company"].create({"name": "company_1"})

    def test_get_rates_uses_datetime(self):
        vef_currency = self.env.ref("base.VEF")
        self.env["res.currency.rate"].create({
            "name": datetime.datetime(year=2021, month=9, day=15, hour=11, minute=30, second=0),
            "exchange_rate": 1 / 1.555,
            "currency_id": vef_currency.id,
            "company_id": self.company.id
        })
        self.env["res.currency.rate"].create({
            "name": datetime.datetime(year=2021, month=9, day=19, hour=11, minute=30, second=0),
            "exchange_rate": 1 / 2.123,
            "currency_id": vef_currency.id,
            "company_id": self.company.id
        })
        self.env["res.currency.rate"].create({
            "name": datetime.datetime(year=2021, month=9, day=21, hour=15, minute=30, second=0),
            "exchange_rate": 1 / 3.123,
            "currency_id": vef_currency.id,
            "company_id": self.company.id
        })
        now_datetime = datetime.datetime(year=2021, month=9, day=21, hour=12, minute=30, second=00)
        with mock.patch(
            "odoo.addons.l10n_ve_plusteam.models.res_currency.datetime",
            wraps=datetime
        ) as datetime_mock:
            datetime_mock.datetime.now = mock.Mock(return_value=now_datetime)
            currency_rates = vef_currency._get_rates(self.company, now_datetime)
        self.assertEqual(
            currency_rates.get(vef_currency.id), 2.123,
            msg="Rate value must be the latest applicable according to now"
        )
