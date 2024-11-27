from odoo import http
from odoo.http import request, Response
import json
import base64

from ..utils.helpers import get_label_from_gender_list, get_label_from_marital_status_list

import logging
_logger = logging.getLogger(__name__)

class PublicFormController(http.Controller):
    
    @http.route('/survey/<string:job_application_id>/<string:name>/<string:last_name_father>/<string:last_name_mother>', type='http', auth='public', website=True)
    def public_form(self, job_application_id, name, last_name_father, last_name_mother, **post):
    
        health_questions = self.get_questions('EC01')
        health_questions_json = [{
            'id': str(q.id), 
            'title': q.title, 
            'question_type': q.question_type, 
            'options': [{'value':o.value, 'id': o.id} for o in q.suggested_answer_ids], 
            'option_values': [ov.value for ov in q.matrix_row_ids],
            'extra_input': q.extra_input,
            'extra_input_enabled': q.extra_input_enabled
        } for q in health_questions]

        gender_label = get_label_from_gender_list(post.get('gender'))
        marital_status_label = get_label_from_marital_status_list(post.get('marital_status'))

        context = {
            'health_questions_json': health_questions_json,
            'job_application_id': job_application_id,
            'name': name,
            'last_name_father': last_name_father,
            'last_name_mother': last_name_mother,
            'gender': gender_label,
            'birthplace': post.get('birthplace'),
            'birthdate': post.get('birthdate'),
            'nationality': post.get('nationality'),
            'age': post.get('age'),
            'marital_status': marital_status_label
        }

        return request.render('tyt_recruitment.template_health_survey_form', context)
    
    @http.route('/health_survey/submit', type='http', auth='public', website=True, csrf=False)
    def submit_form(self, **post):

        job_application_id = request.params.get('job_application_id')
        health_questions = self.get_questions('EC01')

        # health_asnwer_json = [{
        #     'text': post.get(str(q.id)), 
        #     'question_id': q.id
        # } for q in health_questions]

        image_base64 = post.get('signature')
        image_data = None

        if image_base64:
            # Remueve el prefijo "data:image/png;base64," si existe
            image_data = image_base64.split(",")[1]

        complete_survey_data = {
            'state': 'sent',
            'signature_image': image_data,
            'job_application_id': job_application_id
        }

        complete_survey = request.env['tyt_recruitment.complete_survey'].sudo().create(complete_survey_data)
        _logger.info("----------------------------complete_survey")
        _logger.info(complete_survey)
        _logger.info(complete_survey.signature_image)
        health_asnwer_json = []
        answer_data = {}
        for question in health_questions:
            if question.question_type == 'multiple_choice':
                _logger.info("----------------------------aaaaaaaaaaaa")
                _logger.info(post.get("extra_"+str(question.id)))
                _logger.info(post.get("extra_"+str(question.id)))
                _logger.info(question.id)
                answer_data = {
                    'text': post.get(str(question.id)), 
                    'question_id': question.id,
                    'complete_survey_id': complete_survey.id,
                    'extra_text': post.get("extra_"+str(question.id))
                }
                for answer in question.suggested_answer_ids:
                    _logger.info("----------------------------ans")
                    _logger.info(answer.id)
                    _logger.info(post.get(str(answer.id)))
                    answer_data = {
                        'text': answer.value, 
                        'question_id': question.id,
                        'complete_survey_id': complete_survey.id,
                        'extra_text': post.get("extra_"+str(question.id))
                    }
                    health_asnwer_json.append(answer_data)
            elif question.question_type == 'matrix':
                pass
            else:
                answer_data = {
                    'text': post.get(str(question.id)), 
                    'question_id': question.id,
                    'complete_survey_id': complete_survey.id,
                    'extra_text': post.get("extra_"+str(question.id))
                }
                health_asnwer_json.append(answer_data)
            request.env['tyt_recruitment.survey_answer'].sudo().create(answer_data)

        return request.render('tyt_recruitment.template_health_survey_success')

    def get_questions(self, code):
        questions = request.env['survey.question'].sudo().search([
            ('health_survey_id', '!=', False),
            ('health_survey_id.code', '=', code)
        ])
        return questions