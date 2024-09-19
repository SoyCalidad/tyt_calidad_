{
    'name': 'Auditorías TYT Contact Center - Soy Calidad',
    'version': '1.0',
    'description': 'Añade características al módulo Auditorías TYT Contact Center',
    'summary': 'Añade características al módulo Auditorías TYT Contact Center',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': '',
    'category': 'soycalidad',
    'depends': [
        'mgmtsystem_audit',
        'mgmtsystem_nonconformity.xml',
    ],
    'data': [
        #'security/ir.model.access.csv',
        'views/audit.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}