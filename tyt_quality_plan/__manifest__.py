# -*- coding: utf-8 -*-
{
    'name': "Quality Plan",

    'summary': """
        Quality Plan""",

    'description': """
    """,

    'author': "soycalidad",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','maintenance','report_xlsx'],

    'data': [
        'security/ir.model.access.csv',
        'views/maintenance_quality_plan_views.xml',
        'report/report_quality_plan.xml',
    ],
}