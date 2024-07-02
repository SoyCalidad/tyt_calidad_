{
    'name': 'Partner de Soy Calidad 15',
    'version': '1.0',
    'description': 'Añade características "Partner" a Soy Calidad 15 ',
    'summary': 'Añade características "Partner" a Soy Calidad 15',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': '',
    'category': 'soycalidad',
    'depends': [
        'hola_calidad',
        'mgmtsystem_partner_qualification',

    ],
    'data': [
        'views/res_partner_inherit_views.xml',

    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}