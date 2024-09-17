{
    'name': 'Reclutamiento TYT Contact Center - Soy Calidad',
    'version': '1.0',
    'description': 'Añade características al módulo Reclutamiento TYT Contact Center',
    'summary': 'Añade características al módulo Reclutamiento TYT Contact Center',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': '',
    'category': 'soycalidad',
    'depends': [
        'hola_calidad',
        'hr_recruitment',
        'report_xlsx',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'data/mail_templates.xml',
        'views/share_templates.xml',
        'reports/reports_xls.xml',
        'reports/reports_pdf.xml',  # Definición del reporte
        'views/template_report_requisition.xml',  # Plantilla QWeb
    ],
    'auto_install': False,
    'installable': True,
    'application': False,

    'assets': {
        'tyt_recruitment.assets_pdfjs_viewer': [
            'tyt_recruitment/static/lib/pdfjs/build/pdf.js',
            'tyt_recruitment/static/lib/pdfjs/build/pdf.worker.js',
            'tyt_recruitment/static/lib/pdfjs/web/viewer.css',
            'tyt_recruitment/static/lib/pdfjs/web/viewer.js',
            'tyt_recruitment/static/lib/pdfjs/web/viewer.html',
            'tyt_recruitment/static/lib/pdfjs/web/cmaps/**',
            'tyt_recruitment/static/lib/pdfjs/web/images/**',
            'tyt_recruitment/static/lib/pdfjs/web/locale/**',
        ],
        'web.assets_backend': [
            '/tyt_recruitment/static/src/img/logo.png',  # Ruta a la imagen
        ],
    },
    'images': ["static/src/img/logo.png"],
}