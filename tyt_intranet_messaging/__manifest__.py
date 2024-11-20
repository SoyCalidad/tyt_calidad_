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
        'views/department_message_portal_templates.xml',
        'views/menus.xml',

        'views/snippets/s_message_popup.xml',
        'views/snippets/snippets.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'tyt_intranet_messaging/static/src/js/mark_as_read.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
}
