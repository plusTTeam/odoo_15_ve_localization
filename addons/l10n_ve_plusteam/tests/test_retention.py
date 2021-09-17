from odoo import fields, _
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase, Form
from ..tools.constants import RETENTION_TYPE_ISLR, RETENTION_TYPE_IVA


class TestRetention(TransactionCase):

    def setUp(self):
        super(TestRetention, self).setUp()

        self.partner = self.env.ref("base.partner_admin")
        self.date = fields.Date.today()
        self.invoice_amount = 1000000
        self.invoice_tax = 160000
        self.tax = self.env["account.tax"].create({
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
            'amount_tax': self.invoice_tax,
            'invoice_line_ids': [(0, 0, {
                'name': 'product that cost %s' % self.invoice_amount,
                'quantity': 1,
                'price_unit': self.invoice_amount,

            })]
        })
        self.invoice.write({"state": "posted"})
        self.retention = self.env["retention"].create({
            "invoice_id": self.invoice.id,
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
                "invoice_id": self.invoice.id,
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
            self.retention.amount_tax * self.retention.vat_withholding_percentage / 100,
            self.retention.amount_retention,
            msg="calculation of the retention amount is wrong"
        )

        )
        
    def test_onchange_value_withholding(self):
        """Test  when onchange_value_withholding porcentage
        """
        with Form(self.retention) as retention:
            retention.vat_withholding_percentage = 100
        self.assertEqual(
            self.retention.amount_tax*self.retention.vat_withholding_percentage/100,
            self.retention.amount_retention,
            msg="calculation of the retention amount is wrong"
        )           
    def test_create_retention(self):
        retention = self.env["retention"].create({
            "invoice_id": self.invoice.id,
            "partner_id": self.partner.id,
            "move_type": self.invoice.move_type,
            "retention_type": RETENTION_TYPE_IVA,
            "vat_withholding_percentage": 75.0
        })
        self.assertTrue(retention.destination_account_id is not False,
                        msg="The destination account was not configured correctly")
        self.assertTrue(len(retention.move_id.line_ids), msg="the account movements were not created")

    def test_month_fiscal_char(self):
        self.assertEqual(
            self.retention.month_fiscal_period,
            "0" + str(self.retention.date.month),
            msg="Field month fiscal period is wrong"
        )    

    def test_type_document(self):
         self.assertEqual(
            self.retention.type_document,
            _('Invoice'),
            msg="Field type document is wrong"
        )    
    
    def test_retention_type_other(self):
        """Test  when create retention for retention_type
        """
        with Form(self.retention) as retention:
            self.retention.retention_type = RETENTION_TYPE_ISLR
            self.invoice.write({"retention_state": "with_retention_both"})
        self.assertEqual(
            self.invoice.retention_state,
            "with_retention_both",
            msg="Field retention_state is wrong"
            )    

    def test_partner_id(self):
        """Test  partner id equal invoice
        """
        with self.assertRaises(ValidationError) as raise_exception:
            self.retention.partner_id = " "
        self.assertEqual(
            str(raise_exception.exception),
            _("The selected contact is different from the invoice contact, "
                      "they must be the same, please correct it"),
            msg="Field partner id is wrong"
            )    

    def test_vat_withholding_percentage(self):
        """Test  withholding percentage > 0
        """
        with self.assertRaises(ValidationError) as raise_exception:
            self.retention.vat_withholding_percentage = 0
        self.assertEqual(
            str(raise_exception.exception),
            _("The retention percentage must be between the values 1 and 100, "
                      "please verify that the value is in this range"),
            msg="Field withholding percentage is wrong"
            )    

    def test_complete_name(self):
        self.assertEqual(
            self.retention.complete_name_with_code,
            f"[{self.retention.code}] {self.retention.original_document_number}",
            msg="Field complete_name_with_code is wrong"
        )    

