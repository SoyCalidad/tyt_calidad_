# -*- coding: utf-8 -*-
{
    'name': "Remediation log",

    'summary': """
        Remediation log""",

    'description': """
    """,

    'author': "soycalidad",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','maintenance'],

    'data': [
        'security/ir.model.access.csv',
        'views/maintenance_remediationlog_views.xml',
        'report/report_remediation_log.xml',
    ],
}