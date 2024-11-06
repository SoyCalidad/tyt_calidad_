from odoo import http
from odoo.http import request
from odoo import api, exceptions, fields, models, _
from datetime import datetime

import json
import logging
import werkzeug

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import fields, http, SUPERUSER_ID, _
from odoo.exceptions import UserError
from odoo.http import request, content_disposition
from odoo.osv import expression
from odoo.tools import format_datetime, format_date, is_html_empty
from odoo.addons.base.models.ir_qweb import keep_query

_logger = logging.getLogger(__name__)


class DocumentController(http.Controller):

    def get_all_documents(self, folder):
        all_documents = folder.document_ids
        for child_folder in folder.children_folder_ids:
            all_documents |= self.get_all_documents(child_folder)
        return all_documents

    @http.route('/documents/folder/share', type='http', auth='user', website=True)
    def documents_folder_share(self):
        values = request.params.copy()
        folders = request.env['documents.folder'].sudo().search([('is_intranet_folder', '=', True)])
        values.update({
            'folders': folders,
        })
        return request.render('tyt_intranet_documents.portal_documents_folder_share', values)

    @http.route('/my/documents/share/<int:folder_id>', type='http', auth='user', website=True)
    def my_documents_share(self, folder_id):
        values = request.params.copy()
        folder = request.env['documents.folder'].sudo().browse(folder_id)
        if not folder.exists():
            return request.redirect('/my')

        documents = folder.document_ids
        document_count = len(documents)
        values.update({
            'folder': folder,
            'documents': documents,
            'document_count': document_count,
        })
        return request.render('tyt_intranet_documents.portal_my_documents_share', values)

    @http.route('/my/document/view/<int:document_id>', type='http', auth='user', website=True)
    def my_document_view(self, document_id):
        values = request.params.copy()
        document = request.env['documents.document'].sudo().browse(document_id)
        values = {
            'page_name': 'document',
            'document': document,
            'url': f'/web/content/{document.id}?model%3Ddocuments.document',
        }

        return request.render('tyt_intranet_documents.portal_my_document_view', values)

    @http.route('/my/document/share/<int:document_id>', type='http', auth='user', website=True)
    def mailbox_form_share(self, document_id):
        values = request.params.copy()
        document = request.env['documents.document'].sudo().browse(document_id)
        values = {
            'page_name': 'document',
            'document': document,
            'url': '/view/document/' + str(document.id),
        }

        return request.render('tyt_intranet_documents.portal_my_document_share_form', values)
