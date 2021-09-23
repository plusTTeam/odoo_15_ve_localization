from odoo import _
from odoo.tests.common import TransactionCase, Form
from odoo.exceptions import ValidationError
from ..tools.constants import REF_MAIN_COMPANY, MESSAGE_EXCEPTION_NOT_EXECUTE


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
        self.settings = self.env["res.config.settings"].with_company(self.company).search([], limit=1)

    def test_set_values(self):
        igtf_account = self.env["account.account"].create({
            "code": "6546546",
            "name": "New account",
            "user_type_id": self.env.ref("account.data_account_type_expenses").id,
            "reconcile": True
        })
        self.settings.iva_account_purchase_id = self.new_account.id
        igtf = 2.0
        self.settings.igtf = igtf
        self.settings.igtf_account_id = igtf_account.id
        self.settings.flush()
        self.settings.execute()
        self.assertEqual(self.company.iva_account_purchase_id.id, self.new_account.id,
                         msg="The account was not changed in the company instance")
        self.assertEqual(self.company.igtf, igtf, msg="The IGTF field was not changed in the company instance")
        self.assertEqual(self.company.igtf_account_id.id, igtf_account.id,
                         msg="The IGTF account was not changed in the company instance")

    def test_raise_when_check_igtf(self):
        with self.assertRaises(ValidationError) as raise_exception:
            self.settings.igtf = 150.0
        self.assertEqual(
            str(raise_exception.exception),
            _("The value of the tax on large financial transactions (IGTF) must be between 0 and 100, "
              "please verify the information"),
            msg=MESSAGE_EXCEPTION_NOT_EXECUTE
        )
        with self.assertRaises(ValidationError) as raise_exception:
            self.settings.igtf = -150.0
        self.assertEqual(
            str(raise_exception.exception),
            _("The value of the tax on large financial transactions (IGTF) must be between 0 and 100, "
              "please verify the information"),
            msg=MESSAGE_EXCEPTION_NOT_EXECUTE
        )
