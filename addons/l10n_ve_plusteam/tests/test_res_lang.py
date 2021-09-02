from odoo.tests.common import TransactionCase


class TestResLang(TransactionCase):

    def setUp(self):
        super(TestResLang, self).setUp()

    def test_install_lang_es_ve(self):
        self.env["res.lang"].install_lang_es_ve()
        ir_default = self.env['ir.default']
        default_value_lang = ir_default.get('res.partner', 'lang')
        self.assertEqual(default_value_lang, "es_VE", msg="The default value for the language is not 'es_VE'")
