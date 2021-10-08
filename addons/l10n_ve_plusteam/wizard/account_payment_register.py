from odoo import models, fields, api


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    igtf = fields.Boolean(string="IGTF", default=False, readonly=False)
    igtf_amount = fields.Monetary(string="IGTF Amount", currency_field="currency_id",
                                  compute="_compute_igtf_amount", readonly=True, store=True)
    hide_igtf = fields.Boolean(string="Hide IGTF", compute="_compute_hide_igtf")

    @api.depends("amount", "hide_igtf", "igtf")
    def _compute_igtf_amount(self):
        for record in self:
            igtf_amount = 0
            if record.igtf and record.hide_igtf is False:
                igtf_amount = record.amount * (record.company_id.igtf / 100)
            record.igtf_amount = igtf_amount

    @api.depends("journal_id.type", "company_id.igtf", "payment_type")
    def _compute_hide_igtf(self):
        for record in self:
            hide = record.payment_type != "outbound" or record.journal_id.type != "bank" or \
                   record.company_id.igtf <= 0.00
            record.hide_igtf = hide

    def _create_payment_vals_from_wizard(self):
        value = super(AccountPaymentRegister, self)._create_payment_vals_from_wizard()
        value["igtf"] = self.igtf
        value["igtf_amount"] = self.igtf_amount
        return value

    def _create_payment_vals_from_batch(self, batch_result):
        value = super(AccountPaymentRegister, self)._create_payment_vals_from_batch(batch_result)
        value["igtf"] = self.igtf
        value["igtf_amount"] = self.igtf_amount
        return value
