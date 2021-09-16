
from odoo import _
from odoo.tests.common import TransactionCase, Form
from odoo.exceptions import ValidationError
from ..tools.constants import MESSAGE_EXCEPTION_NOT_EXECUTE


class TestResPartner(TransactionCase):

    def setUp(self):
        super(TestResPartner, self).setUp()

        self.account_type_receivable_id = self.env["account.account.type"].search([("id", "=", 1)], limit=1).id
        self.account_type_payable_id = self.env["account.account.type"].search([("id", "=", 2)], limit=1).id
        self.account_receivable = self.env["account.account"].create({
            "code": "11111",
            "name": "Cuenta por cobrar",
            "user_type_id": self.account_type_receivable_id,
            "reconcile": True
        })
        self.account_payable = self.env["account.account"].create({
            "code": "222222",
            "name": "Cuenta por pagar",
            "user_type_id": self.account_type_payable_id,
            "reconcile": True
        })
        self.contact = self.env["res.partner"].create({
            "name": "New User",
            "vat": "J123456789",
            "taxpayer": True,
            "special_taxpayer": True,
            "property_account_receivable_id": self.account_receivable.id,
            "property_account_payable_id": self.account_payable.id
        })

    def test_raise_when_rif_is_invalid(self):
        """Test raise when save invalid RIF
        """
        with self.assertRaises(ValidationError) as raise_exception:
            self.contact.vat = "V12345678912"
        self.assertEqual(
            str(raise_exception.exception),
            _("The RIF/Identification Card format is invalid. "
              "Must start with a letter (V, J, E, P) followed by 7 or 9 numbers"),
            msg=MESSAGE_EXCEPTION_NOT_EXECUTE
        )

    def test_onchange_taxpayer_field(self):
        """Test that the special_taxpayer change
        """
        with Form(self.contact) as contact:
            contact.taxpayer = False
        self.assertFalse(contact.special_taxpayer, msg="The special_taxpayer field don't change")

    def test_raise_when_vat_withholding_percentage_is_out_range(self):
        """Test raise when the vat_withholding_percentage field
        is out of range
        """
        with self.assertRaises(ValidationError) as raise_exception:
            self.contact.vat_withholding_percentage = 150.00
        self.assertEqual(
            str(raise_exception.exception),
            _("The retention percentage must be between the the values 0 and 100, "
              "please verify that the value is in this range"),
            msg=MESSAGE_EXCEPTION_NOT_EXECUTE
        )
        with self.assertRaises(ValidationError) as raise_exception:
            self.contact.vat_withholding_percentage = -150.00
        self.assertEqual(
            str(raise_exception.exception),
            _("The retention percentage must be between the the values 0 and 100, "
              "please verify that the value is in this range"),
            msg=MESSAGE_EXCEPTION_NOT_EXECUTE
        )
