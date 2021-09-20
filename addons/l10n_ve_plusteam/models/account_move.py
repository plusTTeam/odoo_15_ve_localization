# -*- coding: utf-8 -*-

import re
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    control_number = fields.Char(string="Control Number")
    form_number = fields.Char(string="form number", help="Import form number C-80 or C-81")
    file_number = fields.Char(string="file number", help="Import file number")
    import_doc = fields.Boolean(string="Import")
    document_number = fields.Char(string="Document Number", help="Is defined when it is a supplier invoice")
    fiscal_printing_serial = fields.Char(
        string="Fiscal Printing Serial",
        help="Defined when the invoice is printed to the customer"
    )
    amount_base_taxed = fields.Monetary(string="Amount Base taxed", store=True, readonly=True, tracking=True,
                                        compute="_compute_amount_base_tax")
    retention_id = fields.One2many("retention", "invoice_id", string="Retention", copy=False, check_company=True)
    retention_state = fields.Selection(selection=[
        ("with_retention_iva", "With Retention IVA"),
        ("with_retention_islr", "With Retention ISLR"),
        ("with_retention_both", "With Retention Both"),
        ("without_retention", "Without Retention")],
        string="Retention Status", store=True, readonly=True, copy=False, tracking=True, default="without_retention")

    @api.constrains("control_number")
    def _check_control_number(self):
        for record in self:
            if record.control_number and re.match(r"^[0-9]{6,9}$", record.control_number) is None:
                raise ValidationError(
                    _("Invalid control number format. Must have at least 6 numbers and a maximum of 9 numbers"))

    def button_cancel(self):
        cancel = True
        for retention in self.retention_id:
            if retention.state != "cancel":
                cancel = False
        if cancel:
            super(AccountMove, self).button_cancel()
        else:
            raise ValidationError(_("You cannot cancel an invoice when it has withholding associated with "
                                    "a different status of cancel, please cancel all withholding first"))

    @api.depends("line_ids.currency_id", "line_ids.amount_currency")
    def _compute_amount_base_tax(self):
        for move in self:
            total_base_taxed = 0.0
            total_base_taxed_currency = 0.0
            currencies = move._get_lines_onchange_currency().currency_id
            for line in move.line_ids:
                if move.is_invoice(
                        include_receipts=True) and not line.exclude_from_invoice_tab and line.tax_ids.amount > 0:
                    total_base_taxed += line.balance
                    total_base_taxed_currency += line.amount_currency
            if move.move_type == "entry" or move.is_outbound():
                sign = 1
            else:
                sign = -1
            move.amount_base_taxed = sign * (total_base_taxed_currency if len(currencies) == 1 else total_base_taxed)

    def action_register_retention(self):
        """ Open the retention.register wizard to retention the selected journal entries.
        :return: An action opening the retention.register wizard.
        """
        return {
            "name": _("Register Retention"),
            "res_model": "account.retention.register",
            "view_mode": "form",
            "context": {
                "active_model": "account.move",
                "active_ids": self.ids,
            },
            "target": "new",
            "type": "ir.actions.act_window",
        }
