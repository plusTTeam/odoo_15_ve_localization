from odoo.tests.common import TransactionCase
from ..tools.constants import RES_LANG_MODEL, RES_PARTNER_MODEL


class TestResLang(TransactionCase):

    def setUp(self):
        super(TestResLang, self).setUp()

    def test_install_lang_es_ve(self):
        self.env[RES_LANG_MODEL].install_lang_es_ve()
        ir_default = self.env["ir.default"]
        default_value_lang = ir_default.get(RES_PARTNER_MODEL, "lang")
        self.assertEqual(default_value_lang, "es_VE", msg="The default value for the language is not 'es_VE'")
