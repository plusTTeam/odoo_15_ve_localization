# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError
import re



class AccountMove(models.Model):
    _inherit = 'account.move'

    number_control = fields.Char(string="Control Number")
    form_number = fields.Char(string="form number", help="Import form number C-80 o C-81", defaul="  ")
    file_number = fields.Char(string="file number", help="Import file number", defaul="  ")
    import_doc = fields.Boolean(string="Import")

    @api.constrains('number_control')
    def _check_number_control(self):
        for record in self:
            if re.match(r"^[0-9]{6,9}$", record.number_control) is None:
                raise ValidationError("Formato Numero de control Invalido. Debe tener minimo 6 números")

