# -*- coding: utf-8 -*-
{
    'name': "dswd_registry_individuals",

    'summary': """
        individual registrants information""",

    'description': """
         individual registrants information
    """,

    'author': "OpenG2p",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['g2p_registry_individual'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'installable': True,
    'application': True,
    
}
