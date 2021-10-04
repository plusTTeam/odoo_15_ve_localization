from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    igtf = fields.Boolean(string="IGTF", default=False)
    igtf_amount = fields.Monetary(string="IGTF Amount", currency_field="currency_id",
                                  compute="_compute_igtf_amount", store=True)
    igtf_move_id = fields.Many2one("account.move", string="IGTF Account Move")
    hide_igtf = fields.Boolean(string="Hide IGTF", compute="_compute_hide_igtf")

    @api.depends("amount", "hide_igtf", "igtf")
    def _compute_igtf_amount(self):
        for record in self:
            igtf_amount = 0
            if record.igtf and record.hide_igtf is False and record.state == "draft":
                igtf_amount = record.amount * (record.company_id.igtf / 100)
            record.igtf_amount = igtf_amount

    @api.depends("journal_id.type", "company_id.igtf", "payment_type")
    def _compute_hide_igtf(self):
        for record in self:
            hide = record.payment_type != "outbound" or record.journal_id.type != "bank" or \
                   record.company_id.igtf <= 0.00
            record.hide_igtf = hide

    @api.model_create_multi
    def create(self, values):
        payments = super(AccountPayment, self).create(values)
        for payment in payments:
            create_igtf_move = payment.igtf is not False and payment.igtf_amount != 0.0 and \
                               payment.payment_type == "outbound"
            if create_igtf_move:
                igtf_account = payment.company_id.igtf_account_id
                if not igtf_account:
                    raise ValidationError(
                        _("There is not accounting account for the Tax on Big Financial Transactions (IGTF), "
                          "please go to Settings and select an account to apply this tax")
                    )
                igtf_journal = payment.company_id.igtf_journal_id
                if not igtf_journal:
                    raise ValidationError(
                        _("There is not journal for the Tax on Big Financial Transactions (IGTF), "
                          "please go to Settings and select an journal to apply this tax")
                    )
                move_lines = payment.move_id.line_ids
                counterpart_amount = -payment.igtf_amount
                balance = payment.currency_id._convert(counterpart_amount, payment.company_id.currency_id,
                                                       payment.company_id, payment.date)
                lines = {
                    "name": _("IGTF for payment %s", payment.name),
                    "date_maturity": payment.date,
                    "amount_currency": -counterpart_amount,
                    "currency_id": payment.currency_id.id,
                    "debit": 0.0,
                    "credit": abs(balance),
                    "partner_id": payment.partner_id.id,
                    "account_id": move_lines[0].account_id.id
                }, {
                    "name": _("IGTF for payment %s", payment.name),
                    "date_maturity": payment.date,
                    "amount_currency": counterpart_amount,
                    "currency_id": payment.currency_id.id,
                    "debit": abs(balance),
                    "credit": 0.0,
                    "partner_id": payment.partner_id.id,
                    "account_id": igtf_account.id
                }
                move = self.env["account.move"].create({
                    "move_type": "entry",
                    "partner_id": payment.partner_id.id,
                    "journal_id": igtf_journal.id,
                    "date": payment.date,
                    "ref": payment.ref
                })
                move.write({"line_ids": [(0, 0, line) for line in lines]})
                payment.write({"igtf_move_id": move.id})
        return payments

    def action_post(self):
        super(AccountPayment, self).action_post()
        self.igtf_move_id.write({"state": "posted"})
