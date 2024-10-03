# -*- coding: utf-8 -*-
{
    'name': "Personalizar Ventas Frescos",

    'summary': """
        Personaliza ventas Frescos""",

    'description': """
    """,

    'author': "soycalidad",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base',
                'frescos_sale',],

    'data': [
        'views/sale_order_views.xml',
        'reports/report_saleorder_document.xml', 
    ],
}