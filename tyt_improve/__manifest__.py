{
    'name': 'Mejora Continua TYT Contact Center - Soy Calidad',
    'version': '1.0',
    'description': 'Añade características al módulo Mejora Continua TYT Contact Center',
    'summary': 'Añade características al módulo Mejora Continua TYT Contact Center',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': '',
    'category': 'soycalidad',
    'depends': [
        'mgmtsystem_nonconformity',
        'mgmtsystem_audit',
        'soycalidad_improve',
    ],
    'data': [
        #'security/ir.model.access.csv',
        'views/change_request.xml',
        'views/mgmtsystem_nonconformity.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}