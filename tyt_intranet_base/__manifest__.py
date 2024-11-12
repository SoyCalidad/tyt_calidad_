{
    'name': 'Intranet Base TYT Contact Center - Soy Calidad',
    'version': '1.0',
    'description': 'Intranet Base TYT Contact Center - Soy Calidad',
    'summary': 'Intranet Base TYT Contact Center - Soy Calidad',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': 'Other proprietary',
    'category': 'soycalidad',
    'depends': [
        'hr',
    ],
    'data': [
        'security/intranet_security.xml',
        'security/ir.model.access.csv',
        'views/intranet_groups_views.xml',
        'views/hr_employee_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
