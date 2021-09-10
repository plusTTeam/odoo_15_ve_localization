# -*- coding: utf-8 -*-
import logging
from odoo import models, api, _
_logger = logging.getLogger(__name__)


class AccountChartTemplate(models.Model):
    _inherit = "account.chart.template"

    @api.model
    def update_translation_accounts(self):
        account_liquidity_transfer = self.env["account.account"].search([("name", "=", "Liquidity Transfer")])
        for account in account_liquidity_transfer:
            account.write({"name": "Transferencia de liquidez"})
        account_undistributed_profits_losses = self.env["account.account"].search(
            [("name", "=", "Undistributed Profits/Losses")])
        for account in account_undistributed_profits_losses:
            account.write({"name": "Ganancias/pérdidas no distribuidas"})

        account_liquidity_transfer_template = self.env["account.account.template"].search([("name", "=", "Liquidity Transfer")])
        for account in account_liquidity_transfer_template:
            account.write({"name": "Transferencia de liquidez"})
        account_undistributed_profits_losses_template = self.env["account.account.template"].search(
            [("name", "=", "Undistributed Profits/Losses")])
        for account in account_undistributed_profits_losses_template:
            account.write({"name": "Ganancias/pérdidas no distribuidas"})

    def _load(self, sale_tax_rate, purchase_tax_rate, company):
        load = super(AccountChartTemplate, self)._load(sale_tax_rate, purchase_tax_rate, company)
        company = self.env.company
        refs = [
            ["vat_withholding_suppliers", "iva_account_purchase_id"],
            ["islr_withholding_suppliers", "iva_account_sale_id"],
            ["vat_withholding_customer", "islr_account_purchase_id"],
            ["islr_withholding_customer", "islr_account_sale_id"]
        ]
        for ref in refs:
            external_id = self.env.ref(ref[0]).get_external_id()
            module, name = external_id.split(".", 1)
            xml_id = "%s.%s_%s" % (module, company.id, name)
            company[ref[1]] = self.env.ref(xml_id).id
            _logger.info(xml_id, self.env.ref(xml_id).id)
        company.account_sale_tax_id = self.env["account.tax"].search(
            [("value", "=", 16), ("company_id", "=", company.id)], limit=1).id
        company.account_purchase_tax_id = self.env["account.tax"].search(
            [("value", "=", 16), ("company_id", "=", company.id)], limit=1).id
        return load
