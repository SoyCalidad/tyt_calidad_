{
    'name': 'Módulo de mejora continua para Soy Calidad',
    'version': '1.0',
    'description': '',
    'summary': '',
    'author': '',
    'website': '',
    'license': 'LGPL-3',
    'category': '',
    'depends': [
        'mgmtsystem_action',
        'mgmtsystem_nonconformity',
        'mgmtsystem_process_integration',
        'mgmtsystem_target',
        #'soycalidad_dms',
    ],
    'data': [
        'data/data.xml',
        'data/soycalidad.improve_plan.change_type.csv',
        'data/soycalidad.change_request.area.csv',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/improve.xml',
        'views/change_request.xml',
        'views/change_request_origin.xml',
        'views/menus.xml',
        'views/improve_onboarding_templates.xml',
        'reports/improve_matrix.xml',
        'reports/change_request.xml',
        'reports/menus.xml',

    ],
    'demo': [

    ],
    'auto_install': False,
    'application': False,
}