from odoo import http
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class RecruitmentController(http.Controller):

    @http.route(['/recruitment/<int:requisition_id>/<token>'], type='http', auth='user', website=True)
    def share_requisition(self, requisition_id, token):
        requisition_temp = request.env['tyt_recruitment.requisition'].sudo().browse(requisition_id)
        if not requisition_temp.exists() or requisition_temp.access_token != token:
            return request.not_found()

        return request.render('tyt_recruitment.edition_share_template', {
            'pdf_filename': f'{requisition_temp.weeks}.pdf',
            'pdf_url': f'/recruitment/download/{requisition_temp.id}'
        })

    @http.route('/recruitment/download/<int:requisition_id>', type='http', auth='user')
    def download_requisition(self, requisition_id):
        
        requisition_temp = request.env['tyt_recruitment.requisition'].sudo().browse(requisition_id)
        
        if not requisition_temp.exists():
            return request.not_found()


        pdf_content, _ = request.env['ir.actions.report'].sudo()._render_qweb_pdf(
            'tyt_recruitment.action_report_requisition_pdf', [requisition_temp.id]
        )
        pdf_filename = f'{requisition_temp.weeks}.pdf'
        headers = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf_content)),
            ('Content-Disposition', f'inline; filename="{pdf_filename}"')
        ]
        return request.make_response(pdf_content, headers=headers)
