# -*- coding: utf-8 -*-
{
    'name': "Revisión por la dirección",

    'summary': """[]""",

    'author': "Soy Calidad",
    'website': "http://www.soycalidad.com",

    'category': 'Management System',
    'version': '1.1',

    'depends': ['mgmtsystem_context',
                'mgmtsystem_survey',
                'mgmtsystem_target',
                'mgmtsystem_nonconformity',
                'mgmtsystem_opportunity',
                'mgmtsystem_comunication',
                'soycalidad_comittee',
                'mgmtsystem_documentary_control', ],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/management_review_views.xml',
        'views/mgmt_review_onboarding_templates.xml',
        'report/managementreview_report.xml',
        'report/plan.xml',
        'report/managementreviewplan_report.xml',
        'data/sequences.xml',
    ],
}
