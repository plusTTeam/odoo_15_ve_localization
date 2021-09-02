
from odoo import fields
from odoo.tests.common import TransactionCase
from ..tools.constants import RESOURCE_CALENDAR_ATTENDANCE_MODEL, MESSAGE_DAY_NOT_FOUND


class TestResourceCalendarAttendance(TransactionCase):

    def setUp(self):
        super(TestResourceCalendarAttendance, self).setUp()

    def test_update_translations(self):
        self.env[RESOURCE_CALENDAR_ATTENDANCE_MODEL].update_translations()
        attendance = self.env[RESOURCE_CALENDAR_ATTENDANCE_MODEL].search(
            [("name", "=", "Lunes por la mañana")], limit=1)
        self.assertEqual(attendance.name, "Lunes por la mañana", msg=MESSAGE_DAY_NOT_FOUND)
        attendance = self.env[RESOURCE_CALENDAR_ATTENDANCE_MODEL].search(
            [("name", "=", "Martes por la mañana")], limit=1)
        self.assertEqual(attendance.name, "Martes por la mañana", msg=MESSAGE_DAY_NOT_FOUND)
        attendance = self.env[RESOURCE_CALENDAR_ATTENDANCE_MODEL].search(
            [("name", "=", "Miércoles por la mañana")], limit=1)
        self.assertEqual(attendance.name, "Miércoles por la mañana", msg=MESSAGE_DAY_NOT_FOUND)
        attendance = self.env[RESOURCE_CALENDAR_ATTENDANCE_MODEL].search(
            [("name", "=", "Jueves por la mañana")], limit=1)
        self.assertEqual(attendance.name, "Jueves por la mañana", msg=MESSAGE_DAY_NOT_FOUND)
        attendance = self.env[RESOURCE_CALENDAR_ATTENDANCE_MODEL].search(
            [("name", "=", "Viernes por la mañana")], limit=1)
        self.assertEqual(attendance.name, "Viernes por la mañana", msg=MESSAGE_DAY_NOT_FOUND)
