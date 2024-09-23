{
    'name': 'TYT Surveys',
    'version': '1.0',
    'description': 'TYT Surveys',
    'summary': 'TYT Surveys',
    'author': 'Soy Calidad',
    'website': '',
    'license': 'LGPL-3',
    'category': '',
    'depends': [
        'survey',
        'website',
    ],
    'data': [
        'static/src/xml/satisfaction_survey_main.xml',
    ],
    'auto_install': False,
    'application': False,
    'assets': {
        'web.assets_frontend': [
            "/tyt_survey/static/src/scss/satisfaction_survey_main.scss",
        ],
    },
}