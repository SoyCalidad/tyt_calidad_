# -*- coding: utf-8 -*-
{
    'name': "Organizacion de Soy Calidad",

    'summary': """[]""",

    'author': "Soy Calidad",
    'website': "http://www.soycalidad.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'hola_calidad',
        'mgmtsystem_action',
        'mgmtsystem_context',
        'mgmtsystem_complaints',
        'mgmtsystem_target',
        'mgmtsystem_legal',
        'mgmtsystem_process',
        'mgmtsystem_opportunity',
        'purchase',
        'mgmtsystem_infrastructure',
        'hr_recruitment',
        'mgmtsystem_employees',
        'survey', #deberia de quitarlo, igual se instala con 'mgmtsystem_infrastructure'
        'mgmtsystem_qualitymanual',
        'mgmtsystem_management_review',
        'contacts',
        'document_knowledge',
        'mgmtsystem_validation',
        ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/menu_views.xml',
        'views/general_menus.xml',
        'views/menus_hide.xml',
        'views/general_onboarding_templates.xml',
    ],
}