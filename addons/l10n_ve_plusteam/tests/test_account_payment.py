from datetime import datetime, timedelta
from odoo import fields, _
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase
from ..tools.constants import REF_MAIN_COMPANY, MESSAGE_EXCEPTION_NOT_EXECUTE, MESSAGE_IGTF_AMOUNT_NOT_CALCULATED


class TestAccountPayment(TransactionCase):

    def setUp(self):
        super(TestAccountPayment, self).setUp()

        self.company = self.env.ref(REF_MAIN_COMPANY)
        self.partner = self.env.ref("base.partner_admin")
        self.amount = 10000.0
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
            "igtf": igtf,
            "currency_id": self.env.ref("base.VEF").id
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

    def test_write(self):
        usd_currency = self.env.ref("base.USD")
        payment = self.create_payment(igtf=True)
        payment.write({"currency_id": usd_currency.id})
        self.assertEqual(payment.igtf_move_id.currency_id, usd_currency,
                         msg="Currency field was not change in igtf move")
        new_date = payment.date - timedelta(days=1)
        payment.write({"date": new_date})
        self.assertEqual(payment.igtf_move_id.date, new_date, msg="Date field was not change in igtf move")
        payment.write({"partner_id": False})
        self.assertNotEqual(payment.igtf_move_id.partner_id, self.partner,
                            msg="Partner field was not change in igtf move")
        payment.write({"ref": "Reference"})
        self.assertEqual(payment.igtf_move_id.ref, "Reference", msg="Ref field was not change in igtf move")
        new_amount = self.amount * 2
        payment.write({"amount": new_amount})
        self.assertEqual(payment.igtf_move_id.amount_total, (new_amount * self.company.igtf) / 100,
                         msg="Partner field was not change in igtf move")
        payment.action_post()
        payment.action_draft()
        self.assertEqual(payment.igtf_move_id.state, "draft", msg="State was not change to draft")
        payment.action_cancel()
        self.assertEqual(payment.igtf_move_id.state, "cancel", msg="State was not change to canceled")

    def test_remove_igtf_move(self):
        payment = self.create_payment(igtf=True)
        payment.write({"payment_type": "inbound"})
        self.assertFalse(payment.igtf_move_id, msg="IGTF was not removed")

    def test_create_igtf_move(self):
        payment = self.create_payment(igtf=False)
        payment.write({"igtf": True})
        self.assertTrue(payment.igtf_move_id.id, msg="IGTF was not created")
