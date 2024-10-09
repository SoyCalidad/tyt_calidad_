# -*- coding: utf-8 -*-
{
    'name': "Remediation Log",

    'summary': """
        Remediation Log""",

    'description': """
    """,

    'author': "soycalidad",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','maintenance','report_xlsx'],

    'data': [
        'security/ir.model.access.csv',
        'views/maintenance_remediationlog_views.xml',
        'report/report_remediation_log.xml',
    ],
}