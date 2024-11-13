# -*- coding: utf-8 -*-
{
    'name': "Position Description",

    'summary': """
        Position Description""",

    'description': """
    """,

    'author': "soycalidad",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','hr','hr_recruitment','report_xlsx'],

    'data': [
        'security/ir.model.access.csv',        
        'report/reports_pdf.xml',
        'views/hr_job_form_inherit.xml',
        'views/hr_job_form_inherit_2.xml',
        'views/position_description_template.xml',
        'data/hr_job_work_day.xml',        
    ],
}