# -*- coding: utf-8 -*-
{
    'name': "Sistema de gestión - Comunicación",

    'summary': """
        Incluye Programa de comunicación, plan de comunicación, actas de reunión y otros""",

    'author': 'Ser Calidad',
    'website': "http://www.soycalidad.com",

    "category": "Management System",
    'version': '1.1',

    'depends': [
        'mgmtsystem_process',
        'mgmtsystem_action',
        'mgmtsystem_target',
        'mgmtsystem_nonconformity',
        'mgmtsystem_documentary_control'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/res_config_settings.xml',
        'views/document.xml',
        'views/plan.xml',
        'views/comunication_record.xml',
        'views/menus.xml',
        'views/comunication_onboarding_templates.xml',
        'data/sequences.xml',
        'reports/record_meeting.xml',
        'reports/plan.xml',
        'reports/comunication.xml',
        'data/mail_templates.xml',
        'wizards/models.xml',
        'wizards/comunication.xml',
        'wizards/record_meeting.xml',
        'wizards/menus.xml',
    ],

    'installable': True,
    'application': True,
}
