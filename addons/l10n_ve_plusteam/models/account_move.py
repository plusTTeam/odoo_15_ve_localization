# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError
import re



class AccountMove(models.Model):
    _inherit = 'account.move'

    number_control = fields.Char(string="Control Number")

    @api.constrains('number_control')
    def _check_number_control(self):
        for record in self:
            if re.match(r"^[0-9]{6,9}$", record.number_control) is None:
                raise ValidationError("Formato Numero de control Invalido. Debe tener minimo 6 números")

