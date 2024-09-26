{
    'name': 'TYT Surveys',
    'version': '1.0',
    'description': 'TYT Surveys',
    'summary': 'TYT Surveys',
    'author': 'Soy Calidad',
    'website': 'https://www.soycalidad.com',
    'license': 'LGPL-3',
    'category': '',
    'depends': [
        'survey',
        'website',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/satisfaction_survey.xml',
        'static/src/xml/satisfaction_survey_main.xml',
        'static/src/xml/satisfaction_survey.xml',
    ],
    'auto_install': False,
    'application': False,
    'assets': {
        'web.assets_frontend': [
            "/tyt_survey/static/src/scss/satisfaction_survey_main.scss",
            "/tyt_survey/static/src/js/satisfaction_survey.js",
        ],
    },
}