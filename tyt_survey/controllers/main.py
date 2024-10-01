# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import werkzeug
import base64
from odoo import http, _
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.web.controllers.main import ensure_db, Home
from odoo.addons.base_setup.controllers.main import BaseSetup
from odoo.exceptions import UserError
from odoo.http import request
import datetime

_logger = logging.getLogger(__name__)


class TYTSatisfactionSurvey(http.Controller):

    @http.route('/website/satisfaction_survey', type='http', auth='public', website=True, sitemap=False)
    def satisfaction_survey_main(self, *args, **kw):
        values = request.params.copy()
        response = request.render('tyt_survey.satisfaction_survey_main', values)
        return response
    
    @http.route('/website/survey/satisfaction_survey', type='http', auth='public', website=True, sitemap=False)
    def satisfaction_survey(self, *args, **kw):
        values = request.params.copy()
        response = request.render('tyt_survey.satisfaction_survey', values)
        return response
    
    @http.route('/website/survey/satisfaction_survey_done', type='http', methods=['POST'], auth='public', website=True, sitemap=False)
    def satisfaction_survey_done(self, *args, **kw):
        values = request.params.copy()
        print (args, kw)
        response = request.render('tyt_survey.satisfaction_survey_done', values)
        
        satisfaction_survey_model = request.env['tyt.satisfaction.survey']
        satisfaction_survey_question_model = request.env['tyt.satisfaction.survey.question']
        
        values = {}
        
        values['partner_name'] = kw['partner_name']
        values['job'] = kw['job']
        values['email'] = kw['email']
        values['partner_company'] = kw['partner_company']
        values['campaign'] = kw['campaign']
        
        lines = [(5, 0, 0)]
        
        cat_text_fields = ['cat_1_4', 'cat_2_3', 'cat_3_4', 'cat_4_3', 'cat_5_4', 'cat_6_3', 'cat_7_3', 'cat_7_4']
        
        for key, value in kw.items():            
            if 'cat_' in key:
                
                question_id = satisfaction_survey_question_model.search([('code', '=', key)])
                
                question_values = {
                    'name': question_id.name,
                    'code': question_id.code,
                    'qualification': value if key not in cat_text_fields else False,
                    'text': value if key in cat_text_fields else False,
                }
                
                lines.append((0, 0, question_values))
                
        print (lines)
        
        values['line_ids'] = lines
        
        satisfaction_survey_model.create(values)
        
        return response
