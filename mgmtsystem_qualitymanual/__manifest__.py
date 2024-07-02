# -*- coding: utf-8 -*-
{
    'name': "Manual del sistema de calidad",

    'summary': """Manual del sistema de gestión de calidad""",

    'description': """[]""",

    'author': "Soy Calidad",
    'website': "http://www.soycalidad.com",

    'category': 'Managment System',
    'version': '1.1',

    'depends': ['hola_calidad',
                'mgmtsystem_process',
                'mgmtsystem_context',
                'mgmtsystem_target',
                'mgmtsystem_infrastructure',
                'mgmtsystem_comunication',
                'mgmtsystem_employees',
                'mgmtsystem_partner_qualification',
                'stock_inspection'],

    'data': [
        'security/ir.model.access.csv',
        'views/qualitymanual_views.xml',
        'report/qualitymanual_report.xml',
        'wizards/quality_manual.xml',
    ],
}