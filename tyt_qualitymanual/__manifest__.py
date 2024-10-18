{
    'name': 'Manual del sistema de calidad TYT Contact Center - Soy Calidad',
    'version': '1.0',
    'description': 'Añade características al módulo Manual del sistema de calidad TYT Contact Center',
    'summary': 'Añade características al módulo Manual del sistema de calidad TYT Contact Center',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': 'Other proprietary',
    'category': 'soycalidad',
    'depends': [
        'base',
        'mgmtsystem_qualitymanual',
        'tyt_process',
    ],
    'data': [
        'report/qualitymanual.xml',
        'report/qualitymanual_cover.xml',
        'report/qualitymanual_body.xml',
        'report/qualitymanual_toc.xml',
        'report/qualitymanual_back_cover.xml',
    ],
    'assets': {
        'web.report_assets_common': [
            '/tyt_process/static/src/scss/fonts.scss',
            '/tyt_process/static/src/scss/procedure_edition.scss',
            '/tyt_qualitymanual/static/src/scss/qualitymanual.scss',
        ],
    },
    'auto_install': False,
    'installable': True,
    'application': False,
}
