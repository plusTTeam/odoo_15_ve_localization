
from odoo import _
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from ..tools.constants import REF_MAIN_COMPANY


class TestResCompany(TransactionCase):

    def setUp(self):
        super(TestResCompany, self).setUp()

        self.company = self.env.ref(REF_MAIN_COMPANY)

    def test_raise_when_vat_withholding_percentage_is_out_range(self):
        with self.assertRaises(ValidationError) as raise_exception:
            self.company.vat_withholding_percentage = 150.00
        self.assertEqual(
            str(raise_exception.exception),
            _("The retention percentage must be between 0 and 100, "
              "please verify that the value is in this range"),
            msg="The exception was not executed correctly"
        )
        with self.assertRaises(ValidationError) as raise_exception:
            self.company.vat_withholding_percentage = -150.00
        self.assertEqual(
            str(raise_exception.exception),
            _("The retention percentage must be between 0 and 100, "
              "please verify that the value is in this range"),
            msg="The exception was not executed correctly"
        )
