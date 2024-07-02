# -*- coding: utf-8 -*-
{
    'name': 'Sistema de gestión - Acciones',

    'summary': """
        Acciones""",

    'description': """
        Modulo de acciones preventivas, correctivas y de mejora
    """,

    'author': 'SoyCalidad',
    'website': "http://www.soycalidad.com",

    "category": "Management System",
    'version': '1.1',

    'depends': ['hola_calidad', 'mail','report_xlsx', 'mgmtsystem_process', 'mgmtsystem_documentary_control'],

    'data': [
        # 'data/automated_reminder.xml',
        # 'data/email_template.xml',
        'security/mgmtsystem_action_security.xml',
        'security/ir.model.access.csv',
        'data/action_sequence.xml',
        'data/data.xml',
        'views/menus.xml',
        'views/mgmtsystem_action.xml',
        'views/action_onboarding_templates.xml',
        'reports/action_report.xml',
        'data/email_template.xml',
        'wizards/reports.xml',
        'wizards/menus.xml',
    ],

    'installable': True,
}
