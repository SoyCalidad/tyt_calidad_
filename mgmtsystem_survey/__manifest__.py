# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Management System Encuestas",
    "author": "HC",
    "category": "Management System",
    "depends": [
        'survey',
        'mgmtsystem_nonconformity',
        'mgmtsystem_process',
        'report_xlsx',
    ],
    "data": [
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        'data/survey_stage.xml',
        'views/survey_views.xml',
        'views/survey_onboarding_templates.xml',
        'report/report_survey.xml',
        'report/report_survey_report.xml',
        'report/survey_database.xml',
    ],
    'installable': True,
}
