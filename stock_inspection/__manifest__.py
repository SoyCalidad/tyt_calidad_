# -*- coding: utf-8 -*-
{
    'name': "Ficha de inspección para compras-productos",

    'summary': """
        Ficha de inspección para compras-productos
        """,

    'description': """
        Permite añadir una ficha que indica la revisión
        de la recepción de pedidos, este módulo hereda de
        stock.
    """,

    'author': "HC",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['purchase', 'stock', 'base', 'mgmtsystem_validation'],

    # always loaded
    'data': [
        'reports/inspection.xml',
        'views/stock_inherit.xml',
        'views/criterio_views.xml',
        'views/inspection.xml',
        'views/templates.xml',
        'reports/inspection.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],

    # 'installable': True,
    # 'application': True,
}
