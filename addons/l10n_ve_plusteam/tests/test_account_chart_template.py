from odoo.tests.common import TransactionCase


class TestAccountChartTemplate(TransactionCase):

    def setUp(self):
        super(TestAccountChartTemplate, self).setUp()

        self.new_company = self.env["res.company"].sudo(True).create({
            "name": "Second Company"
        })
        self.user = self.env.ref("base.user_admin")
        self.chart_template = self.env.ref("l10n_ve_plusteam.ve_chart_template_amd")

    def test_update_translation_accounts(self):
        account_liquidity_transfer = self.env["account.account"].search([("name", "=", "Transferencia de liquidez")])
        for account in account_liquidity_transfer:
            account.write({"name": "Liquidity Transfer"})
        account_undistributed_profits_losses = self.env["account.account"].search(
            [("name", "=", "Ganancias/pérdidas no distribuidas")])
        for account in account_undistributed_profits_losses:
            account.write({"name": "Undistributed Profits/Losses"})

        account_liquidity_transfer_template = self.env["account.account.template"].search(
            [("name", "=", "Transferencia de liquidez")])
        for account in account_liquidity_transfer_template:
            account.write({"name": "Liquidity Transfer"})
        account_undistributed_profits_losses_template = self.env["account.account.template"].search(
            [("name", "=", "Ganancias/pérdidas no distribuidas")])
        for account in account_undistributed_profits_losses_template:
            account.write({"name": "Undistributed Profits/Losses"})
        self.env["account.chart.template"].update_translation_accounts()
        account_liquidity_transfer = self.env["account.account"].search([("name", "=", "Transferencia de liquidez")])
        self.assertTrue(len(account_liquidity_transfer), msg="The data was not updated")

    def test_char_template(self):
        """Test if the accounts withholding are defined in the second company instance
        """
        self.user.company_ids |= self.new_company
        setting = self.env["res.config.settings"].with_company(self.new_company).create({})
        self.chart_template.try_loading(company=self.new_company)
        keys = [
            "iva_account_purchase_id",
            "iva_account_sale_id",
            "islr_account_purchase_id",
            "islr_account_sale_id"
        ]
        for key in keys:
            self.assertTrue(self.new_company[key] is not False, msg="The %s field is not defined" % key)
            self.assertEqual(setting[key], self.new_company[key], msg="The values for %s are different" % key)
