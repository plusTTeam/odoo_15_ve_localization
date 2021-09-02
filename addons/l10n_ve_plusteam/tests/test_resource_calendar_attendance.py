
from odoo import fields
from odoo.tests.common import TransactionCase


class TestResourceCalendarAttendance(TransactionCase):

    def setUp(self):
        super(TestResourceCalendarAttendance, self).setUp()

    def test_update_translations(self):
        self.env["resource.calendar.attendance"].update_translations()
        attendance = self.env["resource.calendar.attendance"].search([("name", "=", "Lunes por la mañana")], limit=1)
        self.assertEqual(attendance.name, "Lunes por la mañana", msg="Day not found")
        attendance = self.env["resource.calendar.attendance"].search([("name", "=", "Martes por la mañana")], limit=1)
        self.assertEqual(attendance.name, "Martes por la mañana", msg="Day not found")
        attendance = self.env["resource.calendar.attendance"].search(
            [("name", "=", "Miércoles por la mañana")], limit=1)
        self.assertEqual(attendance.name, "Miércoles por la mañana", msg="Day not found")
        attendance = self.env["resource.calendar.attendance"].search([("name", "=", "Jueves por la mañana")], limit=1)
        self.assertEqual(attendance.name, "Jueves por la mañana", msg="Day not found")
        attendance = self.env["resource.calendar.attendance"].search([("name", "=", "Viernes por la mañana")], limit=1)
        self.assertEqual(attendance.name, "Viernes por la mañana", msg="Day not found")
