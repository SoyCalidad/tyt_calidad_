{
    'name': 'TYT Contacts Reports',
    'version': '1.0',
    'description': 'TYT Contacts Reports',
    'summary': 'TYT Contacts Reports',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': 'Other proprietary',
    'category': 'soycalidad',
    'depends': [
        'contacts',
    ],
    'data': [
        'security/ir.model.access.csv',

        'report/supplier_complaints_inventory.xml',
        'report/customer_directory.xml',

        'wizard/supplier_complaints_inventory_export.xml',
        'wizard/customer_directory_export.xml',

        'views/supplier_complaints_inventory_views.xml',
        'views/customer_directory_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
