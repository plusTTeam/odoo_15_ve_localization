
from odoo import fields
from odoo.tests.common import TransactionCase


class TestTaxUnit(TransactionCase):

    def setUp(self):
        super(TestTaxUnit, self).setUp()

        self.tax_unit = self.env["tax.unit"].create({
            "date": fields.Date.today(),
            "gazette": "321654",
            "publication_date": fields.Date.today(),
            "value": 2000.00
        })

    def test_complete_name(self):
        self.assertEqual(
            self.tax_unit.complete_name_with_code,
            f"Gaceta Nro. {self.tax_unit.gazette}",
            msg="Field complete_name_with_code is wrong"
        )
