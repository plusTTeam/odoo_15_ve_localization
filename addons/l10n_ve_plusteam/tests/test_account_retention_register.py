from odoo import fields, _
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase, Form
from ..tools.constants import RETENTION_TYPE_IVA, REF_MAIN_COMPANY


class TestAccountRetentionRegister(TransactionCase):

    def setUp(self):
        super(TestAccountRetentionRegister, self).setUp()

        self.vat_withholding_percentage = 75.0
        self.partner = self.env.ref("base.partner_admin")
        self.partner.write({
            "vat_withholding_percentage": self.vat_withholding_percentage
        })
        self.date = fields.Date.today()
        self.invoice_amount = 100000
        self.invoice_tax = 16000
        self.retention_code = "New"
        
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
        self.retention_register = self.env["account.retention.register"].with_context(
            active_model="account.move", active_ids=self.active_ids
        ).create({
            "retention_date": self.date,
            "retention_type": RETENTION_TYPE_IVA,
            "retention_code": self.retention_code,
            "partner_id": self.partner.id,
            "vat_withholding_percentage": self.vat_withholding_percentage
        })._create_retentions()
        self.retention = self.env["retention"].browse([self.retention_register])

    def test_retention_type(self):
        """Test  when create retention for retention_type
        """
        with self.assertRaises(ValidationError) as raise_exception:
            self.env["account.retention.register"].with_context(
                active_model="account.move", active_ids=self.active_ids
            ).create({
                "retention_date": self.date,
                "retention_type": RETENTION_TYPE_IVA,
                "retention_code": self.retention_code,
                "partner_id": self.partner.id,
                "vat_withholding_percentage": self.vat_withholding_percentage
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

    def test_vat_percentage_from_sale(self):
        """Test vat_withholding_percentage
        """
        new_vat_percentage = 100.0
        company = self.env.ref(REF_MAIN_COMPANY)
        company.write({
            "vat_withholding_percentage": new_vat_percentage
        })
        invoice_out_invoice = self.env["account.move"].create({
            "move_type": "out_invoice",
            "partner_id": self.partner.id,
            "invoice_date": self.date,
            "date": self.date,
            "amount_tax": self.invoice_tax,
            "invoice_line_ids": [(0, 0, {
                "name": "product" ,
                "quantity": 1,
                "price_unit": self.invoice_amount
            })]
        })
        invoice_out_invoice.write({"state": "posted"})
        active_ids = invoice_out_invoice.ids
        with Form(self.env["account.retention.register"].with_context(
                active_model="account.move", active_ids=active_ids
            )) as retention_register:
            retention_register.retention_date = self.date
            retention_register.retention_type = RETENTION_TYPE_IVA
            retention_register.retention_code = "20211209876543"

        self.assertEqual(
            retention_register.vat_withholding_percentage,
            company.vat_withholding_percentage,
            msg="the retention vat withholding percentage is wrong"
        )

    def test_vat_percentage_from_Purchase(self):
        """Test vat_withholding_percentage Purchase
        """
        invoice_in_invoice = self.env["account.move"].create({
            "move_type": "in_invoice",
            "partner_id": self.partner.id,
            "invoice_date": self.date,
            "date": self.date,
            "amount_tax": self.invoice_tax,
            "invoice_line_ids": [(0, 0, {
                "name": "product2 that cost %s" % self.invoice_amount,
                "quantity": 1,
                "price_unit": self.invoice_amount
            })]
        })
        invoice_in_invoice.write({"state": "posted"})
        active_ids = invoice_in_invoice.ids
        with Form(self.env["account.retention.register"].with_context(
                active_model="account.move", active_ids=active_ids
            )) as retention_register:
            retention_register.retention_date = self.date
            retention_register.retention_type = RETENTION_TYPE_IVA

        self.assertEqual(
            retention_register.vat_withholding_percentage,
            self.partner.vat_withholding_percentage,
            msg="the retention vat withholding percentage is wrong"
        )