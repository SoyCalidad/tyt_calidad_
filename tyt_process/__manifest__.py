{
    'name': 'Procesos TYT Contact Center - Soy Calidad',
    'version': '1.0',
    'description': 'Añade características al módulo Procesos TYT Contact Center',
    'summary': 'Añade características al módulo Procesos TYT Contact Center',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': '',
    'category': 'soycalidad',
    'depends': [
        'mgmtsystem_process',
        'mgmtsystem_process_integration',
        'mgmtsystem_management_review',
    ],
    'data': [
        'views/documentary_control_views.xml',
        #'views/communication.xml',
        #'views/management_review_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}