{
    'name': 'Intranet Survey Module',
    'version': '1.0',
    'description': 'Intranet Survey Module',
    'summary': 'Intranet Survey Module',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': 'Other proprietary',
    'category': 'soycalidad',
    'depends': [
        'tyt_intranet_base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/survey_survey_views.xml',
        'views/survey_management_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
