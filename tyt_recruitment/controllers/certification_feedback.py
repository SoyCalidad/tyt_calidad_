from odoo import http
from odoo.http import request, Response
import json

import logging
_logger = logging.getLogger(__name__)

from datetime import datetime

class PublicFormController(http.Controller):
    
    @http.route('/certification_feedback/<string:attendance_id>', type='http', auth='public', website=True)
    def public_form(self, attendance_id, **post):
        
        applicant_name = post.get('applicant_name')
        campaign = post.get('campaign')
        trainer = post.get('trainer')
        group = post.get('group')
        current_date = str(datetime.today().strftime('%Y-%m-%d'))

        _logger.info(f"Attendance ID: {attendance_id}")
        _logger.info(f"applicant_name {applicant_name}")
        _logger.info(f"campaign {campaign}")
        _logger.info(f"trainer {trainer}")
        _logger.info(f"group {group}")
        _logger.info(f"current_date {current_date}")

        components = request.env['tyt_recruitment.component_feeback'].sudo().search([])

        components_json = [{'id': str(q.id), 'text': q.text} for q in components]

        context = {
            'applicant_name': applicant_name,
            'campaign': campaign,
            'trainer': trainer,
            'group': group,
            'current_date': current_date,
            'attendance_id': attendance_id,
            'components_json': components_json
        }

        return request.render('tyt_recruitment.template_certification_feedback_form', context)
    