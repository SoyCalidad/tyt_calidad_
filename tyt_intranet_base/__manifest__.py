{
    'name': 'Intranet Base Module',
    'version': '1.0',
    'description': 'Intranet Base Module',
    'summary': 'Intranet Base Module',
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
        'views/menus.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
