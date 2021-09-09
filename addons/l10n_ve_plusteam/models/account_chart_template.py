# -*- coding: utf-8 -*-
from odoo import models, api, _


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
