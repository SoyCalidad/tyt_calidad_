# -*- coding: utf-8 -*-
{
    'name': "Patrols Log",

    'summary': """
        Patrol Log""",

    'description': """
    """,

    'author': "soycalidad",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','maintenance','tyt_remediation_log'],

    'data': [
        'security/ir.model.access.csv',
        'views/maintenance_patrollog_views.xml',
        'report/report_patrol_log.xml',
    ],
}