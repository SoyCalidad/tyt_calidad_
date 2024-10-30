from odoo import http
from odoo.http import request, Response
import json

import logging
_logger = logging.getLogger(__name__)

class PublicFormController(http.Controller):
    
    @http.route('/survey/<string:job_application_id>', type='http', auth='public', website=True)
    def public_form(self, job_application_id):
        
        health_questions = self.get_questions('EC01')
        health_questions_json = [{
            'id': str(q.id), 
            'title': q.title, 
            'question_type': q.question_type, 
            'options': [{'value':o.value, 'id': o.id} for o in q.suggested_answer_ids], 
            'option_values': [ov.value for ov in q.matrix_row_ids]
        } for q in health_questions]

        context = {
            'health_questions_json': health_questions_json,
            'job_application_id': job_application_id
        }

        return request.render('tyt_recruitment.template_health_survey_form', context)
    
    @http.route('/health_survey/submit', type='http', auth='public', website=True, csrf=False)
    def submit_form(self, **post):

        job_application_id = request.params.get('custom_value')
        health_questions = self.get_questions('EC01')

        # health_asnwer_json = [{
        #     'text': post.get(str(q.id)), 
        #     'question_id': q.id
        # } for q in health_questions]

        complete_survey_data = {
            'state': 'Enviado',
            'job_application_id': job_application_id
        }

        complete_survey = request.env['tyt_recruitment.complete_survey'].sudo().create(complete_survey_data)

        health_asnwer_json = []
        answer_data = {}
        for question in health_questions:
            if question.question_type == 'multiple_choice':
                answer_data = {
                    'text': post.get(str(question.id)), 
                    'question_id': question.id,
                    'complete_survey_id': complete_survey.id
                }
                for answer in question.suggested_answer_ids:
                    _logger.info("----------------------------ans")
                    _logger.info(answer.id)
                    _logger.info(post.get(str(answer.id)))
                    answer_data = {
                        'text': answer.value, 
                        'question_id': question.id,
                        'complete_survey_id': complete_survey.id
                    }
                    health_asnwer_json.append(answer_data)
            elif question.question_type == 'matrix':
                pass
            else:
                answer_data = {
                    'text': post.get(str(question.id)), 
                    'question_id': question.id,
                    'complete_survey_id': complete_survey.id
                }
                health_asnwer_json.append(answer_data)
            request.env['tyt_recruitment.survey_answer'].sudo().create(answer_data)

        # for answer in health_asnwer_json:
        #     request.env['tyt_recruitment.answer'].sudo().create(answer)

        return Response(
            json.dumps(health_asnwer_json), 
            content_type='application/json;charset=utf-8'
        )

    def get_questions(self, code):
        questions = request.env['survey.question'].sudo().search([
            ('health_survey_id', '!=', False),
            ('health_survey_id.code', '=', code)
        ])
        return questions