# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'

    hours_per_day = fields.Float(string="Average Hour per Day",
                                 help=_("Average hours per day a resource is supposed to work with this calendar."))
