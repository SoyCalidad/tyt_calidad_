from odoo import http
from odoo.http import request


class ShareController(http.Controller):

    @http.route(['/edition/share/<int:edition_id>/<token>'], type='http', auth='user', website=True)
    def share_edition(self, edition_id, token):
        edition = request.env['process.edition'].sudo().browse(edition_id)
        if not edition.exists() or edition.access_token != token:
            return request.not_found()

        return request.render('tyt_share.edition_share_template', {
            'pdf_filename': f'{edition.name}.pdf',
            'pdf_url': f'/edition/download/{edition.id}'
        })

    @http.route('/edition/download/<int:edition_id>', type='http', auth='user')
    def download_edition(self, edition_id):
        edition = request.env['process.edition'].sudo().browse(edition_id)
        if not edition.exists():
            return request.not_found()

        pdf_content, _ = request.env['ir.actions.report'].sudo()._render_qweb_pdf(
            'mgmtsystem_process.report_process_edition', [edition.id]
        )
        pdf_filename = f'{edition.name}.pdf'
        headers = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf_content)),
            ('Content-Disposition', f'inline; filename="{pdf_filename}"')
        ]
        return request.make_response(pdf_content, headers=headers)
