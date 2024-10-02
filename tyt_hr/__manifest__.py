{
    'name': 'Empleados (HR) TYT Contact Center - Soy Calidad',
    'version': '1.0',
    'description': 'Añade características al módulo Empleados (HR) TYT Contact Center',
    'summary': 'Añade características al módulo Empleados (HR) TYT Contact Center',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': 'LGPL-3',
    'category': 'soycalidad',
    'depends': [
        'hr',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}