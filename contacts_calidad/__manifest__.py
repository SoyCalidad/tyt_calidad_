# -*- coding: utf-8 -*-
{
    'name': "Personalizar Contactos",

    'summary': """
        Personaliza contactos Frescos""",

    'description': """
        Codigo, Segmento, grupo, Frescos
    """,

    'author': "soycalidad",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base',
                'frescos_contacts',],

    'data': [
        'views/res_partner_views.xml',
    ],
}