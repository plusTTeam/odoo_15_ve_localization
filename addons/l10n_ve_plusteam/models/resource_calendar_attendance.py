
from odoo import models, api, fields, _


class ResourceCalendarAttendance(models.Model):
    _inherit = 'resource.calendar.attendance'

    name = fields.Char(translate=True)

    @api.model
    def update_translations(self):
        monday = self.search([("name", "=", "Monday Morning")])
        if monday:
            monday.write({"name": _("Monday Morning")})
        monday = self.search([("name", "=", "Monday Afternoon")])
        if monday:
            monday.write({"name": _("Monday Afternoon")})
        tuesday = self.search([("name", "=", "Tuesday Morning")])
        if tuesday:
            tuesday.write({"name": _("Tuesday Morning")})
        tuesday = self.search([("name", "=", "Tuesday Afternoon")])
        if tuesday:
            tuesday.write({"name": _("Tuesday Afternoon")})
        wednesday = self.search([("name", "=", "Wednesday Morning")])
        if wednesday:
            wednesday.write({"name": _("Wednesday Morning")})
        wednesday = self.search([("name", "=", "Wednesday Afternoon")])
        if wednesday:
            wednesday.write({"name": _("Wednesday Afternoon")})
        thursday = self.search([("name", "=", "Thursday Morning")])
        if thursday:
            thursday.write({"name": _("Thursday Morning")})
        thursday = self.search([("name", "=", "Thursday Afternoon")])
        if thursday:
            thursday.write({"name": _("Thursday Afternoon")})
        friday = self.search([("name", "=", "Friday Morning")])
        if friday:
            friday.write({"name": _("Friday Morning")})
        friday = self.search([("name", "=", "Friday Afternoon")])
        if friday:
            friday.write({"name": _("Friday Afternoon")})
