{
    "name": "Customer satisfaction history",
    "author": "soycalidad",
    "category": "Management System",
    "depends": [
        'survey',
        'mgmtsystem_survey',
        'mgmtsystem_nonconformity',
        'mgmtsystem_process',
        'report_xlsx',
        'tyt_survey',
    ],
    "data": [
        'security/ir.model.access.csv',
        'report/customer_satisfaction_history.xml',
        'report/customer_satisfaction_cx.xml',
        'wizards/satisfaction_survey_history.xml',
    ],
    'installable': True,
}
