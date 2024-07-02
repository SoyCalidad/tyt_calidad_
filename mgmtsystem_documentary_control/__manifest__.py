{
    'name': 'Lista maestra',
    'version': '1.0',
    'description': 'Gestión de la lista maestra así como los códigos',
    'summary': 'Generación de códigos y lista maestra',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': 'Other proprietary',
    'category': 'mgmtsystem',
    'depends': [
        'mgmtsystem_process',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/documentary_control.xml',
        'reports/report_purchase.xml',
    ],
    'demo': [
    ],
    'auto_install': False,
    'application': False,
}