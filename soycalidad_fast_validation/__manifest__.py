{
    'name': 'Validación rápida',
    'version': '1.0',
    'description': 'La validación rápida permite que el usuario actual pase por todos los datos de validación',
    'summary': 'Validación rápida según lo descrito en la norma',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': 'LGPL-3',
    'category': 'soycalidad',
    'depends': [
        'mgmtsystem_audit',
        'mgmtsystem_comunication',
        'mgmtsystem_context',
        'mgmtsystem_employees',
        'mgmtsystem_infrastructure',
        'mgmtsystem_legal',
        'mgmtsystem_process',
        'mgmtsystem_process_integration',
        'mgmtsystem_management_review',
        'mgmtsystem_partner_qualification',
        'mgmtsystem_qualitymanual',
        'mgmtsystem_survey',
        'mgmtsystem_target',
        'stock_inspection',
    ],
    'data': [
        'views/validation.xml'
    ],
    'demo': [
        
    ],
    'auto_install': False,
    'application': False,
}