# -*- coding: utf-8 -*-
{
    'name': "Manejo de satisfaccion del cliente",

    'summary': """
        Ejecucion de satisfacciones etc""",

    'description': """
        [Descripción]
    """,

    'author': "HC",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['mgmtsystem_action', 'mgmtsystem_nonconformity', 'website', 'mgmtsystem_documentary_control'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/complaint_attributes.xml',
        'data/complaint.complaint.reason.csv',
        'views/templates.xml',
        'views/menus.xml',
        'views/complaint_views.xml',
        'views/configuration_views.xml',
        'views/analisis_views.xml',
        'views/report_views.xml',
        'views/complaints_onboarding_templates.xml',
        'reports/complaint.xml',
        'wizards/complaint_wizard_views.xml',
        "static/src/xml/complaint.xml",
    ],
    'assets': {
        'web.assets_frontend': [
            "/mgmtsystem_complaints/static/src/css/complaint.css",
            "/mgmtsystem_complaints/static/src/js/complaint.js",
        ],
    },
}