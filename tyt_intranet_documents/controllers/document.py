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


class DocumentController(http.Controller):

    def get_all_documents(self, folder):
        all_documents = folder.document_ids
        for child_folder in folder.children_folder_ids:
            all_documents |= self.get_all_documents(child_folder)
        return all_documents

    @api.model
    def _check_folder_access(self, folder):
        now = fields.Datetime.now()
        Access = request.env['documents.access'].sudo()
        accesses = Access.search([
            ('document_id', '=', folder.id),
            ('partner_id', '=', request.env.user.partner_id.id),
            ('role', 'in', ['view', 'edit']),
            '|',
                ('expiration_date', '=', False),
                ('expiration_date', '>', now),
        ], limit=1)
        

        # Si no hay acceso explícito, denegar
        if not accesses:
            return False
        
        return folder.is_intranet_folder and bool(accesses)

    @api.model
    def _check_document_access(self, document):
        if document.folder_id:
            return self._check_folder_access(document.folder_id)
        return False

    @http.route('/documents/folder/share', type='http', auth='user', website=True)
    def documents_folder_share(self):
        values = request.params.copy()
        folders = request.env['documents.document'].sudo().search([('type', '=', 'folder'),('is_intranet_folder', '=', True)])
        accessible_folders = folders.filtered(lambda folder: self._check_folder_access(folder))
        values.update({
            'page_name': 'documents_folder',
            'default_url': '/documents/folder/share',
            'folders': accessible_folders,
        })
        return request.render('tyt_intranet_documents.portal_documents_folder_share', values)

    @http.route('/my/documents/share/<int:folder_id>', type='http', auth='user', website=True)
    def my_documents_share(self, folder_id):
        values = request.params.copy()
        folder = request.env['documents.document'].sudo().browse(folder_id)
        if not folder.exists() or not self._check_folder_access(folder):
            return request.redirect('/my')
        documents = folder.children_ids.filtered(lambda d: d.mimetype == 'application/pdf')
        document_count = len(documents)
        values.update({
            'page_name': 'documents_folder',
            'folder': folder,
            'documents': documents,
            'document_count': document_count,
        })
        return request.render('tyt_intranet_documents.portal_my_documents_share', values)

    @http.route('/my/document/view/<int:document_id>', type='http', auth='user', website=True)
    def my_document_view(self, document_id):
        document = request.env['documents.document'].sudo().browse(document_id)
        if not document.exists() or not self._check_document_access(document):
            return request.redirect('/my')
        values = {
            'page_name': 'document',
            'document': document,
            'url': f'/web/content/{document.id}?model%3Ddocuments.document',
        }
        return request.render('tyt_intranet_documents.portal_my_document_view', values)
