# -*- coding: utf-8 -*-
{
    'name': "Non-Conforming Products Log",

    'summary': """
        Non-Conforming Products Log""",

    'description': """
    """,

    'author': "soycalidad",
    'license': 'Other proprietary',
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': [
        'base',
        'hr',
        'mgmtsystem_nonconformity',
        'marketing_automation',
        'report_xlsx', 
        #'tyt_studio'
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/non_conforming_products_log_view.xml',
        'report/non_conformity_log_xlsx.xml',
        'report/non_conformity_log_wizard_view.xml',
        'report/menu.xml',
    ],
}