# -*- coding: utf-8 -*-
{
    'name': "report_requirements",

    'summary': """
        report of the legal requirements module""",

    'description': """
        report of the legal requirements module
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['mgmtsystem_legal'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/report_requirements.xml',
        
    ],
}