# -*- coding: utf-8 -*-
{
    'name': "Personalizar Fracturas",

    'summary': """
        Personaliza Facturas Frescos""",

    'description': """
        Facturas Frescos
    """,

    'author': "soycalidad",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base',
                'account',
                'sale',
                'stock',],

    'data': [
        'reports/report_invoice_templates.xml', 
    ],
}