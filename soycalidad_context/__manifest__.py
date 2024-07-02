{
    'name': 'Contexto de Soy Calidad',
    'version': '1.0',
    'description': 'Agrega especificaciones para el módulo de contexto para Soy Calidad',
    'summary': 'Personalización del módulo de contexto para Soy Calidad',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': '',
    'category': 'soycalidad',
    'depends': [
        'mgmtsystem_context',
        'mgmtsystem_target',
    ],
    'data': [
        'data/data.xml',
        'views/internal_issue.xml',
        'reports/policy.xml',
        'reports/internal_issue.xml',
    ],
    'demo': [
    ],
    'auto_install': False,
    'application': False,
}