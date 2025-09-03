{
    'name': 'Contexto TYT Contact Center - Soy Calidad',
    'version': '1.0',
    'description': 'Añade características al módulo Contexto TYT Contact Center',
    'summary': 'Añade características al módulo Contexto TYT Contact Center',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': 'Other proprietary',
    'category': 'soycalidad',
    'depends': [
        'base',
        'mgmtsystem_context',
        'mgmtsystem_process_integration',
        'tyt_process',
        'hola_calidad',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/mail_template_data.xml',

        'views/context.xml',
        'views/context_scope_views.xml',
        'views/process_edition_views.xml',
        'report/stakeholders_report.xml',
        'wizard/product_service_communicate.xml',
        'views/menus.xml',

        'report/context_scope.xml',
        'report/context_scope_cover.xml',
        'report/context_scope_body.xml',
        'report/context_scope_toc.xml',
        'report/context_scope_back_cover.xml',

        'data/context_scope_mail_template.xml',
    ],
    'assets': {
        'web.report_assets_common': [
            '/tyt_process/static/src/scss/fonts.scss',
            '/tyt_process/static/src/scss/procedure_edition.scss',
            '/tyt_context/static/src/scss/context_scope.scss',
        ],
    },
    'auto_install': False,
    'installable': True,
    'application': False,
    "external_dependencies": {
        "python": [
            "PyMuPDF",
        ],
    },
}
