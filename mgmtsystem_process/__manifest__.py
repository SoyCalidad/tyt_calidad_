# -*- coding: utf-8 -*-
{
    'name': "Procesos y procedimientos",

    'summary': """
        Mapa de proceso, procesos y procedimientos""",

    'description': """
        [description]""",

    'author': 'SoyCalidad',
    'website': "http://www.soycalidad.com",

    'category': "Management System",
    'version': '1.1',

    'depends': ['hola_calidad','hr',
                'document_knowledge',
                'document_knowledge','document_page','report_xlsx', 'mgmtsystem_validation', 'purchase', 'stock'],

    'data': [
        'data/mgmt_categ.xml',
        'security/security.xml',
        'security/rules.xml',
        'security/ir.model.access.csv',
        'views/menus.xml',
        'views/process_edition_views.xml',
        'views/process_views.xml',
        'views/documentary_control_views.xml',
        'views/documentation_inherit.xml',
        'views/process_onboarding_templates.xml',
        'views/process_validation.xml',
        'views/templates.xml',
        'report/report_process.xml',
        'report/report_process_edition.xml',
        'report/documentary_control.xml',
        'data/mail_template_data.xml',
        'wizards/process_report.xml',
        'wizards/process_edition.xml',
    ],
    'installable': True,
    'application': True,
}