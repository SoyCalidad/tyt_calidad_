# -*- coding: utf-8 -*-

{
    'name': 'HR Organizational Chart',
    'version': '18.0.1.0.1',
    'summary': 'HR Employees organizational chart',
    'description': 'HR Employees organizational chart',
    'author': 'Soy Calidad',
    'company': 'Soy Calidad',
    'category': 'Generic Modules/Human Resources',
    'website': "https://www.openhrms.com",
    'depends': ['hr'],
    'data': [
        'views/show_employee_chart.xml',
    ],
    'assets': {
        'web.assets_backend': [
            #'hr_organizational_chart/static/src/js/organizational_view.js',
            'hr_organizational_chart/static/src/js/organization_dashboard.js',
            'hr_organizational_chart/static/src/scss/chart_view.scss',
            'hr_organizational_chart/static/src/xml/organization_dashboard.xml',
            #'hr_organizational_chart/static/src/**/*',
        ],
    },
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'AGPL-3',
}
