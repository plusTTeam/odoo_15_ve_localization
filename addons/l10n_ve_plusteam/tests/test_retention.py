from odoo import _
from odoo.exceptions import ValidationError
from odoo.tests.common import Form
from .common import AccountMoveModelRetentionTestingCommon
from ..tools.constants import (RETENTION_TYPE_ISLR, RETENTION_TYPE_IVA, NAME_PRODUCT,
                               MESSAGE_EXCEPTION_NOT_EXECUTE)


class TestRetention(AccountMoveModelRetentionTestingCommon):

    def test_retention_type(self):
        """Test  when create retention for retention_type
        """
        with self.assertRaises(ValidationError) as raise_exception:
            self.env["retention"].create({
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

    def test_onchange_value_withholding(self):
        """Test  when onchange_value_withholding porcentage
        """
        with Form(self.retention) as retention:
            retention.vat_withholding_percentage = 100
        self.assertEqual(
            self.retention.amount_tax * retention.vat_withholding_percentage / 100,
            self.retention.amount_retention,
            msg="calculation of the retention amount is wrong"
        )

    def test_destination_account_id(self):
        retention_account = self.retention._get_destination_account_id()
        self.assertEqual(self.retention.destination_account_id.id, retention_account,
                         msg="The destination account was not configured correctly")

    def test_move_lines_creations(self):
        receivable_payable_account = self.retention.move_id.line_ids.search(
            [("account_id.internal_type", "in", ("receivable", "payable"))])
        self.assertTrue(receivable_payable_account,
                        msg="There are no accounting entries for account payable or receivable")
        self.assertTrue(len(self.retention.move_id.line_ids), msg="the account movements were not created")

    def test_month_fiscal_char(self):
        month = self.retention.retention_date.strftime("%m")
        self.assertEqual(
            self.retention.month_fiscal_period,
            month,
            msg="Field month fiscal period is wrong"
        )

    def test_type_document(self):
        self.assertEqual(
            self.retention.document_type,
            _("Invoice"),
            msg="Field type document is wrong"
        )

    def test_retention_type_other(self):
        """Test  when create retention for retention_type
        """
        with Form(self.retention) as retention:
            retention.retention_type = RETENTION_TYPE_ISLR
            retention.invoice_id.write({"retention_state": "with_both_retentions"})
        self.assertEqual(
            self.invoice.retention_state,
            "with_both_retentions",
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
            _("The retention percentage must be between 1 and 100, "
              "please verify that the value is in this range"),
            msg="Field withholding percentage is wrong"
        )

    def test_complete_name(self):
        self.assertEqual(
            self.retention.complete_name_with_code,
            f"[{self.retention.retention_code}] {self.retention.original_document_number}",
            msg="Field complete_name_with_code is wrong"
        )

    def test_get_default_journal(self):
        new_invoice = self.env["account.move"].create({
            "move_type": "in_invoice",
            "partner_id": self.partner.id,
            "invoice_date": self.date,
            "date": self.date,
            "retention_state": "with_retention_iva",
            "amount_tax": self.invoice_tax,
            "invoice_line_ids": [(0, 0, {
                "name": NAME_PRODUCT % self.invoice_amount,
                "quantity": 1,
                "price_unit": self.invoice_amount
            })]
        })
        new_invoice.action_post()
        default_journal = self.env["account.journal"].create({
            "name": "New Journal",
            "type": "general",
            "code": "RT"
        })
        new_retention = self.env["retention"].with_context(default_journal_id=default_journal.id).create({
            "invoice_id": new_invoice.id,
            "partner_id": self.partner.id,
            "move_type": new_invoice.move_type,
            "retention_type": RETENTION_TYPE_IVA,
            "vat_withholding_percentage": 75.0
        })
        self.assertEqual(new_retention.move_id.journal_id.id, default_journal.id,
                         msg="The journal selected was not the default_journal_id")

    def test_raise_when_journal_is_not_found(self):
        self.env.company.write({"withholding_journal_id": False})
        if self.default_withholding_journal:
            self.default_withholding_journal.write({
                "active": False
            })
        new_invoice = self.env["account.move"].create({
            "move_type": "in_invoice",
            "partner_id": self.partner.id,
            "invoice_date": self.date,
            "date": self.date,
            "retention_state": "with_retention_iva",
            "amount_tax": self.invoice_tax,
            "invoice_line_ids": [(0, 0, {
                "name": NAME_PRODUCT % self.invoice_amount,
                "quantity": 1,
                "price_unit": self.invoice_amount
            })]
        })
        with self.assertRaises(ValidationError) as raise_exception:
            self.env["retention"].create({
                "invoice_id": new_invoice.id,
                "partner_id": self.partner.id,
                "move_type": new_invoice.move_type,
                "retention_type": RETENTION_TYPE_IVA,
                "vat_withholding_percentage": 75.0
            })
        self.assertEqual(str(raise_exception.exception),
                         _("The company does not have a journal configured for withholding, "
                           "please go to the configuration section to add one"),
                         msg="There is a journal configured")

    def test_check_move_type(self):
        entry = self.env["account.move"].create({
            "move_type": "entry",
            "partner_id": self.partner.id,
            "date": self.date,
            "retention_state": "with_both_retentions"
        })
        with self.assertRaises(ValidationError) as raise_exception:
            self.env["retention"].create({
                "invoice_id": entry.id,
                "partner_id": self.partner.id,
                "move_type": entry.move_type,
                "retention_type": RETENTION_TYPE_IVA,
                "vat_withholding_percentage": 75.0
            })
        self.assertEqual(str(raise_exception.exception),
                         _("You are trying to create a withholding from an illegal journal entry type (%s)",
                           entry.move_type),
                         msg=MESSAGE_EXCEPTION_NOT_EXECUTE)

    def test_get_original_journal(self):
        self.env.company.write({"withholding_journal_id": False})
        new_invoice = self.env["account.move"].create({
            "move_type": "in_invoice",
            "partner_id": self.partner.id,
            "invoice_date": self.date,
            "date": self.date,
            "retention_state": "with_retention_iva",
            "amount_tax": self.invoice_tax,
            "invoice_line_ids": [(0, 0, {
                "name": NAME_PRODUCT % self.invoice_amount,
                "quantity": 1,
                "price_unit": self.invoice_amount
            })]
        })
        new_invoice.action_post()
        new_retention = self.env["retention"].create({
            "invoice_id": new_invoice.id,
            "partner_id": self.partner.id,
            "move_type": new_invoice.move_type,
            "retention_type": RETENTION_TYPE_IVA,
            "vat_withholding_percentage": 75.0
        })
        self.assertEqual(new_retention.move_id.journal_id.id, self.default_withholding_journal.id,
                         msg="The journal was not the original journal")

    def test_cancel_withholding(self):
        self.retention.button_cancel()

        self.assertEqual(self.retention.state, "cancel", msg="Withholding status was unchanged")
        self.assertEqual(self.retention.move_id.state, "cancel", msg="Withholding status was unchanged")

    def test_reconcile_lines(self):
        new_invoice = self.env["account.move"].create({
            "move_type": "in_invoice",
            "partner_id": self.partner.id,
            "invoice_date": self.date,
            "date": self.date,
            "amount_tax": self.invoice_tax,
            "invoice_line_ids": [(0, 0, {
                "name": NAME_PRODUCT % self.invoice_amount,
                "quantity": 1,
                "price_unit": self.invoice_amount
            })]
        })
        new_invoice.action_post()
        new_retention = self.env["retention"].create({
            "invoice_id": new_invoice.id,
            "partner_id": self.partner.id,
            "move_type": new_invoice.move_type,
            "retention_type": RETENTION_TYPE_IVA,
            "vat_withholding_percentage": 75.0
        })
        domain = [('account_internal_type', 'in', ('receivable', 'payable')), ('matching_number', '!=', False)]
        invoice_lines = new_invoice.line_ids.search(domain)
        retention_lines = new_retention.move_id.line_ids.search(domain)
        for invoice_line, retention_line in zip(invoice_lines, retention_lines):
            match = invoice_line.matching_number == retention_line.matching_number and \
                retention_line.matching_number
            self.assertTrue(match, msg="The moves are not reconciled")
