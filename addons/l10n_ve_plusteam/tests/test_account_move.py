from odoo import fields, _
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase
from .common import AccountMoveModelRetentionTestingCommon
from ..tools.constants import MESSAGE_EXCEPTION_NOT_EXECUTE, REF_MAIN_COMPANY, NAME_PRODUCT, RETENTION_TYPE_IVA


class TestAccountMove(AccountMoveModelRetentionTestingCommon):

    def setUp(self):
        super(TestAccountMove, self).setUp()
        self.journal = self.env["account.journal"].create({
            "name": "Journal Customer",
            "type": "sale",
            "code": "12345"
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
        with self.assertRaises(ValidationError) as raise_exception:
            self.invoice.button_cancel()
        self.assertEqual(
            str(raise_exception.exception),
            _("You cannot cancel an invoice when it has withholding associated with a different status of cancel, "
              "please cancel all withholding first"),
            msg=MESSAGE_EXCEPTION_NOT_EXECUTE
        )

    def test_cancel_invoice_successfully(self):
        self.retention.button_cancel()
        self.invoice.button_cancel()
        self.assertEqual(self.retention.state, "cancel", msg="")
        self.assertEqual(self.invoice.state, "cancel", msg="")
