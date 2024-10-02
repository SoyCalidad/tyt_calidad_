{
    'name': 'Procesos TYT Contact Center - Soy Calidad',
    'version': '1.0',
    'description': 'Añade características al módulo Procesos TYT Contact Center',
    'summary': 'Añade características al módulo Procesos TYT Contact Center',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': 'Other proprietary',
    'category': 'soycalidad',
    'depends': [
        'mgmtsystem_process',
    ],
    'data': [
        'data/process.xml',
    ],
    'assets': {
        'web.report_assets_common': [
                "/tyt_process/static/src/scss/fonts.scss",
                "/tyt_process/static/src/scss/procedure_edition.scss",
        ],
    },
    'auto_install': False,
    'installable': True,
    'application': False,
}