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

    'depends': ['base','hr','hr_recruitment','hr_job_functions','mgmtsystem_process','report_xlsx'],

    'data': [
        'security/ir.model.access.csv',        
        'report/reports_pdf.xml',
        'views/hr_job_form_inherit.xml',
        'views/position_description_template.xml',
        'views/position_description_template_job.xml',
        'data/hr_job_work_day.xml',        
    ],
}