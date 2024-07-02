# -*- coding: utf-8 -*-
{
    'name': "Gestión de riesgos y oportunidades",

    'summary': """
        Ejecucion de gestion etc""",

    'description': """
        [Descripción]
    """,

    'author': "Soy Calidad",


    'category': 'Uncategorized',
    'version': '0.1',


    'depends': ['mgmtsystem_action',
                'mgmtsystem_process',
                'hola_calidad',
                'mgmtsystem_documentary_control', ],


    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        'data/evaluation_criterio.xml',
        'views/menus.xml',
        'views/block_views.xml',
        'views/matrix_views.xml',
        'views/configuration_views.xml',
        'views/assets.xml',
        'views/opportunity_onboarding_templates.xml',
        'report/matrix_report.xml',
    ],
    'assets': {
        'web.assets_backend': [
            "/mgmtsystem_opportunity/static/src/js/tour.js",
        ],
    },
}
