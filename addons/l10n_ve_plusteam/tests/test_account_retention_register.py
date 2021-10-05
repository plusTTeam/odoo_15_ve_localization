from odoo import fields, _
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase, Form
from ..tools.constants import RETENTION_TYPE_IVA, MESSAGE_DOCUMENT_WRONG


class TestAccountRetentionRegister(TransactionCase):

    def setUp(self):
        super(TestAccountRetentionRegister, self).setUp()

        self.modelo = "account.retention.register"
        self.partner = self.env.ref("base.partner_admin")
        self.date = fields.Date.today()
        self.invoice_amount = 100000
        self.invoice_tax = 16000
        self.retention_code = "New"
        self.vat_withholding_percentage = 75.0
        self.new_invoice = self.env["account.move"].create({
            'move_type': "out_refund",
            'partner_id': self.partner.id,
            'invoice_date': self.date,
            'date': self.date,
            'amount_tax': self.invoice_tax,
            "invoice_line_ids": [(0, 0, {
                "name": "product that cost %s" % self.invoice_amount,
                "quantity": 1,
                "price_unit": self.invoice_amount,
            })]
        })
        self.new_invoice.write({"state": "posted"})
        self.invoice = self.env["account.move"].create({
            "move_type": "in_invoice",
            "partner_id": self.partner.id,
            "invoice_date": self.date,
            "date": self.date,
            "amount_tax": self.invoice_tax,
            "invoice_line_ids": [(0, 0, {
                "name": "product that cost %s" % self.invoice_amount,
                "quantity": 1,
                "price_unit": self.invoice_amount,
            })]
        })
        self.invoice.write({"state": "posted"})
        self.active_ids = self.invoice.ids
        self.retention_register = self.env[self.modelo].with_context(
            active_model="account.move", active_ids=self.active_ids
        ).create({
            "retention_date": self.date,
            "retention_type": RETENTION_TYPE_IVA,
            "retention_code": self.retention_code,
            "partner_id": self.partner.id,
            "vat_withholding_percentage": self.vat_withholding_percentage,
            "invoice_date": self.date
        })._create_retentions()
        self.retention = self.env["retention"].browse([self.retention_register])

    def test_retention_type(self):
        """Test  when create retention for retention_type
        """
        with self.assertRaises(ValidationError) as raise_exception:
            self.env[self.modelo].with_context(
                active_model="account.move", active_ids=self.active_ids
            ).create({
                "retention_date": self.date,
                "retention_type": RETENTION_TYPE_IVA,
                "retention_code": self.retention_code,
                "partner_id": self.partner.id,
                "vat_withholding_percentage": self.vat_withholding_percentage,
                "invoice_date": self.date
            }).action_create_retention()
        self.assertEqual(
            str(raise_exception.exception),
            _("This type was already generated"),
            msg="Field retention_state is wrong"
        )

    def test_compute_amount_retention(self):
        """Test when create retention calculation of the amount
        """
        self.assertEqual(
            self.retention.amount_tax * self.vat_withholding_percentage / 100,
            self.retention.amount_retention,
            msg="calculation of the retention amount is wrong"
        )

    def test_vat_percentage(self):
        """Test vat_withholding_percentage
        """
        self.active_ids = self.new_invoice.ids
        retention_new = self.env[self.modelo].with_context(
            active_model="account.move", active_ids=self.active_ids
        ).create({
            "retention_code": "01236547895632",
            "retention_date": self.date,
            "retention_type": RETENTION_TYPE_IVA,
            "partner_id": self.partner.id,
            "move_type": self.new_invoice.move_type,
            "vat_withholding_percentage": self.vat_withholding_percentage,
            "invoice_date": self.date
        })._create_retentions()
        retention = self.env["retention"].browse([retention_new])
        self.assertEqual(
            retention.vat_withholding_percentage,
            retention.invoice_id.company_id.vat_withholding_percentage,
            msg="the retention vat withholding percentage is wrong"
        )
       
        self.assertEqual(
            retention.document_type,
            _("C/N"),
            msg=MESSAGE_DOCUMENT_WRONG
        )  
