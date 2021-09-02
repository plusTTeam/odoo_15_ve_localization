
from odoo import fields
from odoo.tests.common import TransactionCase
from ..tools.constants import RESOURCE_CALENDAR_ATTENDANCE_MODEL, MESSAGE_DAY_NOT_FOUND, WEEK_DAYS


class TestResourceCalendarAttendance(TransactionCase):

    def setUp(self):
        super(TestResourceCalendarAttendance, self).setUp()

        mondays = self.env[RESOURCE_CALENDAR_ATTENDANCE_MODEL].search([("name", "=", WEEK_DAYS["monday"]["morning"]["name_spanish"])])
        for monday in mondays:
            monday.write({"name": WEEK_DAYS["monday"]["morning"]["name_english"]})
        mondays = self.env[RESOURCE_CALENDAR_ATTENDANCE_MODEL].search([("name", "=", WEEK_DAYS["monday"]["afternoon"]["name_spanish"])])
        for monday in mondays:
            monday.write({"name": WEEK_DAYS["monday"]["afternoon"]["name_english"]})
        tuesdays = self.env[RESOURCE_CALENDAR_ATTENDANCE_MODEL].search([("name", "=", WEEK_DAYS["tuesday"]["morning"]["name_spanish"])])
        for tuesday in tuesdays:
            tuesday.write({"name": WEEK_DAYS["tuesday"]["morning"]["name_english"]})
        tuesdays = self.env[RESOURCE_CALENDAR_ATTENDANCE_MODEL].search([("name", "=", WEEK_DAYS["tuesday"]["afternoon"]["name_spanish"])])
        for tuesday in tuesdays:
            tuesday.write({"name": WEEK_DAYS["tuesday"]["afternoon"]["name_english"]})
        wednesdays = self.env[RESOURCE_CALENDAR_ATTENDANCE_MODEL].search([("name", "=", WEEK_DAYS["wednesday"]["morning"]["name_spanish"])])
        for wednesday in wednesdays:
            wednesday.write({"name": WEEK_DAYS["wednesday"]["morning"]["name_english"]})
        wednesdays = self.env[RESOURCE_CALENDAR_ATTENDANCE_MODEL].search([("name", "=", WEEK_DAYS["wednesday"]["afternoon"]["name_spanish"])])
        for wednesday in wednesdays:
            wednesday.write({"name": WEEK_DAYS["wednesday"]["afternoon"]["name_english"]})
        tuesdays = self.env[RESOURCE_CALENDAR_ATTENDANCE_MODEL].search([("name", "=", WEEK_DAYS["tuesday"]["morning"]["name_spanish"])])
        for tuesday in tuesdays:
            tuesday.write({"name": WEEK_DAYS["tuesday"]["morning"]["name_english"]})
        tuesdays = self.env[RESOURCE_CALENDAR_ATTENDANCE_MODEL].search([("name", "=", WEEK_DAYS["tuesday"]["afternoon"]["name_spanish"])])
        for tuesday in tuesdays:
            tuesday.write({"name": WEEK_DAYS["tuesday"]["afternoon"]["name_english"]})
        fridays = self.env[RESOURCE_CALENDAR_ATTENDANCE_MODEL].search([("name", "=", WEEK_DAYS["friday"]["morning"]["name_spanish"])])
        for friday in fridays:
            friday.write({"name": WEEK_DAYS["friday"]["morning"]["name_english"]})
        fridays = self.env[RESOURCE_CALENDAR_ATTENDANCE_MODEL].search([("name", "=", WEEK_DAYS["friday"]["afternoon"]["name_spanish"])])
        for friday in fridays:
            friday.write({"name": WEEK_DAYS["friday"]["afternoon"]["name_english"]})

    def test_update_translations(self):
        self.env[RESOURCE_CALENDAR_ATTENDANCE_MODEL].update_translations()
        attendance = self.env[RESOURCE_CALENDAR_ATTENDANCE_MODEL].search(
            [("name", "=", WEEK_DAYS["monday"]["morning"]["name_spanish"])], limit=1)
        self.assertEqual(attendance.name, WEEK_DAYS["monday"]["morning"]["name_spanish"], msg=MESSAGE_DAY_NOT_FOUND)
        attendance = self.env[RESOURCE_CALENDAR_ATTENDANCE_MODEL].search(
            [("name", "=", WEEK_DAYS["tuesday"]["afternoon"]["name_spanish"])], limit=1)
        self.assertEqual(attendance.name, WEEK_DAYS["tuesday"]["morning"]["name_spanish"], msg=MESSAGE_DAY_NOT_FOUND)
        attendance = self.env[RESOURCE_CALENDAR_ATTENDANCE_MODEL].search(
            [("name", "=", WEEK_DAYS["wednesday"]["afternoon"]["name_spanish"])], limit=1)
        self.assertEqual(attendance.name, WEEK_DAYS["wednesday"]["morning"]["name_spanish"], msg=MESSAGE_DAY_NOT_FOUND)
        attendance = self.env[RESOURCE_CALENDAR_ATTENDANCE_MODEL].search(
            [("name", "=", WEEK_DAYS["tuesday"]["morning"]["name_spanish"])], limit=1)
        self.assertEqual(attendance.name, WEEK_DAYS["tuesday"]["morning"]["name_spanish"], msg=MESSAGE_DAY_NOT_FOUND)
        attendance = self.env[RESOURCE_CALENDAR_ATTENDANCE_MODEL].search(
            [("name", "=", WEEK_DAYS["friday"]["morning"]["name_spanish"])], limit=1)
        self.assertEqual(attendance.name, WEEK_DAYS["friday"]["morning"]["name_spanish"], msg=MESSAGE_DAY_NOT_FOUND)
