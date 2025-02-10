{
    'name': 'Etapas de validación de registros',
    'version': '13.0.0.0',
    'description': 'Añade etapas de evaluación a los diferentes modulos de soy calidad',
    'summary': 'Las etapas de evaluación por defecto son validado, revisado y validado',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': 'Other proprietary',
    'category': 'tools',
    'depends': [
        'hola_calidad',
        #'dms',
    ],
    'data': [
        'views/validation_step.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        ''
    ],
    'auto_install': False,
    'application': False,
}