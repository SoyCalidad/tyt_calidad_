# -*- coding: utf-8 -*-
{
    'name': "Calificación para socios",

    'summary': """Agrega calificaciones a proveedores""",

    'author': "Soy Calidad",
    'website': "http://www.soycalidad.com",

    'category': 'Uncategorized',
    'version': '1.1',

    'depends': ['contacts', 'report_xlsx', 'hola_calidad', 'mgmtsystem_process'],

    'data': [
        'data/evaluation.xml',
        'data/initial_evaluation.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        'views/evaluation_history_views.xml',
        'views/initial_evaluation.xml',
        'views/res_partner_inherit_views.xml',
        'report/report_res_partner_evaluation.xml',
        'report/initial_evaluation.xml',
        'wizards/partner_qualification.xml',
        'data/mail_template_data.xml',
    ],
}
