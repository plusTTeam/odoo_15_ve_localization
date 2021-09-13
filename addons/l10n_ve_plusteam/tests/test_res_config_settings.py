from odoo.tests.common import TransactionCase
from ..tools.constants import REF_MAIN_COMPANY


class TestResConfigSettings(TransactionCase):

    def setUp(self):
        super(TestResConfigSettings, self).setUp()

        self.company = self.env.ref(REF_MAIN_COMPANY)
        self.account_type = self.env.ref("account.data_account_type_current_liabilities")
        self.new_account = self.env["account.account"].create({
            "code": "987987987",
            "name": "New account",
            "user_type_id": self.account_type.id,
            "reconcile": True
        })

    def test_set_values(self):
        settings = self.env["res.config.settings"].search([("company_id", "=", self.company.id)], limit=1)
        settings.iva_account_purchase_id = self.new_account.id
        settings.set_values()
        settings.flush()
        settings.execute()
        self.assertEqual(self.company.iva_account_purchase_id.id, self.new_account.id,
                         msg="The account was not changed in the company instance")
