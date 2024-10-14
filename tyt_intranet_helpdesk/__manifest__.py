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
        'base', 'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/mailbox_views.xml',
        'views/notification_matrix_views.xml',
        'views/mailbox_templates.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
