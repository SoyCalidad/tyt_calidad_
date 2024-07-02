{
    'name': 'Manual de organización y funciones',
    'version': '1.0',
    'description': 'Manual de organización y funciones',
    'summary': 'Manual de organización y funciones',
    'author': 'Soy Calidad',
    'website': 'https://soycalidad.com',
    'license': 'Other proprietary',
    'category': 'Soy Calidad',
    'depends': [
        'hr',
        'dms',
        'hola_calidad',
        'mgmtsystem_validation',
        'mgmtsystem_documentary_control',
        'mgmtsystem_process_integration',
        'soycalidad_improve',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/mof.xml',
        'views/menus.xml',
        'reports/mof.xml',
    ],
    'demo': [
    ],
    'auto_install': False,
    'application': False,
}