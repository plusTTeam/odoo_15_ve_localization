# -*- coding: utf-8 -*-

import pytz
from datetime import datetime, timedelta
from odoo import fields, models, api
from ..tools.constants import GLOBAL_TIME_OFF


class ResourceCalendarLeaves(models.Model):
    _inherit = "resource.calendar.leaves"

    @api.model
    def add_holidays(self):
        now, ve_timezone = self.get_now_with_timezone()
        years = [now.year, now.year + 1]
        for year in years:
            for holiday in GLOBAL_TIME_OFF:
                date = ve_timezone.localize(datetime(
                    year=year,
                    month=int(holiday["month"]),
                    day=int(holiday["day"])
                ))
                if date < now:
                    continue
                utc_offset = date.utcoffset().total_seconds() * (-1)
                self.create({
                    "calendar_id": self.env.ref("resource.resource_calendar_std").id,
                    "name": holiday["name"],
                    "date_from": (date.replace(tzinfo=None) + timedelta(seconds=utc_offset)),
                    "date_to": (fields.Datetime.end_of(date.replace(tzinfo=None), "day") + timedelta(seconds=utc_offset))
                })

    @api.model
    def add_days_weekend(self):
        now, ve_timezone = self.get_now_with_timezone()
        weekends = self.all_weekends(now.replace(tzinfo=None))
        start_dates = self.search([]).mapped("date_from")
        for weekend in weekends:
            utc_offset = ve_timezone.utcoffset(weekend).total_seconds() * (-1)
            if (fields.Datetime.start_of(weekend, "day") + timedelta(seconds=utc_offset)) in start_dates:
                continue
            self.create({
                "calendar_id": self.env.ref("resource.resource_calendar_std").id,
                "name": "Fin de Semana",
                "date_from": (fields.Datetime.start_of(weekend, "day") + timedelta(seconds=utc_offset)),
                "date_to": (fields.Datetime.end_of(weekend, "day") + timedelta(seconds=utc_offset))
            })

    @api.model
    def all_weekends(self, now):
        current_year = now.year
        next_year = current_year + 1
        weekends = []
        if now.weekday() <= 5:
            weekends.append(now + timedelta(days=5 - now.weekday()))
        weekends.append(now + timedelta(days=6 - now.weekday()))
        band = True
        while band:
            weekends.append(weekends[-1] + timedelta(days=6))
            weekends.append(weekends[-1] + timedelta(days=1))
            band = weekends[-1].year == current_year or weekends[-1].year == next_year
        return weekends

    @api.model
    def get_now_with_timezone(self):
        ve_timezone = pytz.timezone(self.env.user.tz or "America/Caracas")
        return datetime.now(tz=ve_timezone), ve_timezone
