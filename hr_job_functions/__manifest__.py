{
    'name': 'Añadidos de calidad a empleados y puestos',
    'version': '1.0',
    'description': 'Añade a los puesto de trabajo: identificación, Funciones, Factores de Evaluación, Coordinación, Supervisión, Perfil del Puesto, Competencias Genéricas, Competencias de trabajos en equipo, Competenciones Personales, Competencias estratégicas',
    'summary': 'Añade funciones e información general a los puestos de trabajo',
    'author': 'Soy Calidad',
    'website': '',
    'license': 'LGPL-3',
    'category': '',
    'depends': [
        'hr',
        'mgmtsystem_context',
        'mgmtsystem_employees',
        #'user_creation_from_employee123456',
        'hr_recruitment',
    ],
    'data': [
        'data/sequences.xml',
        'views/hr_job.xml',
        'views/employee.xml',
        'report/hr_job_report.xml',
        'wizards/job_function.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        ''
    ],
    'auto_install': False,
    'application': True,
}