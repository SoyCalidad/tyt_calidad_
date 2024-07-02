{
    'name': 'Procesos predeterminados Soy Calidad',
    'version': '1.0',
    'description': 'Añade procesos predeterminados para Soy Calidad',
    'summary': 'Procesos predeterminados para Soy Calidad',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': '',
    'category': 'mgmt',
    'depends': [
        'mgmtsystem_process',
        'mgmtsystem_legal',
    ],
    'data': [
        'data/process_categ.xml',
        'data/process.xml',
        'wizards/utils.xml',
    ],
    'demo': [
    ],
    'auto_install': False,
    'application': False,
}