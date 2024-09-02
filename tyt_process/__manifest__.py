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
        'security/ir.model.access.csv',
        'views/procedure_edition.xml',
        'reports/report_paperformat.xml',
        'reports/report_layout.xml',
        'reports/procedure_edition.xml',
        'reports/procedure_edition_cover.xml',
        'reports/procedure_edition_toc.xml',
        'reports/procedure_edition_meta.xml',
        'reports/procedure_edition_body.xml',
        'reports/procedure_edition_back_cover.xml',
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