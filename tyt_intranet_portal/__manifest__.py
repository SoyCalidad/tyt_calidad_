{
    'name': 'Intranet Portal Module',
    'version': '1.0',
    'description': 'Intranet Portal Module',
    'summary': 'Intranet Portal Module',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': 'Other proprietary',
    'category': 'soycalidad',
    'depends': [
        'portal',
    ],
    'data': [
        'views/portal_templates.xml',
        'views/sale_portal_templates.xml',
        # 'views/purchase_portal_templates.xml',
        # 'views/account_portal_templates.xml',
        # 'views/project_portal_templates.xml',
        # 'views/hr_timesheet_portal_templates.xml',
        'views/helpdesk_portal_templates.xml',
        # 'views/sign_portal_templates.xml',
        'views/survey_portal_templates.xml',
        'views/mailbox_portal_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            "/tyt_intranet_portal/static/src/css/main.css",
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}
