{
    'name': 'CRM de Soy Calidad',
    'version': '1.0',
    'description': 'Añade características al módulo CRM',
    'summary': 'Añade características al módulo CRM',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': '',
    'category': 'crm',
    'depends': [
        'crm',
        'dms',
        'soycalidad_ciiu',
    ],
    'data': [
        'data/dms.xml',
        'views/crm.xml',
        'reports/sales_report.xml',
        'reports/crm_report.xml',
        'wizards/crm_user_transfer.xml',
    ],
    'auto_install': False,
    'application': False,
}