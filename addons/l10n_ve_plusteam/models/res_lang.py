# -*- coding: utf-8 -*-

from odoo import models, api


class ResLang(models.Model):
    _inherit = 'res.lang'

    @api.model
    def install_lang_es_ve(self):
        lang_code = "es_VE"
        if not self._activate_lang(lang_code):
            self._create_lang(lang_code)
        ir_default = self.env['ir.default']
        default_value = ir_default.get('res.partner', 'lang')
        if default_value is None or default_value == "en_US":
            ir_default.set('res.partner', 'lang', lang_code)
            partner = self.env.company.partner_id
            if not partner.lang:
                partner.write({'lang': lang_code})
            lang_install = self.env["base.language.install"].create({
                "lang": "es_VE",
                "overwrite": True
            })
            lang_install.lang_install()
            lang_install.switch_lang()
        return True
