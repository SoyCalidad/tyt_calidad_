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
        'contacts', 'mgmtsystem_partner_qualification', 'mgmtsystem_process_integration',
    ],
    'data': [
        'security/ir.model.access.csv',

        'report/supplier_complaints_inventory.xml',
        'report/customer_directory.xml',
        'report/approved_supplier.xml',
        'report/customer_property.xml',
        'report/supplier_evaluation_verification.xml',

        'wizard/supplier_complaints_inventory_export.xml',
        'wizard/customer_directory_export.xml',
        'wizard/approved_supplier_export.xml',
        'wizard/customer_property_export.xml',
        'wizard/supplier_evaluation_verification_export.xml',

        'views/supplier_complaints_inventory_views.xml',
        'views/res_partner_views.xml',
        'views/evaluation_history_views.xml',
        'views/menus.xml',

        'data/data.xml',
        'data/evaluation.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
