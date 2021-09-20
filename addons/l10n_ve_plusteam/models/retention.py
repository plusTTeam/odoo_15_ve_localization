# -*- coding: utf-8 -*-

import re
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Retention(models.Model):
    _name = "retention"
    _description = "Retention"
    _inherits = {'account.move': 'move_id'}
    _rec_name = "complete_name_with_code"

    today = fields.Date.today()
    complete_name_with_code = fields.Char(string="Complete Name with Code", compute="_compute_complete_name_with_code",
                                          store=True)
    move_type = fields.Selection(selection=[
        ("entry", "Journal Entry"),
        ("out_invoice", "Customer Invoice"),
        ("out_refund", "Customer Credit Note"),
        ("in_invoice", "Vendor Bill"),
        ("in_refund", "Vendor Credit Note"),
    ], string="Type", required=True, store=True, index=True, readonly=True, tracking=True,
        default="entry", change_default=True, related="invoice_number.move_type")

    move_id = fields.Many2one(
        comodel_name="account.move", string="Journal Entry", required=True, readonly=True, ondelete="cascade",
        check_company=True)
    code = fields.Char(string="Retention Number", default=_("New"), store=True)
    date = fields.Date(string="Date", required=True, default=fields.Date.context_today)
    receipt_date = fields.Date(string="Receipt Date", required=True, default=fields.Date.context_today)
    month_fiscal_period = fields.Char(string="Month", compute="_compute_month_fiscal_char", store=True, readonly=False)
    year_fiscal_period = fields.Char(string="Year", default=str(today.year))
    is_iva = fields.Boolean(string="Is IVA", default=False,
                            help="Check if the retention is a iva, otherwise it is islr")
    retention_type = fields.Selection(string="Retention Type",
                                      selection=[("iva", "IVA"), ("islr", "ISLR")],
                                      compute="_compute_retention_type", inverse="_write_retention_type", default="iva")
    destination_account_id = fields.Many2one(comodel_name="account.account", string="Destination Account", store=True,
                                             readonly=False, check_company=True)
    state = fields.Selection(selection=[
        ("draft", "Draft"),
        ("posted", "Posted"),
        ("cancel", "Cancelled"),
    ], string="Status", required=True, readonly=True, copy=False, tracking=True,
        default="draft")
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 store=True, readonly=True,
                                 compute="_compute_company_id")

    partner_id = fields.Many2one("res.partner", string="Customer/Vendor", domain="[('parent_id','=', False)]",
                                 check_company=True)
    rif = fields.Char(string="RIF", related="partner_id.vat")
    vat_withholding_percentage = fields.Float(string="vat withholding percentage", store=True, readonly=False,
                                              compute="_compute_vat_percentage", required=True)
    invoice_number = fields.Many2one("account.move", string="Invoice Number", required=True,
                                     domain="[('move_type', 'in', ('out_invoice', 'in_invoice', 'in_refund', "
                                            "'out_refund')), ('retention_state', '!=', 'with_retention_both'),"
                                            "('state', '=', 'posted'),('partner_id', '=', partner_id )]")                                     
    original_document_number = fields.Char(string="Original Document Number", related="invoice_number.document_number")                                        
    invoice_date = fields.Date(string="Invoice Date", required=True, related="invoice_number.date")
    type_document = fields.Char(string="Type Document", compute="_compute_type_document")
    control_number = fields.Char(string="Control Number", related="invoice_number.control_number")
    ref = fields.Char(string="Reference", related="invoice_number.ref")
    company_currency_id = fields.Many2one(related="invoice_number.company_currency_id", string="Company Currency",
                                          readonly=True, help="Utility field to express amount currency")
    currency_id = fields.Many2one(related="invoice_number.currency_id", string="Currency", readonly=True,
                                  help="Invoice currency")
    amount_tax = fields.Monetary(string="Amount tax", related="invoice_number.amount_tax",
                                 currency_field="company_currency_id")
    amount_untaxed = fields.Monetary(string="Amount untaxed", related="invoice_number.amount_untaxed",
                                     currency_field="company_currency_id")
    amount_total = fields.Monetary(string="Amount total", related="invoice_number.amount_total",
                                   currency_field="company_currency_id")
    amount_base_taxed = fields.Monetary(string="Amount base taxed", related="invoice_number.amount_base_taxed",
                                        currency_field="company_currency_id")
    amount_retention = fields.Monetary(string="Amount Retention", compute="_compute_amount_retention",
                                       currency_field="company_currency_id")
    amount_base_untaxed = fields.Monetary(string="Amount base untaxed", compute="_compute_amount_base_untaxed",
                                          currency_field="company_currency_id")

    @api.constrains("partner_id")
    def _check_partner_id(self):
        for record in self:
            if record.partner_id != record.invoice_number.partner_id:
                raise ValidationError(
                    _("The selected contact is different from the invoice contact, "
                      "they must be the same, please correct it")
                )

    @api.constrains("vat_withholding_percentage")
    def _check_vat_withholding_percentage(self):
        for record in self:
            if record.vat_withholding_percentage <= 0 or record.vat_withholding_percentage > 100:
                raise ValidationError(
                    _("The retention percentage must be between the values 1 and 100, "
                      "please verify that the value is in this range")
                )

    @api.constrains("retention_type")
    def _check_retention_type(self):
        created = False
        retentions = self.read_group([("retention_type", "=", "iva")], ["invoice_number"], ["invoice_number"])
        for retention in retentions:
            if retention.get('invoice_number_count', 0) > 1:
                created = True
        retentions = self.read_group([("retention_type", "=", "islr")], ["invoice_number"], ["invoice_number"])
        for retention in retentions:
            if retention.get('invoice_number_count', 0) > 1:
                created = True
        if created:
            raise ValidationError(_("This type was already generated"))

    @api.constrains('code','move_type')
    def _check_receipt_number(self):
        for record in self:
            if record.code and re.match(r"^[0-9]{14,14}$", record.code) is None and record.move_type in ("out_invoice","out_refund"):
                raise ValidationError(
                    _("Invalid receipt number format. Must have at least 14 numbers"))

    @api.depends("partner_id")
    def _compute_company_id(self):
        for retention in self:
            retention.company_id = retention.partner_id.company_id or retention.company_id or self.env.company

    @api.depends("move_type")
    def _compute_vat_percentage(self):
        for retention in self:
            if retention.move_type in ("in_invoice","in_refund"):
                retention.vat_withholding_percentage = retention.partner_id.vat_withholding_percentage
            else:
                retention.vat_withholding_percentage = retention.company_id.vat_withholding_percentage

    @api.depends(
        "vat_withholding_percentage",
        "amount_tax")
    def _compute_amount_retention(self):
        for retention in self:
            amount_retention = retention.amount_tax * retention.vat_withholding_percentage / 100
            retention.amount_retention = amount_retention

    @api.depends("amount_untaxed")
    def _compute_amount_base_untaxed(self):
        for retention in self:
            retention.amount_base_untaxed = retention.amount_untaxed - retention.amount_base_taxed

    @api.onchange("vat_withholding_percentage")
    def _onchange_value_withholding_percentage(self):
        for retention in self:
            retention.amount_retention = retention.amount_tax * retention.vat_withholding_percentage / 100

    @api.depends("date")
    def _compute_month_fiscal_char(self):
        for retention in self:
            month_char = str(retention.date.month)
            if len(month_char) == 1:
                month_char = "0" + str(retention.date.month)
            retention.month_fiscal_period = month_char

    @api.depends("is_iva")
    def _compute_retention_type(self):
        for partner in self:
            partner.retention_type = "iva" if partner.is_iva else "islr"

    def _write_retention_type(self):
        for partner in self:
            partner.is_iva = partner.retention_type == "iva"

    @api.depends("invoice_number")
    def _compute_type_document(self):
        for retention in self:
            if retention.invoice_number.move_type in ('out_invoice', 'in_invoice'):
                if retention.invoice_number.debit_origin_id:
                    retention.type_document = _('D/N')
                elif retention.invoice_number.move_type == 'out_invoice':
                    retention.type_document = _('Invoice')
                else:
                    retention.type_document = _('Bills')
            elif retention.invoice_number.move_type in ('in_refund', 'out_refund'):
                retention.type_document = _('C/N')
            else:
                retention.type_document = _('Other')

    @api.model
    def create(self, values):
        if values.get("code", "").strip().lower() in ["", "nuevo", "new"] and values.get("move_type", "") not in ['out_invoice', 'out_refund', ""]:
            values["code"] = self.env["ir.sequence"].next_by_code("retention.sequence")
        values["state"] = "posted"
        if values.get("retention_type", False) == "iva":
            retention_state = "with_retention_iva"
        else:
            retention_state = "with_retention_islr"
        invoice = self.env["account.move"].browse([values["invoice_number"]])
        if invoice.retention_state == "without_retention":
            invoice.write({
                "retention_state": retention_state
            })
        elif invoice.retention_state != retention_state and invoice.retention_state != "with_retention_both":
            invoice.write({
                "retention_state": "with_retention_both"
            })
        retention = super(Retention, self).create(values)

        return retention

    def _update_move_id(self):
        self.ensure_one()
        return {
            "journal_id": self._get_default_journal().id,
            "ref": _("%s withholding from %s invoice", self.retention_type, self.invoice_number.name),
            "date": self.date,
            "move_type": "entry",
            "partner_id": self.partner_id.id,
            "state": "posted"
        }

    def _prepare_move_lines(self):
        self.ensure_one()
        default_line_name = self.code
        if self.move_type in ('in_invoice', "out_refund"):
            # Receive money.
            counterpart_amount = self.amount_retention
        elif self.move_type in ('out_invoice', "in_refund"):
            # Send money.
            counterpart_amount = -self.amount_retention
        else:
            counterpart_amount = 0.0
        balance = self.currency_id._convert(
            counterpart_amount, self.company_id.currency_id, self.company_id, self.date)
        counterpart_amount_currency = counterpart_amount
        counterpart_account = self._get_counterpart_account()
        line_ids = [{
            'name': default_line_name,
            'date_maturity': self.date,
            'amount_currency': -counterpart_amount_currency,
            'currency_id': self.currency_id.id,
            'debit': balance < 0.0 and -balance or 0.0,
            'credit': balance > 0.0 and balance or 0.0,
            'partner_id': self.partner_id.id,
            'account_id': self.destination_account_id.id
        }, {
            'name': default_line_name,
            'date_maturity': self.date,
            'amount_currency': -counterpart_amount_currency,
            'currency_id': self.currency_id.id,
            'debit': balance > 0.0 and balance or 0.0,
            'credit': balance < 0.0 and -balance or 0.0,
            'partner_id': self.partner_id.id,
            'account_id': counterpart_account.account_id.id
        }]
        return line_ids

    def _get_counterpart_account(self):
        self.ensure_one()
        lines = []
        for line in self.invoice_number.line_ids:
            if line.account_id.internal_type in ("receivable", "payable"):
                lines.append(line)
        return lines[0]

    @api.depends("original_document_number", "code")
    def _compute_complete_name_with_code(self):
        for retention in self:
            retention.complete_name_with_code = f"[{retention.code}] {retention.original_document_number}"

    def button_cancel(self):
        self.write({"state": "cancel"})
        self.move_id.button_draft()
        self.move_id.button_cancel()
