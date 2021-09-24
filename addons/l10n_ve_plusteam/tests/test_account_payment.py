from odoo.tests.common import TransactionCase


class TestAccountPayment(TransactionCase):

    def setUp(self):
        super(TestAccountPayment, self).setUp()

        self.payment = self.env["account.payment"].create({})
