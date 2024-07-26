{
    'name': 'Post-Soy Calidad - Base',
    'version': '1.0',
    'description': 'Instala las mejoras soycalidad hasta el modulo MEJORA CONTINUA',
    'summary': 'Instala las mejoras soycalidad hasta el modulo MEJORA CONTINUA',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': 'LGPL-3',
    'category': 'quality_system',
    'depends': [
        'hola_calidad',
        'menus_hola_calidad',

        'soy_calidad_onboarding',
        'soycalidad_bugtracker',
        'soycalidad_ciiu',
        'soycalidad_context',
        'soycalidad_default_processes',        
        'dms',
        'soycalidad_dms',
        'soycalidad_fast_validation',
        'soycalidad_improve',

        #'dms_user_role', # necesita de otro modulo base "base_user_role" y causa errores si dejas de comentarlo
        #'dms_auto_classification',
    ],
    'data': [
    ],
    'demo': [
    ],
    'auto_install': False,
    'application': True,
}
