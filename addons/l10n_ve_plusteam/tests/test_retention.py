from odoo import fields, _
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase
from ..tools.constants import RETENTION_TYPE_IVA


class TestRetention(TransactionCase):

    def setUp(self):
        super(TestRetention, self).setUp()

        self.partner = self.env.ref("base.partner_admin")
        self.date = fields.Date.today()
        self.invoice_amount = 1000000
        self.invoice_tax = 160000
        self.tax= self.env["account.tax"].create({
            "name": "Dummy Tax",
            "amount": "16.00",
            "type_tax_use": "purchase",
        })
        self.invoice = self.env["account.move"].create({
            'move_type': "out_invoice",
            'partner_id': self.partner.id,
            'invoice_date': self.date,
            'date': self.date,
            'retention_state': "with_retention_iva",
            'amount_tax':self.invoice_tax,
            'invoice_line_ids': [(0, 0, {
                'name': 'product that cost %s' % self.invoice_amount,
                'quantity': 1,
                'price_unit': self.invoice_amount,

            })]
        })
        self.invoice.write({"state": "posted"})
        self.retention = self.env["retention"].create({
            "invoice_number": self.invoice.id,
            "partner_id": self.partner.id,
            "move_type": self.invoice.move_type,
            "retention_type": RETENTION_TYPE_IVA,
            "vat_withholding_percentage": 75.0
        })

    def test_retention_type(self):
        """Test  when create retention for retention_type
        """
        with self.assertRaises(ValidationError) as raise_exception:
            new_retention = self.env["retention"].create({
                "invoice_number": self.invoice.id,
                "partner_id": self.partner.id,
                "move_type": self.invoice.move_type,
                "retention_type": RETENTION_TYPE_IVA,
                "vat_withholding_percentage": 75.0
            })
        self.assertEqual(
            str(raise_exception.exception),
            _("This type was already generated"),
            msg="Field retention_state is wrong"
            )    
            
    def test_compute_amount_retention(self):
        """Test when create retention calculation of the amount
        """
        self.assertEqual(
            self.retention.amount_tax*self.retention.vat_withholding_percentage/100,
            self.retention.amount_retention,
            msg="calculation of the retention amount is wrong"
        )    

