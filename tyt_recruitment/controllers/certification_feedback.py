from odoo import http
from odoo.http import request, Response
import json

import logging
_logger = logging.getLogger(__name__)

from datetime import datetime

class PublicFormController(http.Controller):
    
    @http.route('/certification_feedback/<string:kardex_by_applicant_id>', type='http', auth='public', website=True)
    def public_form(self, kardex_by_applicant_id, **post):
        
        current_date = str(datetime.today().strftime('%Y-%m-%d'))

        kardex = request.env['tyt_recruitment.kardex_by_applicant'].sudo().search([
            ("id", "=", kardex_by_applicant_id)
        ])

        kardex_json = {}
        certification_feedback_json = {}
        if kardex and kardex.attendance_id:

            kardex_json = {
                'applicant_name': kardex.applicant_name or "",
                'campaign': kardex.attendance_id.campaign_id.display_name or "",
                'trainer': kardex.attendance_id.trainer.name or "",
                'group': str(kardex.attendance_id.id) or "",
                'evaluation_average': kardex.average or 0.0,
                'current_date': current_date,
                'kardex_by_applicant_id': kardex_by_applicant_id
            }

            if kardex.certification_feedback_ids[0]:

                _logger.info("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                _logger.info(kardex.certification_feedback_ids[0].strengths)
                _logger.info(kardex.certification_feedback_ids[0].opportunity_areas)
                _logger.info(kardex.certification_feedback_ids[0].suggestions_quality_technician)

                certification_feedback_json = {
                    'strengths': kardex.certification_feedback_ids[0].strengths,
                    'opportunity_areas ': kardex.certification_feedback_ids[0].opportunity_areas,
                    'suggestions_quality_technician': kardex.certification_feedback_ids[0].suggestions_quality_technician
                }

        context = {**kardex_json, **certification_feedback_json}
        
        return request.render('tyt_recruitment.template_certification_feedback_form', context)

    @http.route('/certification_feedback/submit', type='http', auth='public', website=True, csrf=False)
    def submit_form(self, **post):
        
        kardex_by_applicant_id = post.get('kardex_by_applicant_id')

        certification_feedback = request.env['tyt_recruitment.certification_feedback'].sudo().search([
            ("kardex_id", "=", kardex_by_applicant_id)
        ])

        prospectus_commitments = post.get('prospectus_commitments')
        # IMAGE SIGNATURE
        image_base64 = post.get('signature')
        image_data = None

        if image_base64:
            image_data = image_base64.split(",")[1]

        if certification_feedback:
            certification_feedback.sudo().write({
                'prospectus_commitments': prospectus_commitments,
                'applicant_signature': image_data
            })

        return request.render('tyt_recruitment.template_certification_feedback_success')
    