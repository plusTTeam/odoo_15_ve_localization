from odoo import models, fields, api


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    igtf = fields.Boolean(string="IGTF", default=False, readonly=False)
    igtf_amount = fields.Monetary(string="IGTF Amount", currency_field="currency_id",
                                  compute="_compute_igtf_amount", readonly=True, store=True)

    @api.depends("amount", "company_id", "igtf")
    def _compute_igtf_amount(self):
        for record in self:
            igtf_amount = 0
            if record.igtf is not False and record.payment_type == "outbound":
                igtf_amount = record.amount * (record.company_id.igtf / 100)
            record.igtf_amount = igtf_amount

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
