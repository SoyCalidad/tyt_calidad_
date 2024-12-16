{
    'name': 'Objetivos TYT Contact Center - Soy Calidad',
    'version': '1.0',
    'description': 'Añade características al módulo Objetivos TYT Contact Center',
    'summary': 'Añade características al módulo Objetivos TYT Contact Center',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': '',
    'category': 'soycalidad',
    'depends': [
        'mgmtsystem_target',
        'mgmtsystem_process_integration',
    ],
    'data': [
        #'security/ir.model.access.csv',
        'views/target.xml',
        'report/helpers.xml',
        'report/target.xml',
        'report/template.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}