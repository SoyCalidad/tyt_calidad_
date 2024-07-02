# -*- coding: utf-8 -*-
{
    'name': "Management Auditorías Internas",

    'summary': """
        Incluye plan de auditorías, individuales y otros""",

    'author': "soycalidad",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['mgmtsystem_process', 'hola_calidad', 'mgmtsystem_validation', 'mgmtsystem_documentary_control'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/plan.xml',
        'views/audit.xml',
        'views/audit_onboarding_templates.xml',
        'report/report_plananual02_auditorias.xml',
        'report/report_informe.xml',
        'report/report_audit.xml',
        'data/mail_templates.xml',
        'data/sequences.xml',
        'wizards/reports.xml',
    ],
}