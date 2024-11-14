from odoo import http
from odoo.http import request, Response
import json

class PublicFormController(http.Controller):
    
    @http.route('/job_application/<string:requisition_id>', type='http', auth='public', website=True)
    def public_form(self, requisition_id, **post):
        
        site_id = post.get('site_name')
        tag_name = post.get('tag_name')
        campaign_id = post.get('campaign_id')

        health_questions = self.get_questions('enable', 'health');
        job_questions = self.get_questions('enable', 'job');
        study_questions = self.get_questions('enable', 'study');

        health_questions_json = [{'id': str(q.id), 'text': q.text} for q in health_questions]
        job_questions_json = [{'id': str(q.id), 'text': q.text} for q in job_questions]
        study_questions_json = [{'id': str(q.id), 'text': q.text} for q in study_questions]

        context = {
            'requisition_id': requisition_id,
            'tag_name': tag_name,
            'campaign_id': campaign_id,
            'site_id': site_id,
            'health_questions_json': health_questions_json,
            'job_questions_json': job_questions_json,         
            'study_questions_json': study_questions_json
        }

        return request.render('tyt_recruitment.template_job_application_form', context)

    @http.route('/job_application/submit', type='http', auth='public', website=True, csrf=False)
    def submit_form(self, **post):
        
        # MEDIA REFERENCE
        ref = post.get('reference')
        if not ref:
            ref = post.get('other_reference')

        # CREATING APPLICANT DATA
        data_applicant = {
            'reference': ref,
            'name': post.get('name'),
            'last_name_father': post.get('last_name_father'),
            'last_name_mother': post.get('last_name_mother'),
            'birthplace': post.get('birthplace'),
            'birthdate': post.get('birthdate'),
            'nationality': post.get('nationality'),
            'gender': post.get('gender'),
            'age': post.get('age'),
            'marital_status': post.get('marital_status'),
            'social_security_number': post.get('social_security_number'),
            'rfc': post.get('rfc'),
            'curp': post.get('curp'),
            'address_street': post.get('address_street'),
            'address_neighborhood': post.get('address_neighborhood'),
            'address_city': post.get('address_city'), 
            'number_phone': post.get('number_phone'),
            'personal_email': post.get('personal_email'),
            'live_with': post.get('live_with'), 
            'rent_amount': post.get('rent_amount'), 
            'infonavit_credit_amount': post.get('infonavit_credit_amount'),
            'transports': post.get('transports'),
            'requested_job_position': post.get('requested_job_position'),
            'monthly_expenses': post.get('monthly_expenses'), 
            'availability': post.get('availability'), 
            'dependents': post.get('dependents'),
            'foreign_nationality': post.get('foreign_nationality'), 
            'daily_activities': post.get('daily_activities'),
            'campaign_id': post.get('campaign_id')
        }
        applicant = request.env['tyt_recruitment.applicant'].sudo().create(data_applicant)

        # CREATING PARENTS
        data_father = {
            'type': post.get('typef_1'),
            'name': post.get('fullnamef_1'),
            'occupation': post.get('ocupationf_1'),
            'phone_number': post.get('phonef_1')
        }
        father = request.env['tyt_recruitment.family_data_detail'].sudo().create(data_father)

        data_mother = {
            'type': post.get('typef_2'),
            'name': post.get('fullnamef_2'),
            'occupation': post.get('ocupationf_2'),
            'phone_number': post.get('phonef_2')
        }
        mother = request.env['tyt_recruitment.family_data_detail'].sudo().create(data_mother)

        data_spouse = {
            'type': post.get('typef_3'),
            'name': post.get('fullnamef_3'),
            'occupation': post.get('ocupationf_3'),
            'phone_number': post.get('phonef_3')
        }
        spouse = request.env['tyt_recruitment.family_data_detail'].sudo().create(data_spouse)

        # IMAGE SIGNATURE

        image_base64 = post.get('signature')
        image_data = None

        if image_base64:
            # Remueve el prefijo "data:image/png;base64," si existe
            image_data = image_base64.split(",")[1]

        # CREATING JOB APPLICATION
        data_job_application = {
            'request_date': post.get('request_date'),
            'requisition': post.get('requisition'), 
            'site': post.get('site'), 

            'campaign_id': post.get('campaign_id'),
            'applicant_id': applicant.id,

            'father_data_id': father.id,
            'mother_data_id': mother.id,
            'spouse_data_id': spouse.id,

            'signature_image': image_data
        }

        job_application = request.env['tyt_recruitment.job_application'].sudo().create(data_job_application)

        # CREATING ACADEMIC DATA

        data_academic = {
            'degree': post.get('degree'),
            'institution': post.get('institution'),
            'specification': post.get('specification'),
            'job_application_id': job_application.id
        }
        request.env['tyt_recruitment.data_academic'].sudo().create(data_academic)

        # CREATING ANWERS
        health_questions = self.get_questions('enable', 'health');
        job_questions = self.get_questions('enable', 'job');
        study_questions = self.get_questions('enable', 'study');

        health_asnwer_json = [{'text': post.get(str(q.id)), 'job_application_id': job_application.id, 'question_id': q.id} for q in health_questions]

        for answer in health_asnwer_json:
            request.env['tyt_recruitment.answer'].sudo().create(answer)

        job_asnwer_json = [{'text': post.get(str(q.id)), 'job_application_id': job_application.id, 'question_id': q.id} for q in job_questions]

        for answer in job_asnwer_json:
            request.env['tyt_recruitment.answer'].sudo().create(answer)

        study_asnwer_json = [{'text': post.get(str(q.id)), 'job_application_id': job_application.id, 'question_id': q.id} for q in study_questions]

        for answer in study_asnwer_json:
            request.env['tyt_recruitment.answer'].sudo().create(answer)

        # JOB HISTORY

        company_names = request.httprequest.form.getlist('company_name[]')
        start_dates = request.httprequest.form.getlist('start_date[]')
        end_dates = request.httprequest.form.getlist('end_date[]')
        separation_reasons = request.httprequest.form.getlist('separation_reason[]')
        weekly_salarys = request.httprequest.form.getlist('weekly_salary[]')

        for index, company_name in enumerate(company_names):
            new_history = {
                'company_name': company_name,
                'start_date': str(start_dates[index]),
                'end_date': str(end_dates[index]),
                'separation_reason': separation_reasons[index],
                'weekly_salary': weekly_salarys[index],
                'job_application_id': job_application.id,
            }
            request.env['tyt_recruitment.job_history'].sudo().create(new_history)

        # JOB REFERENCES
        reference_types = request.httprequest.form.getlist('reference_type[]')
        reference_names = request.httprequest.form.getlist('reference_name[]')
        references_occupations = request.httprequest.form.getlist('references_occupation[]')
        references_phones = request.httprequest.form.getlist('references_phone[]')

        for index, name in enumerate(reference_names):
            new_reference = {
                'name': name,
                'type': reference_types[index],
                'occupation': references_occupations[index],
                'phone_number': references_phones[index],
                'job_application_id': job_application.id,
            }
            request.env['tyt_recruitment.reference'].sudo().create(new_reference)

         # CREATING CHILDREN


        # data = {
        #     # 'data_applicant': data_applicant,

        #     # 'health_asnwer_json': health_asnwer_json,
        #     # 'study_asnwer_json': study_asnwer_json,
        #     # 'job_asnwer_json': job_asnwer_json,
            
        #     'data_academic': data_academic,
        #     'data_father': data_father,
        #     'data_mother': data_mother,
        #     'data_spouse': data_spouse

        #     # 'data_job_application': data_job_application,
        # }

        context = {
            'job_application_id': job_application.id,
            'name': applicant.name,
            'last_name_father': applicant.last_name_father,
            'last_name_mother': applicant.last_name_mother,
            'gender': 'gender',
            'birthplace': applicant.birthplace,
            'birthdate': applicant.birthdate,
            'nationality': applicant.nationality,
            'age': applicant.age,
            'marital_status': applicant.marital_status
        }

        return request.render('tyt_recruitment.template_job_application_success', context)
    
    @http.route('/fields/<string:model_name>', type='http', auth='public')
    def list_fields_generic(self, model_name):
        # Accede al entorno de Odoo
        fields = http.request.env[model_name]._fields
        field_names = [field for field in fields]
        return "<br/>".join(field_names)
    
    @http.route('/job_application/list', type='http', auth='public')
    def list_fields_job_application(self):
        applications = request.env['tyt_recruitment.job_application'].sudo().search([])
        json_data = [{
            'id': a.id, 
            'request_date': str(a.request_date), 
            'requisition': a.requisition, 
            'campaign': a.campaign_id.id, 
            'site': a.site,
            'applicant': a.applicant_id.id
            } for a in applications]

        return Response(
            json.dumps(json_data), 
            content_type='application/json;charset=utf-8'
        )
    
    @http.route('/applicant/list', type='http', auth='public')
    def list_fields_applicant(self):
        # ('campaign_id', '=', int(tag_id))
        applicants = request.env['tyt_recruitment.applicant'].sudo().search([])

        json_data = [{
            'id': a.id, 
            'name': a.name, 
            'last_name_father': a.last_name_father, 
            'last_name_mother': a.last_name_mother, 
            'birthplace': str(a.birthplace),
            'applicant': a.campaign_id.id
            } for a in applicants]
        
        return Response(
            json.dumps(json_data), 
            content_type='application/json;charset=utf-8'
        )

    def get_questions(self, state, type):
        questions = request.env['tyt_recruitment.question'].sudo().search([
            ('state', '=', state),
            ('type', '=', type)
        ])
        return questions

    @http.route('/job_applications', type='http', auth='public')
    def list_fields_applicant(self):
        
        context = {
            'job_application_id': 222,
            'name': 'name',
            'last_name_father': 'last_name_father',
            'last_name_mother': 'last_name_mother',
            'gender': 'gender',
            'birthplace': 'birthplace',
            'birthdate': 'birthdate',
            'nationality': 'nationality',
            'age': 'age',
            'marital_status': 'marital_status'
        }
        return request.render('tyt_recruitment.template_job_application_success', context)