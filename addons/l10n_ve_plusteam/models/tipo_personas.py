# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TipoPersonas(models.Model):
    _name = "tipo.personas"

    id = fields.Char(string="Codigo", translate=True)
    name = fields.Char(string="Descripcion", translate=True)

