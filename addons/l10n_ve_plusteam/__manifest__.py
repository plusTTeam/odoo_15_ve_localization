# -*- coding: utf-8 -*-
{
    'name': "Venezuela - Accounting",

    'summary': """
Venezuelan accounting Localization based on laws defined by SENIAT to operate in Venezuela
    """,

    'description': """
Venezuelan Account Localization
----------

Venezuela doesn't have any chart of account by law, but the default
proposed in Odoo should comply with some Accepted best practices in Venezuela

Features:
* Taxes for Venezuela
* Retention process for IVA, ISLR and IGTF
* Accounting books: Mayor, Diario, Inventario y Balances
* States for Venezuela
* Consulting of RIF
* New fields in invoices and contacts
* Multiple exchange rates by day
* Communication with fiscal printers
    """,

    'author': "PLUSTEAM",
    'website': "https://plusteam.tech",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting/Localizations/Account Charts',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts', 'account', 'account_accountant', 'hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/res_currency_data.xml',
        'data/res_lang_data.xml',
        'data/ir_translation_data.xml',
        'data/res_users_data.xml',
        'data/islr_concepts_data.xml',
        'data/person_type_data.xml',
        'data/res_country_state_data.xml',
        'data/account_chart_template_data.xml',
        'data/account_account_data.xml',
        'data/account_tax_data.xml',
        'data/account_chart_template_try_loading_data.xml',
        'data/resource_calendar_leaves_data.xml',
        'data/resource_calendar_attendance_data.xml',
        'data/resource_calendar_data.xml',
        'data/account_journal_data.xml',
        'data/res_config_settings_data.xml',
        'data/res_country_data.xml',
        'views/res_partner_views.xml',
        'views/islr_concepts_views.xml',
        'views/person_type_views.xml',
        'views/tax_unit_views.xml',
        'views/account_move_views.xml',
        'views/res_config_settings_views.xml',
        'views/res_currency_views.xml',
        'views/res_company_views.xml',
        'views/account_payment_views.xml',
        'wizard/account_payment_register_views.xml',
        'views/menu_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
