from odoo import fields, _
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase
from ..tools.constants import MESSAGE_EXCEPTION_NOT_EXECUTE, REF_MAIN_COMPANY, NAME_PRODUCT, RETENTION_TYPE_IVA


class TestAccountMove(TransactionCase):

    def setUp(self):
        super(TestAccountMove, self).setUp()

        self.journal = self.env["account.journal"].create({
            "name": "Journal Customer",
            "type": "sale",
            "code": "12345"
        })
        self.invoice = self.env["account.move"].create({
            "journal_id": self.journal.id
        })

    def test_raise_when_control_number_is_invalid(self):
        """Test raise when save invalid control number
        """
        with self.assertRaises(ValidationError) as raise_exception:
            self.invoice.control_number = "12345"
        self.assertEqual(
            str(raise_exception.exception),
            _("Invalid control number format. Must have at least 6 numbers and a maximum of 9 numbers"),
            msg=MESSAGE_EXCEPTION_NOT_EXECUTE
        )

    def test_assert_when_cancel_invoice(self):
        company = self.env.ref(REF_MAIN_COMPANY)
        default_withholding_journal = self.env.ref("l10n_ve_plusteam.journal_withholding",
                                                   raise_if_not_found=False)
        if default_withholding_journal:
            company.write({
                "withholding_journal_id": default_withholding_journal.id
            })
        partner = self.env.ref("base.partner_admin")
        date = fields.Date.today()
        invoice_amount = 1000000
        invoice_tax = 160000
        tax = self.env["account.tax"].create({
            "name": "Dummy Tax",
            "amount": "16.00",
            "type_tax_use": "purchase",
        })
        invoice = self.env["account.move"].create({
            "move_type": "out_invoice",
            "partner_id": partner.id,
            "invoice_date": date,
            "date": date,
            "amount_tax": invoice_tax,
            "invoice_line_ids": [(0, 0, {
                "name": NAME_PRODUCT % invoice_amount,
                "quantity": 1,
                "price_unit": invoice_amount,

            })]
        })
        invoice.write({"state": "posted"})
        self.env["retention"].create({
            "invoice_id": invoice.id,
            "partner_id": partner.id,
            "move_type": invoice.move_type,
            "retention_type": RETENTION_TYPE_IVA,
            "vat_withholding_percentage": 75.0
        })
        with self.assertRaises(ValidationError) as raise_exception:
            invoice.button_cancel()
        self.assertEqual(
            str(raise_exception.exception),
            _("You cannot cancel an invoice when it has withholding associated with a different status of cancel, "
              "please cancel all withholding first"),
            msg=MESSAGE_EXCEPTION_NOT_EXECUTE
        )

    def test_cancel_invoice_successfully(self):
        company = self.env.ref(REF_MAIN_COMPANY)
        default_withholding_journal = self.env.ref("l10n_ve_plusteam.journal_withholding",
                                                   raise_if_not_found=False)
        if default_withholding_journal:
            company.write({
                "withholding_journal_id": default_withholding_journal.id
            })
        partner = self.env.ref("base.partner_admin")
        date = fields.Date.today()
        invoice_amount = 1000000
        invoice_tax = 160000
        tax = self.env["account.tax"].create({
            "name": "Dummy Tax",
            "amount": "16.00",
            "type_tax_use": "purchase",
        })
        invoice = self.env["account.move"].create({
            "move_type": "out_invoice",
            "partner_id": partner.id,
            "invoice_date": date,
            "date": date,
            "amount_tax": invoice_tax,
            "invoice_line_ids": [(0, 0, {
                "name": NAME_PRODUCT % invoice_amount,
                "quantity": 1,
                "price_unit": invoice_amount,

            })]
        })
        invoice.write({"state": "posted"})
        retention = self.env["retention"].create({
            "invoice_id": invoice.id,
            "partner_id": partner.id,
            "move_type": invoice.move_type,
            "retention_type": RETENTION_TYPE_IVA,
            "vat_withholding_percentage": 75.0
        })
        retention.button_cancel()
        invoice.button_cancel()
        self.assertEqual(retention.state, "cancel", msg="")
        self.assertEqual(invoice.state, "cancel", msg="")
