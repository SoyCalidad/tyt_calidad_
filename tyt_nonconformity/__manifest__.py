{
    'name': 'No Conformidades TYT - Soy Calidad',
    'version': '1.0',
    'description': 'Añade características al módulo No Conformidades TYT',
    'summary': 'Añade características al módulo No Conformidades TYT',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': 'AGPL-3',
    'category': 'soycalidad',
    'depends': [
        'mgmtsystem_nonconformity',
    ],
    'data': [
        'views/menus.xml',
        'report/non_conformity_report.xml',
        #'report/stakeholders_report.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}