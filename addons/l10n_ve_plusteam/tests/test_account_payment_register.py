from odoo.tests.common import TransactionCase
from ..tools.constants import REF_MAIN_COMPANY


class TestAccountPaymentRegister(TransactionCase):

    def setUp(self):
        super(TestAccountPaymentRegister, self).setUp()

        self.company = self.env.ref(REF_MAIN_COMPANY)
        self.partner = self.env.ref("base.user_admin")
        self.amount = 10000
        self.igtf = 10
        self.invoice = self.env["account.move"].create({
            "move_type": "in_invoice",

        })
        self.company.write({
            "igtf": self.igtf
        })
        self.payment = self.env["account.payment"].create({
            "payment_type": "outbound",
            "partner_type": "supplier",
            "partner_id": self.partner.id,
            "amount": self.amount
        })

    def test_compute_igtf_amount(self):
        self.payment.write({
            "igtf": True
        })
        igtf_amount = self.amount * (self.igtf / 100)
        self.assertEqual(self.payment.igtf_amount, igtf_amount, msg="The igtf_amount was not calculated correctly")

    def test_igtf_amount_equals_zero(self):
        self.payment.write({
            "igtf": False
        })
        igtf_amount = 0
        self.assertEqual(self.payment.igtf_amount, igtf_amount, msg="The igtf_amount was not calculated correctly")
