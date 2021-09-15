from odoo import fields
from odoo.tests.common import TransactionCase
from ..tools.constants import RETENTION_TYPE_IVA


class TestTaxUnit(TransactionCase):

    def setUp(self):
        super(TestTaxUnit, self).setUp()

        self.partner = self.env.ref("base.partner_admin")
        self.category = self.env["product.category"].create({"name": "Parent Category"})
        self.product = self.env["product.product"].create({"name": "Product Test"})
        self.date = fields.Date.today()
        invoice_amount = 1000000
        self.invoice = self.env["account.move"].create({
            'move_type': "out_invoice",
            'partner_id': self.partner.id,
            'invoice_date': self.date,
            'date': self.date,
            'invoice_line_ids': [(0, 0, {
                'name': 'product that cost %s' % invoice_amount,
                'quantity': 1,
                'price_unit': invoice_amount,
                'tax_ids': [(6, 0, [])]
            })]
        })
        self.invoice.write({"state": "posted"})

    def test_create_retention(self):
        retention = self.env["retention"].create({
            "invoice_number": self.invoice.id,
            "partner_id": self.partner.id,
            "move_type": self.invoice.move_type,
            "retention_type": RETENTION_TYPE_IVA,
            "vat_withholding_percentage": 75.0
        })
        self.assertTrue(retention.destination_account_id is not False,
                        msg="The destination account was not configured correctly")
        self.assertTrue(len(retention.move_id.line_ids), msg="the account movements were not created")
