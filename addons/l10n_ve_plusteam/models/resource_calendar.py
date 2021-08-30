# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'

    hours_per_day = fields.Float(string="Average Hour per Day",
                                 help=_("Average hours per day a resource is supposed to work with this calendar."))

    @api.model
    def remove_working_hours(self):
        working_hour_40 = self.env.ref("resource.resource_calendar_std", raise_if_not_found=False)
        if working_hour_40:
            working_hour_40.update({
                "name": _("Standard 40 hours/week")
            })
        working_hour_35 = self.env.ref("resource.resource_calendar_std_35h", raise_if_not_found=False)
        if working_hour_35:
            working_hour_35.unlink()
        working_hour_38 = self.env.ref("resource.resource_calendar_std_38h", raise_if_not_found=False)
        if working_hour_38:
            working_hour_38.unlink()
