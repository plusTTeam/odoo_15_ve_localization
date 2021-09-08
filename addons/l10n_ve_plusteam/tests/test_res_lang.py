from odoo.tests.common import TransactionCase
from ..tools.constants import RES_LANG_MODEL, RES_PARTNER_MODEL


class TestResLang(TransactionCase):

    def setUp(self):
        super(TestResLang, self).setUp()

    def test_install_lang_es_ve(self):
        lang_code = "en_US"
        if not self.env[RES_LANG_MODEL]._activate_lang(lang_code):
            self.env[RES_LANG_MODEL]._create_lang(lang_code)
        ir_default = self.env["ir.default"]
        default_value = ir_default.get(RES_PARTNER_MODEL, "lang")
        if default_value is None or default_value == "es_VE":
            ir_default.set(RES_PARTNER_MODEL, "lang", lang_code)
            partner = self.env.company.partner_id
            if not partner.lang:
                partner.write({"lang": lang_code})
            lang_install = self.env["base.language.install"].create({
                "lang": "es_VE",
                "overwrite": True
            })
            lang_install.lang_install()
            lang_install.switch_lang()

        self.env[RES_LANG_MODEL].install_lang_es_ve()
        ir_default = self.env["ir.default"]
        default_value_lang = ir_default.get(RES_PARTNER_MODEL, "lang")
        self.assertEqual(default_value_lang, "es_VE", msg="The default value for the language is not 'es_VE'")
