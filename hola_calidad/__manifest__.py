# -*- coding: utf-8 -*-
{
    'name': "Gestion de Calidad",

    'summary': """
        Gestion de calidad""",

    'description': """
        Es necesario instalar lib de python:
            - openpyxl
    """,

    'author': "6",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'mail', 'account', 'soycalidad_css'],

    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        'views/frequency.xml',
        'views/helpers.xml',
        'views/menus.xml',
        'views/res_config.xml',
        'views/report_templates.xml',
        'views/diagnostic_views.xml',
        'views/partner.xml',
        'views/report.xml',
        'wizards/report_wizard.xml',
        'data/hola_calidad_data.xml',
        'data/hola_calidad.clause.csv',
        'data/hola_calidad.requirement.csv',
        'data/general.standard.csv',
        'data/iso_9001.requirement.csv',
        'data/frequency.xml',
    ],
    'assets': {
        'web.assets_backend': [
            "/hola_calidad/static/src/js/fun.js",
            "/hola_calidad/static/src/css/my_css.css",
            "/hola_calidad/static/src/css/soycalidad_report.css",
        ],
        'web.report_assets_common': [
            "/hola_calidad/static/src/scss/soycalidad_table.scss",
            "/hola_calidad/static/src/css/soycalidad_report.css",
        ],
        'web.assets_common': [
            "/hola_calidad/static/src/scss/soycalidad_table.scss",
            "/hola_calidad/static/src/css/soycalidad_report.css",
        ],
    },

    'installable': True,
    'application': True,
}
