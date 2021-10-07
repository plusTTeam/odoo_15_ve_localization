from odoo import fields
from odoo.tests.common import TransactionCase
from ..tools.constants import RETENTION_TYPE_IVA, REF_MAIN_COMPANY, NAME_PRODUCT


class AccountMoveModelRetentionTestingCommon(TransactionCase):

    def setUp(self):
        super(AccountMoveModelRetentionTestingCommon, self).setUp()
        
        self.company = self.env.ref(REF_MAIN_COMPANY)
        self.default_withholding_journal = self.env.ref("l10n_ve_plusteam.journal_withholding",
                                                        raise_if_not_found=False)
        if self.default_withholding_journal:
            self.company.write({
                "withholding_journal_id": self.default_withholding_journal.id
            })
        self.partner = self.env.ref("base.partner_admin")
        self.date = fields.Date.today()
        self.invoice_amount = 1000000
        self.invoice_tax = 160000
        self.invoice = self.env["account.move"].create({
            "move_type": "out_invoice",
            "partner_id": self.partner.id,
            "invoice_date": self.date,
            "date": self.date,
            "retention_state": "with_retention_iva",
            "amount_tax": self.invoice_tax,
            "invoice_line_ids": [(0, 0, {
                "name": NAME_PRODUCT % self.invoice_amount,
                "quantity": 1,
                "price_unit": self.invoice_amount,

            })]
        })
        self.invoice.write({"state": "posted"})
        self.retention = self.env["retention"].create({
            "invoice_id": self.invoice.id,
            "partner_id": self.partner.id,
            "move_type": self.invoice.move_type,
            "retention_type": RETENTION_TYPE_IVA,
            "vat_withholding_percentage": 75.0
        })
