# -*- coding: utf-8 -*-
{
    'name': "Plan de mantenimientos y gestión de equipos",

    'summary': """
        Incluye inventario y otros""",

    'author': "soycalidad",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['hola_calidad',
                'mgmtsystem_process',
                'maintenance',
                'kanban_draggable',
                'mgmtsystem_action',
                'mgmtsystem_target',
                'mgmtsystem_nonconformity',
                'maintenance_plan',
                'mgmtsystem_documentary_control'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'data/mgmtsystem.maintenance.frequency.csv',
        'views/res_config_settings.xml',
        'views/infrastructure.xml',
        'views/maintenance_plan.xml',
        'views/maintenance_inherit.xml',
        'views/calibration_plan.xml',
        'views/maintenance_onboarding_templates.xml',
        'report/report_maintenance_plan.xml',
        'report/report_request.xml',
        'report/report_calibration_plan.xml',
        'report/report_inventory.xml',
        'report/menus.xml',
    ],
    'external_dependencies': {
        'python': ['pandas'],
    },
}
