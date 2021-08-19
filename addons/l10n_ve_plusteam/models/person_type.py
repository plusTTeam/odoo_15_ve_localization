# -*- coding: utf-8 -*-

from odoo import models, fields, _


class PersonType(models.Model):
    _name = "person.type"
    _description = "Person Type"

    code = fields.Char(string="Code", required=True)
    name = fields.Char(string="Description", translate=True, required=True)
    islr_tab_ids = fields.One2many("islr.tab", "person_type_id", string="ISLR Tab")


class TabuladorISLR(models.Model):
    _name = "islr.tab"
    _description = "ISLR Tab"

    concept_id = fields.Many2one('islr.concepts', string="ISRL Concepts", required=True)
    percentage_base = fields.Float(
        string="% Tax Base",
        default=0.0,
        required=True,
        help=_("This percentage is applied to the amount of the service "
               "according to the concept or type of person to determine the tax base."))
    percentage_retention = fields.Float(
        string="% Retention",
        default=0.0,
        required=True,
        help=_("It is the percentage that is applied to the tax base "
               "to calculate the withholding according to the concept and type of person."))
    subtracting = fields.Float(
        string="Subtracting",
        default=0.0,
        help=_("This is the amount that is calculated from the resident natural "
               "persons as an exempt amount of tax, that is to say that this amount is subtracted "
               "from the withholding calculated to obtain the withholding for resident natural persons."))
    person_type_id = fields.Many2one("person.type", string="Person Type", readonly=True)
