# -*- coding: utf-8 -*-
{
    'name': "l10n_ve_plusteam",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/islr_concepts_data.xml',
        'data/person_type_data.xml',
        'views/res_partner_views.xml',
        'views/islr_concepts_views.xml',
        'views/person_type_views.xml',
        'views/menu_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
