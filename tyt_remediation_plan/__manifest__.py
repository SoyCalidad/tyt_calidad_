# -*- coding: utf-8 -*-
{
    'name': "Remediation Plan",

    'summary': """
        Remediation Plan""",

    'description': """
    """,

    'author': "soycalidad",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','maintenance'],

    'data': [
        'security/ir.model.access.csv',
        'views/maintenance_remediation_plan_views.xml',
        'report/report_remediation_plan.xml',
    ],
}