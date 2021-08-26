from odoo import _
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase
from ..tools.constants import MESSAGE_EXCEPTION_NOT_EXECUTE


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
            _("Invalid control number format. Must have at least 6 numbers"),
            msg=MESSAGE_EXCEPTION_NOT_EXECUTE
        )
