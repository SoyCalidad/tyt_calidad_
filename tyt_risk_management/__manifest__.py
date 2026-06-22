{
    'name': 'TyT - Gestión de Riesgos',
    'version': '18.0.1.0.0',
    'summary': 'Estructurar la organización bajo un modelo basado en procesos',
    'category': 'Management',
    'author': 'David/SoyCalidad',
    'depends': [
        'base', 
        'web_hierarchy', 
        'mail',
        'documents',
        'hr',
        'report_xlsx',
        'preview_officeapps_attachments',
    ],
    'data': [
        'data/documents_document.xml',
        
        'security/group.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',


        'views/business_process_views.xml',
        'views/risk_management_views.xml',
        'views/catalog_views.xml',
        'views/res_users_views.xml',
        'views/action_plan_views.xml',
        'views/risk_mitigation_views.xml',
        'views/reports_templates.xml',
        'views/menus.xml',

        'wizard/risk.xml',
        'wizard/report_wizard_reports.xml',

        'data/risk_domain_data.xml',
        'data/catalog_data.xml',
        'data/risk_goal_coso_data.xml',
        'data/risk_assertion_data.xml',
        'data/risk_financial_statement_category_data.xml',
        'data/ir_cron.xml',
        'data/risk_degree_mitigation.xml',
        
        
    ],
    'assets':{ 
        'web.assets_backend': [
            'tyt_risk_management/static/src/**/*',
            'tyt_risk_management/static/lib/echarts/**/*',
        ],

    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}