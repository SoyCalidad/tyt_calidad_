# -*- coding: utf-8 -*-
{
    'name': "Management Requisitos Legales",

    'summary': """
        Incluye programa de requisitos legales, requisitos, normas y otros""",

    'author': "soycalidad",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['mgmtsystem_process',
                'report_xlsx',
                'mgmtsystem_target',
                'mgmtsystem_nonconformity',
                'mgmtsystem_action',
                'mgmtsystem_documentary_control'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/legal_data.xml',
        'data/sequences.xml',
        'views/plan.xml',
        'views/legal.xml',
        'views/article.xml',
        'views/process.xml',
        'views/res_config_settings.xml',
        'views/legal_onboarding_templates.xml',
        'report/report_requirements.xml',
        'report/legal.xml',
        'report/process_edition.xml',
    ],
}
