{
    'name': 'Mejoras y correcciones de CSS para Soy Calidad',
    'version': '1.0',
    'description': 'Mejora las vistas y estilos de Soy Calidad',
    'summary': 'Mejora las vistas y estilos de Soy Calidad',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': 'LGPL-3',
    'category': 'soycalidad',
    'depends': [
        'web'
    ],
    'data': [
        'views/web.xml',
    ],
    'demo': [

    ],
    'assets': {
        'web.report_assets_pdf': [
            "/soycalidad_css/static/src/scss/mgmtsystem.scss",
        ],
        'web.assets_backend': [
            "/soycalidad_css/static/src/scss/form_view_extra.scss",
        ],
    },
    'auto_install': False,
    'application': False,
}