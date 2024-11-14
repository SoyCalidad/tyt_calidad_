{
    'name': 'Intranet Messaging TYT Contact Center - Soy Calidad',
    'version': '1.0',
    'description': 'Intranet Messaging TYT Contact Center - Soy Calidad',
    'summary': 'Intranet Messaging TYT Contact Center - Soy Calidad',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': 'Other proprietary',
    'category': 'soycalidad',
    'depends': [
        'base', 'mail', 'portal', 'website', 'tyt_intranet_base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/department_message_views.xml',
        'views/menus.xml',
    ],
    'assets': {
        'web.assets_frontend': [

        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
}
