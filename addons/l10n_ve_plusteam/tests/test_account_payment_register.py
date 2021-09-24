from odoo import fields
from odoo.tests.common import TransactionCase
from ..tools.constants import REF_MAIN_COMPANY


class TestAccountPaymentRegister(TransactionCase):

    def setUp(self):
        super(TestAccountPaymentRegister, self).setUp()

        self.igtf = 10
        self.company = self.env.ref(REF_MAIN_COMPANY)
        self.company.write({
            "igtf": self.igtf
        })
        self.partner = self.env.ref("base.user_admin")
        self.date = fields.Date.today()
        self.invoice_amount = 10000
        self.igtf_amount = self.invoice_amount * (self.igtf / 100)

    def create_invoice(self):
        invoice = self.env["account.move"].create({
            "move_type": "in_invoice",
            "partner_id": self.partner.id,
            "invoice_date": self.date,
            "date": self.date,
            "invoice_line_ids": [(0, 0, {
                "name": "product that cost %s" % self.invoice_amount,
                "quantity": 1,
                "price_unit": self.invoice_amount,
            })]
        })
        invoice.action_post()
        return invoice

    def test_compute_igtf_amount(self):
        invoice = self.create_invoice()
        payment = self.env['account.payment.register'].with_context(
            active_model='account.move', active_ids=invoice.ids
        ).create({
            "igtf": True
        })._create_payments()
        igtf_amount = self.invoice_amount * (self.igtf / 100)
        self.assertEqual(payment.igtf_amount, igtf_amount, msg="The igtf_amount was not calculated correctly")

    def test_igtf_amount_equals_zero(self):
        invoice = self.create_invoice()
        payment = self.env['account.payment.register'].with_context(
            active_model='account.move', active_ids=invoice.ids
        ).create({})._create_payments()
        igtf_amount = 0
        self.assertEqual(payment.igtf_amount, igtf_amount, msg="The igtf_amount was not calculated correctly")

    def test_compute_igtf_amount_with_invoices(self):
        invoices = (self.create_invoice() + self.create_invoice())
        payments = self.env['account.payment.register'].with_context(
            active_model='account.move', active_ids=invoices.ids
        ).create({
            "igtf": True
        })._create_payments()
        for payment in payments:
            igtf_amount = self.invoice_amount * (self.igtf / 100)
            self.assertEqual(payment.igtf_amount, igtf_amount, msg="The igtf_amount was not calculated correctly")
