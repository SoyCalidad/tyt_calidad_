{
    'name': 'Bug Tracker de Soy Calidad',
    'version': '18.0.0.0',
    'description': 'Añade un botón en la pantallla principal para reportar bugs',
    'summary': 'Botón de reporte de bugs',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': 'Other proprietary',
    'category': 'bugs',
    'depends': [
        'base'
    ],
    'data': [
    ],
    'demo': [
    ],
    'qweb': [
        'static/src/xml/tree_view_button.xml',
    ],
    'assets': {
        'web.assets_backend': [
            "/soycalidad_bugtracker/static/src/js/tree_view_button.js",
        ],
    },
    'auto_install': False,
    'application': False,
}
