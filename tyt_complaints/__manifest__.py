{
    'name': 'Quejas y Reclamos TYT Contact Center - Soy Calidad',
    'version': '1.0',
    'description': 'Añade características al módulo Quejas y Reclamos TYT Contact Center',
    'summary': 'Añade características al módulo Quejas y Reclamos TYT Contact Center',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': '',
    'category': 'soycalidad',
    'depends': [
        'mgmtsystem_complaints',
    ],
    'data': [
        #'security/ir.model.access.csv',
        'views/complaints.xml',
        'views/menus.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}