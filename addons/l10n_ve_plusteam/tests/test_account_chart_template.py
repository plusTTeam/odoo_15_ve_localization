from odoo.tests.common import TransactionCase
from ..tools.constants import REF_MAIN_COMPANY


class TestAccountChartTemplate(TransactionCase):

    def setUp(self):
        super(TestAccountChartTemplate, self).setUp()

        self.main_company = self.env.ref(REF_MAIN_COMPANY)
        self.second_company = self.env["res.company"].sudo(True).create({
            "name": "Second Company"
        })
        self.chart_template = self.env.ref("l10n_ve_plusteam.ve_chart_template_amd")

    def test_char_template(self):
        """Test if the accounts withholding are defined in the second company instance
        """
        second_company_settings = self.env["res.config.settings"].with_company(self.second_company)
        second_company_settings.write({
            "chart_template_id": self.chart_template.id
        })
        keys = [
            "iva_account_purchase_id",
            "iva_account_sale_id",
            "islr_account_purchase_id",
            "islr_account_sale_id"
        ]
        for key in keys:
            self.assertTrue(self.second_company[key] is not False, msg="The %s field is not defined" % key)
            self.assertEqual(second_company_settings[key], self.second_company[key],
                             msg="The values for %s are different" % key)
