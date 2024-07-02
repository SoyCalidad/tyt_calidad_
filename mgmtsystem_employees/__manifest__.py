# -*- coding: utf-8 -*-
{
    'name': "Management Employees",

    'summary': """
        Incluye capacitaciones y otros""",

    'author': "soycalidad",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['hr_recruitment', 'mgmtsystem_process', 'survey', 'mgmtsystem_legal', 'mgmtsystem_documentary_control'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/res_config_settings.xml',
        'views/plan.xml',
        'views/training.xml',
        'views/employee.xml',
        'views/applicant.xml',
        'views/menus.xml',
        'views/training_onboarding_templates.xml',
        'views/employee_onboarding_templates.xml',
        'report/report_trainings.xml',
        'report/report_employees.xml',
        'report/report_interested.xml',
        'report/report_announcement.xml',
        'report/report_applicant.xml',
        'report/report_applicants_database.xml',
        'report/training_complete_report.xml',
        'report/report_induction.xml',
        'report/training_certificate.xml',
        'data/sequences.xml',
        'data/mail_templates.xml',
        'data/hr.employee.document_type.csv',
        'wizard/training_plan.xml',
        'wizard/announcement.xml',
        'wizard/applicants_database.xml',
        'wizard/training_database.xml',
        'wizard/training_certificate.xml',
        'wizard/induction.xml',
    ],
    'qweb': [
        'static/src/xml/hr_org_chart.xml',
    ],
}
