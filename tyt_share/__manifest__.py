{
    'name': 'Share TYT Contact Center',
    'version': '1.0',
    'description': 'Share TYT Contact Center',
    'summary': 'Share TYT Contact Center',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': '',
    'category': 'soycalidad',
    'depends': [
        'mgmtsystem_process',
    ],
    'data': [
        'data/mail_template_data.xml',
        'views/share_templates.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,

    'assets': {
        'tyt_share.assets_pdfjs_viewer': [
            'tyt_share/static/lib/pdfjs/build/pdf.js',
            'tyt_share/static/lib/pdfjs/build/pdf.worker.js',
            'tyt_share/static/lib/pdfjs/web/viewer.css',
            'tyt_share/static/lib/pdfjs/web/viewer.js',
            'tyt_share/static/lib/pdfjs/web/viewer.html',
            'tyt_share/static/lib/pdfjs/web/cmaps/**',
            'tyt_share/static/lib/pdfjs/web/images/**',
            'tyt_share/static/lib/pdfjs/web/locale/**',
        ],

    },
}
