from odoo import _
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase
from ..tools.constants import REF_MAIN_COMPANY, MESSAGE_EXCEPTION_NOT_EXECUTE, MESSAGE_IGTF_AMOUNT_NOT_CALCULATED


class TestAccountPayment(TransactionCase):

    def setUp(self):
        super(TestAccountPayment, self).setUp()

        self.company = self.env.ref(REF_MAIN_COMPANY)
        self.partner = self.env.ref("base.user_admin")
        self.amount = 10000
        self.igtf = 10
        self.company.write({
            "igtf": self.igtf
        })

    def create_payment(self, igtf=False):
        return self.env["account.payment"].create({
            "payment_type": "outbound",
            "partner_type": "supplier",
            "partner_id": self.partner.id,
            "amount": self.amount,
            "igtf": igtf
        })

    def test_compute_igtf_amount(self):
        payment = self.create_payment(igtf=True)
        igtf_amount = self.amount * (self.igtf / 100)
        self.assertEqual(payment.igtf_amount, igtf_amount, msg=MESSAGE_IGTF_AMOUNT_NOT_CALCULATED)

    def test_igtf_amount_equals_zero(self):
        payment = self.create_payment(igtf=False)
        igtf_amount = 0
        self.assertEqual(payment.igtf_amount, igtf_amount, msg=MESSAGE_IGTF_AMOUNT_NOT_CALCULATED)

    def test_post_iftg_move(self):
        payment = self.create_payment(igtf=True)
        payment.action_post()
        self.assertEqual(payment.igtf_move_id.state, "posted",
                         msg="The accounting entry corresponding to the IGTF was not posted")

    def test_raise_when_not_found_igtf_account(self):
        self.company.write({
            "igtf_account_id": False
        })
        with self.assertRaises(ValidationError) as raise_exception:
            self.create_payment(igtf=True)
        self.assertEqual(
            str(raise_exception.exception),
            _("There is not accounting account for the Tax on Big Financial Transactions (IGTF), "
              "please go to Settings and select an account to apply this tax"),
            msg=MESSAGE_EXCEPTION_NOT_EXECUTE
        )

    def test_raise_when_not_found_igtf_journal(self):
        self.company.write({
            "igtf_journal_id": False
        })
        with self.assertRaises(ValidationError) as raise_exception:
            self.create_payment(igtf=True)
        self.assertEqual(
            str(raise_exception.exception),
            _("There is not journal for the Tax on Big Financial Transactions (IGTF), "
              "please go to Settings and select an journal to apply this tax"),
            msg=MESSAGE_EXCEPTION_NOT_EXECUTE
        )
