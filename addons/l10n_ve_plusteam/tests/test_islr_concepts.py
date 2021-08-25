
from odoo.tests.common import TransactionCase


class TestISLRConcepts(TransactionCase):

    def setUp(self):
        super(TestISLRConcepts, self).setUp()

        self.concept = self.env.ref("l10n_ve_plusteam.concept_0")

    def test_complete_name(self):
        self.assertEqual(
            self.concept.complete_name_with_code,
            f'[{self.concept.code}] {self.concept.name}',
            msg="Field complete_name_with_code is wrong"
        )
