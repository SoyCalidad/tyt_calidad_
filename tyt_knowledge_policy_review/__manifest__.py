# -*- coding: utf-8 -*-
{
    'name': "Knowledge and Policy Review",

    'summary': """
        Knowledge and Policy Review""",

    'description': """
    """,

    'author': "soycalidad",

    'category': 'Uncategorized',
    'license': 'Other proprietary',
    'version': '0.1',

    'depends': ['base','survey','hr','marketing_automation','report_xlsx'],

    'data': [
        'security/ir.model.access.csv',
        'views/survey_survey_view.xml',
        'report/reports_pdf.xml',
        'views/survey_report_template.xml',
    ],
}