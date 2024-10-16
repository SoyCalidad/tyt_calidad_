{
    'name': 'Intranet Helpdesk TYT Contact Center - Soy Calidad',
    'version': '1.0',
    'description': 'Intranet Helpdesk TYT Contact Center - Soy Calidad',
    'summary': 'Intranet Helpdesk TYT Contact Center - Soy Calidad',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': 'Other proprietary',
    'category': 'soycalidad',
    'depends': [
        'base', 'mail', 'portal', 'website',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_template_data.xml',
        'data/data.xml',
        'views/mailbox_views.xml',
        'views/notification_matrix_views.xml',
        'views/mailbox_templates.xml',
        'views/mailbox_portal_templates.xml',
        'views/menus.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/tyt_intranet_helpdesk/static/src/scss/input.scss',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
}
