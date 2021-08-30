# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import fields, models, api, _
from ..tools.constants import GLOBAL_TIME_OFF


class ResourceCalendarLeaves(models.Model):
    _inherit = "resource.calendar.leaves"

    @api.model
    def add_holidays(self):
        now = datetime.now()
        years = [now.year, now.year + 1]
        for year in years:
            for holiday in GLOBAL_TIME_OFF:
                date = datetime(
                    year=year,
                    month=int(holiday["month"]),
                    day=int(holiday["day"])
                )
                if date <= now:
                    continue
                self.env["resource.calendar.leaves"].create({
                    "calendar_id": self.env.ref("resource.resource_calendar_std").id,
                    "name": holiday["name"],
                    "date_from": (date + timedelta(hours=4)),
                    "date_to": (fields.Datetime.end_of(date, "day") + timedelta(hours=4))
                })

    @api.model
    def add_days_weekend(self):
        today = datetime.now()
        weekends = self.all_weekends(today)
        start_dates = self.env["resource.calendar.leaves"].search([]).mapped("date_from")
        for weekend in weekends:
            if (fields.Datetime.start_of(weekend, "day") + timedelta(hours=4)) in start_dates:
                continue
            self.env["resource.calendar.leaves"].create({
                "calendar_id": self.env.ref("resource.resource_calendar_std").id,
                "name": _("Weekend"),
                "date_from": (fields.Datetime.start_of(weekend, "day") + timedelta(hours=4)),
                "date_to": (fields.Datetime.end_of(weekend, "day") + timedelta(hours=4))
            })

    @api.model
    def all_weekends(self, today):
        current_year = today.year
        next_year = current_year + 1
        weekends = []
        if today.weekday() <= 5:
            weekends.append(today + timedelta(days=5 - today.weekday()))
        weekends.append(today + timedelta(days=6 - today.weekday()))
        band = True
        while band:
            weekends.append(weekends[-1] + timedelta(days=6))
            weekends.append(weekends[-1] + timedelta(days=1))
            band = weekends[-1].year == current_year or weekends[-1].year == next_year
        return weekends
