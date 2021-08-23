# -*- coding: utf-8 -*-

import re
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    control_number = fields.Char(string="Control Number")
    form_number = fields.Char(string="form number", help="Import form number C-80 o C-81", defaul="  ")
    file_number = fields.Char(string="file number", help="Import file number", defaul="  ")
    import_doc = fields.Boolean(string="Import")

    @api.constrains('control_number')
    def _check_number_control(self):
        for record in self:
            if re.match(r"^[0-9]{6,9}$", record.control_number) is None:
                raise ValidationError(_("Invalid control number format. Must have at least 6 numbers"))
