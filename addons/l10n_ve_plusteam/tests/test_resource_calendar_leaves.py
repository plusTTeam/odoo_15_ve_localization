from odoo.tests.common import TransactionCase
from ..tools.constants import GLOBAL_TIME_OFF, RESOURCE_CALENDAR_LEAVES_MODEL


class TestTaxUnit(TransactionCase):

    def setUp(self):
        super(TestTaxUnit, self).setUp()

    def test_add_holidays(self):
        self.env[RESOURCE_CALENDAR_LEAVES_MODEL].add_holidays()
        found_day = False
        for holiday in GLOBAL_TIME_OFF:
            day = self.env[RESOURCE_CALENDAR_LEAVES_MODEL].search([("name", "=", holiday["name"])], limit=1)
            if day:
                found_day = True
                self.assertEqual(holiday["name"], day.name, msg="Day not located")
            self.assertTrue(found_day, msg="There is no record that matches the search")

    def test_add_days_weekend(self):
        self.env[RESOURCE_CALENDAR_LEAVES_MODEL].add_days_weekend()
        days = self.env[RESOURCE_CALENDAR_LEAVES_MODEL].search([("name", "=", "Fin de Semana")])
        self.assertTrue(len(days) > 1, msg="There is no record that matches the search")
