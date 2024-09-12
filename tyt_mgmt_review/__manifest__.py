{
    'name': 'Revision por la dirección TYT Contact Center - Soy Calidad',
    'version': '1.0',
    'description': 'Añade características al módulo Revision por la dirección TYT Contact Center',
    'summary': 'Añade características al módulo Revision por la dirección TYT Contact Center',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': '',
    'category': 'soycalidad',
    'depends': [
        'mgmtsystem_management_review',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/management_review_views.xml',
        'views/management_review_line2.xml',
        'report/management_review_plan_report.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}