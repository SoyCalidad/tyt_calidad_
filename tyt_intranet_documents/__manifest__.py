{
    'name': 'Intranet Documents TYT Contact Center - Soy Calidad',
    'version': '1.0',
    'description': 'Intranet Documents TYT Contact Center - Soy Calidad',
    'summary': 'Intranet Documents TYT Contact Center - Soy Calidad',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': 'Other proprietary',
    'category': 'soycalidad',
    'depends': [
        'base', 'web', 'documents', 'portal', 'website',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/document_portal_templates.xml',
        'views/documents_folder_views.xml',
        'views/documents_document_views.xml',
    ],
    'assets': {
        'tyt_intranet_documents.assets_pdfjs_viewer': [
            'tyt_intranet_documents/static/lib/pdfjs/build/pdf.js',
            'tyt_intranet_documents/static/lib/pdfjs/build/pdf.worker.js',
            'tyt_intranet_documents/static/lib/pdfjs/web/viewer.css',
            'tyt_intranet_documents/static/lib/pdfjs/web/viewer.js',
            'tyt_intranet_documents/static/lib/pdfjs/web/viewer.html',
            'tyt_intranet_documents/static/lib/pdfjs/web/cmaps/**',
            'tyt_intranet_documents/static/lib/pdfjs/web/images/**',
            'tyt_intranet_documents/static/lib/pdfjs/web/locale/**',
        ],
        'web.assets_backend': [
            'tyt_intranet_documents/static/src/views/inspector/documents_inspector.xml',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
}
