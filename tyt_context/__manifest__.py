{
    'name': 'Contexto TYT Contact Center - Soy Calidad',
    'version': '1.0',
    'description': 'Añade características al módulo Contexto TYT Contact Center',
    'summary': 'Añade características al módulo Contexto TYT Contact Center',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': '',
    'category': 'soycalidad',
    'depends': [
        'base',
        'mgmtsystem_context',
        'mgmtsystem_process_integration',
    ],
    'data': [
        #'security/ir.model.access.csv',
        'views/context.xml',
        'report/stakeholders_report.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}