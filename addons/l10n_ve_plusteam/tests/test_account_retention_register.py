from odoo import fields, _
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase, Form
from ..tools.constants import RETENTION_TYPE_ISLR, RETENTION_TYPE_IVA


class TestAccountRetentionRegister(TransactionCase):

    def setUp(self):
        super(TestAccountRetentionRegister, self).setUp()

        self.partner = self.env.ref("base.partner_admin")
        self.date = fields.Date.today()
        self.invoice_amount = 100000
        self.invoice_tax = 16000
        self.retention_code = "New"
        self.retention_type = RETENTION_TYPE_IVA
        self.vat_withholding_percentage = 75.0
        self.month_fiscal_period = "0" + str(self.date.month)
        self.year_fiscal_period = str(self.date.year)

        self.invoice = self.env["account.move"].create({
            "move_type": "out_invoice",
            "partner_id": self.partner.id,
            "invoice_date": self.date,
            "date": self.date,
            "retention_state": "with_retention_iva",
            "amount_tax": self.invoice_tax
        })
        self.invoice.write({"state": "posted"})

        self.active_ids = self.invoice.ids

        self.retention_register = self.env["account.retention.register"].with_context(
            active_model="account.move", active_ids=self.active_ids
        ).create({
            "retention_date": self.date,
            "retention_type": self.retention_type,
            "retention_code": self.retention_code,
            "partner_id": self.partner.id,
            "vat_withholding_percentage": self.vat_withholding_percentage,
            "invoice_date": self.date,
            "month_fiscal_period": self.month_fiscal_period
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
                "retention_type": self.retention_type,
                "retention_code": self.retention_code,
                "partner_id": self.partner.id,
                "vat_withholding_percentage": self.vat_withholding_percentage,
                "invoice_date": self.date,
                "month_fiscal_period": self.month_fiscal_period
            })._create_retentions()
        self.assertEqual(
            str(raise_exception.exception),
            _("This type was already generated"),
            msg="Field retention_state is wrong"
        )

    def test_compute_amount_retention(self):
        """Test when create retention calculation of the amount
        """
        self.assertEqual(
            self.invoice.amount_tax * self.vat_withholding_percentage / 100,
            self.retention.amount_retention,
            msg="calculation of the retention amount is wrong"
        )

    def test_month_fiscal_char(self):
        self.assertEqual(
            self.retention.month_fiscal_period,
            "0" + str(self.date.month),
            msg="Field month fiscal period is wrong"
        )
