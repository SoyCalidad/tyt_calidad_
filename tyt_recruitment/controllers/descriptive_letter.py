from odoo import http
from odoo.http import request, Response
import json

import logging
_logger = logging.getLogger(__name__)

from datetime import datetime

class DescriptiveLetter(http.Controller):
    
    @http.route('/descriptive_letter/<string:template_name>/<string:template_id>/<string:letter_id>', type='http', auth='public', website=True)
    def public_form(self, template_name, template_id, letter_id, **post):
        
        descriptive_letter = request.env['tyt_recruitment.descriptive_letter'].sudo().browse(int(template_id))

        context_framing = {}
        if descriptive_letter.framing_topic_ids:
            context_framing = {
                "letter_id": letter_id,
                "template_id": template_id,
                "framing_topics": [
                    {
                        "id": topic.id,
                        "name": topic.name,
                        "topic_style": f"height:{len(topic.framing_subtopic_ids)*100}px", 
                        "framing_subtopics": [
                            {
                                "id": subtopic.id,
                                "name": subtopic.name,
                                "instructor_learning_activities": subtopic.instructor_learning_activities,
                                "participant_learning_activities": subtopic.participant_learning_activities,
                                "instructional_techniques": subtopic.instructional_techniques,
                                "group_techniques": subtopic.group_techniques,
                                "evaluation": subtopic.evaluation,
                                "required_material": subtopic.required_material,
                                "time": subtopic.time,
                                "subtopic_style": "height:100px", 
                            } for subtopic in topic.framing_subtopic_ids
                        ]
                    } for topic in descriptive_letter.framing_topic_ids
                ]
            }
        
        context_days = {}
        if descriptive_letter.day_ids:
            context_days = {
                "days": [
                    {
                        "id": day.id,
                        "name": day.name, 
                        "framing_topics": [
                            {
                                "id": topic.id,
                                "name": topic.name,
                                "topic_style": f"height:{len(topic.subtopic_ids)*100}px", 
                                "framing_subtopics": [
                                    {
                                        "id": subtopic.id,
                                        "name": subtopic.name,
                                        "instructor_learning_activities": subtopic.instructor_learning_activities,
                                        "participant_learning_activities": subtopic.participant_learning_activities,
                                        "instructional_techniques": subtopic.instructional_techniques,
                                        "group_techniques": subtopic.group_techniques,
                                        "evaluation": subtopic.evaluation,
                                        "required_material": subtopic.required_material,
                                        "time": subtopic.time,
                                        "subtopic_style": "height:100px", 
                                    } for subtopic in topic.subtopic_ids
                                ]
                            } for topic in day.topic_ids
                        ]
                    } for day in descriptive_letter.day_ids
                ]
            }

        context = {**context_framing, **context_days}

        if template_name == "template":
            return request.render('tyt_recruitment.template_descriptive_letter_template_form', context)
        elif template_name == "descriptive_letter":
            return request.render('tyt_recruitment.template_descriptive_letter_form', context)
        else:
            return {}
        

    @http.route('/descriptive_letter/submit/<string:template_id>/<string:letter_id>', type='http', auth='public', website=True, csrf=False)
    def submit_form(self, template_id, letter_id, **post):
        
        _logger.info("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbb")
        _logger.info(template_id)
        _logger.info(letter_id)

        descriptive_letter_template = request.env['tyt_recruitment.descriptive_letter'].sudo().browse(int(template_id))
        descriptive_letter = request.env['tyt_recruitment.descriptive_letter_input'].sudo().browse(int(letter_id))

        for topic in descriptive_letter_template.framing_topic_ids:

            topic_data = {
                'name': topic.name,
                'descriptive_letter_input_id': descriptive_letter.id
            }

            new_topic = request.env['tyt_recruitment.descriptive_letter_framing_topic'].sudo().create(topic_data)

            for subtopic in topic.framing_subtopic_ids:
                subtopic_data = {
                    'name': post.get(f'name_{subtopic.id}'),
                    'instructor_learning_activities': post.get(f'instructor_learning_activities_{subtopic.id}'),
                    'participant_learning_activities': post.get(f'participant_learning_activities_{subtopic.id}'),
                    'instructional_techniques': post.get(f'instructional_techniques_{subtopic.id}'),
                    'group_techniques': post.get(f'group_techniques_{subtopic.id}'),
                    'evaluation': post.get(f'evaluation_{subtopic.id}'),
                    'required_material': post.get(f'required_material_{subtopic.id}'),
                    'time': post.get(f'time_{subtopic.id}'),
                    'framing_topic_id': new_topic.id
                }
                
                request.env['tyt_recruitment.descriptive_letter_framing_subtopic'].sudo().create(subtopic_data)

        for day in descriptive_letter_template.day_ids:

            day_data = {
                'name': day.name,
                'descriptive_letter_input_id': descriptive_letter.id
            }

            new_day = request.env['tyt_recruitment.descriptive_letter_day'].sudo().create(day_data)

            for topic in day.topic_ids:
                topic_data = {
                    'name': topic.name,
                    'day_id': new_day.id
                }

                new_topic = request.env['tyt_recruitment.descriptive_letter_topic'].sudo().create(topic_data)

                for subtopic in topic.subtopic_ids:
                    subtopic_data = {
                        'name': post.get(f'name{subtopic.id}'),
                        'instructor_learning_activities': post.get(f'instructor_learning_activities_{subtopic.id}'),
                        'participant_learning_activities': post.get(f'participant_learning_activities_{subtopic.id}'),
                        'instructional_techniques': post.get(f'instructional_techniques_{subtopic.id}'),
                        'group_techniques': post.get(f'group_techniques_{subtopic.id}'),
                        'evaluation': post.get(f'evaluation_{subtopic.id}'),
                        'required_material': post.get(f'required_material_{subtopic.id}'),
                        'time': post.get(f'time_{subtopic.id}'),
                        'topic_id': new_topic.id
                    }
                    
                    request.env['tyt_recruitment.descriptive_letter_subtopic'].sudo().create(subtopic_data)

        return request.render('tyt_recruitment.template_descriptive_letter_success')

    def get_questions(self, code):
        questions = request.env['survey.question'].sudo().search([
            ('health_survey_id', '!=', False),
            ('health_survey_id.code', '=', code)
        ])
        return questions