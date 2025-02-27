# -*- coding: utf-8 -*-
{
    'name': "Control of non-conforming outputs",

    'summary': """
        Control of non-conforming outputs""",

    'description': """
    """,

    'author': "soycalidad",
    'license': 'Other proprietary',
    'category': 'Management System',
    'version': '0.1',

    'depends': ['base','mgmtsystem_nonconformity','report_xlsx'],

    'data': [
        'security/ir.model.access.csv',
        'views/nonconformity_views.xml',
        'report/non_conformity_report_xlsx.xml',
        'report/non_conformity_report_wizard_view.xml',
        'report/menu.xml',
    ],
    
}