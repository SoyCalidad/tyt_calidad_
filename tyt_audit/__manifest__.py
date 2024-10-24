{
    'name': 'Auditorías TYT Contact Center - Soy Calidad',
    'version': '1.0',
    'description': 'Añade características al módulo Auditorías TYT Contact Center',
    'summary': 'Añade características al módulo Auditorías TYT Contact Center',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': '',
    'category': 'soycalidad',
    'depends': [
        'mgmtsystem_nonconformity',
        'mgmtsystem_audit',
        
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/audit_plan_tyt_auditor.xml',
        'views/audit.xml',
        'views/audit_plan_schedule_line.xml',        
        'views/plan.xml',
        'reports/report_paperformat.xml',               
        'reports/report_layout.xml',        
        'reports/report_informe.xml',
        'reports/audit_checklist.xml',
        'data/activities.xml',
        'data/descriptions.xml',
    ],
    'assets': {
        'web.report_assets_common': [
                "/tyt_audit/static/src/scss/report_informe.scss",
        ],
    },
    'auto_install': False,
    'installable': True,
    'application': False,
}