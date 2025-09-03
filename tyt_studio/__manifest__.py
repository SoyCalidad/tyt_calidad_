{
    'name': 'TYT Studio - Soy Calidad',
    'version': '1.0',
    'description': 'Añade modelos y campos que se crearon mediante odoo studio',
    'summary': 'Añade modelos y campos que se crearon mediante odoo studio',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': 'Other proprietary',
    'category': 'soycalidad',
    'depends': [
        'mail',
        'account',
        'hr',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/site_views.xml',
        'views/sites_views.xml',
        'views/menus.xml',

    ],
    'auto_install': False,
    'installable': True,
    'application': False,
    
}