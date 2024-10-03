# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'FRESCOS Sales',
    'version': '1.2',
    'category': 'Sales/Sales',
    'author': "soycalidad",
    'summary': 'Sales internal machinery',
    'description': """
This module contains all the common features of Sales Management and eCommerce.
    """,
    
    'depends': [
        'sales_team',
        'account_payment',  # -> account, payment, portal
        'utm',
        'sale',
    ],
    'data': [
        'views/sale_order_views.xml',
        'views/sale_menus.xml',  # Last because referencing actions defined in previous files
    ],
    'installable': True,
    'license': 'LGPL-3',
}
