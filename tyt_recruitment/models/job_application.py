from odoo import api, models, fields

from ..utils.constants import MARITAL_STATUS_SELECTION, GENDER_SELECTION
from ..utils.helpers import get_label_from_marital_status_list, get_label_from_gender_list

import logging
_logger = logging.getLogger(__name__)

class JobApplication(models.Model):
    _name = 'tyt_recruitment.job_application'
    _description = 'tyt_recruitment.job_application'
    _inherit = ['mail.thread']
    _rec_name = 'id'

    request_date = fields.Date(string='Fecha', tracking=True)
    requisition = fields.Char(string='Requisición', tracking=True)
    site = fields.Char(string='Sitio', tracking=True)

    signature_image = fields.Binary(string="Firma del solicitante", tracking=True)

    # Campos relacionados para acceder al nombre y apellidos del aplicante
    applicant_name = fields.Char(related="applicant_id.name", string="Nombre", store=True, tracking=True)
    applicant_last_name_father = fields.Char(related="applicant_id.last_name_father", string="Apellido Paterno", store=True, tracking=True)
    applicant_last_name_mother = fields.Char(related="applicant_id.last_name_mother", string="Apellido Materno", store=True, tracking=True)
    applicant_employee_number = fields.Char(related="applicant_id.employee_number", string="Número de empleado", store=True, tracking=True)
    applicant_number_phone = fields.Char(related="applicant_id.number_phone", string="Teléfono", store=True, tracking=True)
    applicant_birthdate = fields.Date(related="applicant_id.birthdate", string="Fecha de nacimiento", store=True, tracking=True)
    applicant_birthplace = fields.Char(related="applicant_id.birthplace", string="Lugar de nacimiento", store=True, tracking=True)
    applicant_rfc = fields.Char(related="applicant_id.rfc", string="Aplicante RFC", store=True, tracking=True)
    applicant_curp = fields.Char(related="applicant_id.curp", string="Aplicante CURP", store=True, tracking=True)
    applicant_social_security_number = fields.Char(related="applicant_id.social_security_number", string="Aplicante NNS", store=True, tracking=True)       

    campaign_id = fields.Many2one('tyt_recruitment.campaign', string="Campaña", tracking=True)
    campaign_turn = fields.Selection(related="campaign_id.turn", string="Turno", tracking=True)
    recruiter_id = fields.Many2one(related='applicant_id.recruiter_id', string="Reclutador", tracking=True)

    applicant_id = fields.Many2one('tyt_recruitment.applicant', tracking=True)
    applicant_status = fields.Boolean( related="applicant_id.status", string="Aprobado", required=True, tracking=True)

    academics_ids = fields.One2many('tyt_recruitment.data_academic', 'job_application_id', string="Formación académica", tracking=True)
    children_ids = fields.One2many('tyt_recruitment.child', 'job_application_id', string="Hijos", tracking=True)
    answer_ids = fields.One2many('tyt_recruitment.answer', 'job_application_id', string="Respuestas", tracking=True)
    job_history_ids = fields.One2many('tyt_recruitment.job_history', 'job_application_id', string="Historial laboral", tracking=True)
    reference_ids = fields.One2many('tyt_recruitment.reference', 'job_application_id', string="Referencia laboral", tracking=True)

    father_data_id = fields.Many2one('tyt_recruitment.family_data_detail', string="Datos del padre", tracking=True)
    mother_data_id = fields.Many2one('tyt_recruitment.family_data_detail', string="Datos de la madre", tracking=True)
    spouse_data_id = fields.Many2one('tyt_recruitment.family_data_detail', string="Datos del cónyuge", tracking=True)

    complete_survey_id = fields.One2many("tyt_recruitment.complete_survey", 'job_application_id', string="Encuesta de salud", tracking=True)
    has_complete_survey = fields.Boolean(string='Tiene Encuesta Completada', compute='compute_has_complete_survey', tracking=True)

    birth_certificate = fields.Binary(string="Acta de nacimiento", tracking=True)
    birth_certificate_filename = fields.Char(string="Nombre del Archivo - ", tracking=True)
    birth_certificate_state = fields.Boolean(string="Estado - Acta de nacimiento", default=False, tracking=True)
    birth_certificate_approved = fields.Boolean(string="Estado de aprobación - Acta de nacimiento", default=False, tracking=True)

    rfc = fields.Binary(string="RFC", tracking=True)
    rfc_filename = fields.Char(string="Nombre del Archivo - RFC", tracking=True)
    rfc_state = fields.Boolean(string="Estado - RFC", default=False, tracking=True)
    rfc_approved = fields.Boolean(string="Estado de aprobación - RFC", default=False, tracking=True)

    curp = fields.Binary(string="CURP", tracking=True)
    curp_filename = fields.Char(string="Nombre del Archivo - CURP", tracking=True)
    curp_state = fields.Boolean(string="Estado - CURP", default=False, tracking=True)
    curp_approved = fields.Boolean(string="Estado de aprobación - CURP", default=False, tracking=True)

    study_certificate = fields.Binary(string="Comprobante de estudio", tracking=True)
    study_certificate_filename = fields.Char(string="Nombre del Archivo - Comprobante de estudio", tracking=True)
    study_certificate_state = fields.Boolean(string="Estado - Comprobante de estudio", default=False, tracking=True)
    study_certificate_approved = fields.Boolean(string="Estado de aprobación - Comprobante de estudio", default=False, tracking=True)

    proposed_letter = fields.Binary(string="Carta propuesta", tracking=True)
    proposed_letter_filename = fields.Char(string="Nombre del Archivo - Carta propuesta", tracking=True)
    proposed_letter_state = fields.Boolean(string="Estado - Carta propuesta", default=False, tracking=True)
    proposed_letter_approved = fields.Boolean(string="Estado de aprobación - Carta propuesta", default=False, tracking=True)

    ine = fields.Binary(string="INE", tracking=True)
    ine_filename = fields.Char(string="Nombre del Archivo - INE", tracking=True)
    ine_state = fields.Boolean(string="Estado - INE", default=False, tracking=True)
    ine_approved = fields.Boolean(string="Estado de aprobación - INE", default=False, tracking=True)

    reference_validation = fields.Binary(string="Validación de referencias", tracking=True)
    reference_validation_filename = fields.Char(string="Nombre del Archivo - Validación de referencias", tracking=True)
    reference_validation_state = fields.Boolean(string="Estado - Validación de referencias", default=False, tracking=True)
    reference_validation_approved = fields.Boolean(string="Estado de aprobación - Validación de referencias", default=False, tracking=True)
    
    utility_bill = fields.Binary(string="Comprobante de domicilio", tracking=True)
    utility_bill_filename = fields.Char(string="Nombre del Archivo - Comprobante de domicilio", tracking=True)
    utility_bill_state = fields.Boolean(string="Estado - Comprobante de domicilio", default=False, tracking=True)
    utility_bill_approved = fields.Boolean(string="Estado de aprobación - Comprobante de domicilio", default=False, tracking=True)

    psychometric = fields.Binary(string="Psicométrico", tracking=True)
    psychometric_filename = fields.Char(string="Nombre del Archivo - Psicométrico", tracking=True)
    psychometric_state = fields.Boolean(string="Estado - Psicométrico", default=False, tracking=True)
    psychometric_approved = fields.Boolean(string="Estado de aprobación - Psicométrico", default=False, tracking=True)

    snn = fields.Binary(string="SNN", tracking=True)
    snn_filename = fields.Char(string="Nombre del Archivo - SNN", tracking=True)
    snn_state = fields.Boolean(string="Estado - SNN", default=False, tracking=True)
    snn_approved = fields.Boolean(string="Estado de aprobación - SNN", default=False, tracking=True)

    interbank_key = fields.Binary(string="Clabe interbancaria", tracking=True)
    interbank_key_filename = fields.Char(string="Nombre del Archivo - Clabe interbancaria", tracking=True)
    interbank_key_state = fields.Boolean(string="Estado - Clabe interbancaria", default=False, tracking=True)
    interbank_key_approved = fields.Boolean(string="Estado de aprobación - Clabe interbancaria", default=False, tracking=True)

    value_proposition = fields.Binary(string="Propuesta de valor", tracking=True)
    value_proposition_filename = fields.Char(string="Nombre del Archivo - Propuesta de valor", tracking=True)
    value_proposition_state = fields.Boolean(string="Estado - Propuesta de valor", default=False, tracking=True)
    value_proposition_approved = fields.Boolean(string="Estado de aprobación - Propuesta de valor", default=False, tracking=True)

    expedient_status = fields.Boolean(string="Estado 01", default=False, tracking=True)
    status_approved = fields.Float(string="Estado 02", default=0, tracking=True)
    status_loaded = fields.Float(string="Estado 03", default=0, tracking=True)
    
    # health_survey fields fix + job_application fields
    
    health_survey = fields.Binary(string="Encuesta de salud")
    health_survey_filename = fields.Char(string="Nombre del Archivo")
    health_survey_state = fields.Boolean(string="Estado", default=False)
    health_survey_approved = fields.Boolean(string="Estado", default=False)

    job_application = fields.Binary(string="Solicitud de empleo")
    job_application_filename = fields.Char(string="Nombre del Archivo")
    job_application_state = fields.Boolean(string="Estado", default=False)
    job_application_approved = fields.Boolean(string="Estado", default=False)

    ###########################

    @api.onchange(
        'birth_certificate', 
        'rfc', 
        'curp', 
        'study_certificate',
        'proposed_letter',
        'ine',
        'reference_validation',
        'utility_bill',
        'psychometric',
        'snn',
        'interbank_key',
        'value_proposition'
    )
    def _onchange_check_all_files(self):
        
        all_fields_filled = sum([
            bool(self.birth_certificate), 
            bool(self.rfc), 
            bool(self.curp), 
            bool(self.study_certificate),
            bool(self.proposed_letter),
            bool(self.ine),
            bool(self.reference_validation),
            bool(self.utility_bill),
            bool(self.psychometric),
            bool(self.snn),
            bool(self.interbank_key),
            bool(self.value_proposition)
        ])

        self.status_loaded = (all_fields_filled/12)*100
        if all_fields_filled == 12:
            self.expedient_status = True
            self.applicant_id.expedient_status = True
        else:
            self.expedient_status = False
            self.applicant_id.expedient_status = False

    @api.onchange(
        'birth_certificate_approved', 
        'rfc_approved', 
        'curp_approved', 
        'study_certificate_approved',
        'proposed_letter_approved',
        'ine_approved',
        'reference_validation_approved',
        'utility_bill_approved',
        'psychometric_approved',
        'snn_approved',
        'interbank_key_approved',
        'value_proposition_approved'
    )
    def _onchange_check_all_files_approved(self):
        
        all_fields_approved = sum([
            self.birth_certificate_approved, 
            self.rfc_approved, 
            self.curp_approved, 
            self.study_certificate_approved,
            self.proposed_letter_approved,
            self.ine_approved,
            self.reference_validation_approved,
            self.utility_bill_approved,
            self.psychometric_approved,
            self.snn_approved,
            self.interbank_key_approved,
            self.value_proposition_approved
        ])
        self.status_approved = (all_fields_approved/12)*100
        if all_fields_approved == 12:
            self.applicant_id.status = True
        else:
            self.applicant_id.status = False

    def action_open_health_survey(self):

        name = self.applicant_id.name
        last_name_father = self.applicant_id.last_name_father
        last_name_mother = self.applicant_id.last_name_mother
        gender = self.applicant_id.gender
        birthplace = self.applicant_id.birthplace
        birthdate = self.applicant_id.birthdate
        nationality = self.applicant_id.nationality
        age = self.applicant_id.age
        marital_status = self.applicant_id.marital_status

        params = f"gender={gender}&birthplace={birthplace}&birthdate={birthdate}&nationality={nationality}&age={age}&marital_status={marital_status}"
        url = f"/survey/{self.id}/{name}/{last_name_father}/{last_name_mother}?"

        return {
            'type': 'ir.actions.act_url',
            'url': url + params,
            'target': 'new', 
        }

    def action_view_binary_file(self):

        field_name = self.env.context.get('field_name')
        field_f = self.env.context.get('field_f')

        if not field_name or not field_f:
            return
    
        attachment_name = getattr(self, field_name, '')
        attachment = getattr(self, field_f, None)

        url = f'/web/content/{self._name}/{self.id}/{field_f}/{attachment_name}'

        if attachment:
            return {
                'type': 'ir.actions.act_url',
                'url': url,
                'target': 'new',
            }

    @api.depends('complete_survey_id')
    def compute_has_complete_survey(self):
        for record in self:
            record.has_complete_survey = bool(record.complete_survey_id)
            record.applicant_id.has_complete_survey = bool(record.complete_survey_id)

class Applicant(models.Model):
    _name = 'tyt_recruitment.applicant'
    _description = 'tyt_recruitment.applicant'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string="Nombre", tracking=True)
    reference = fields.Char(string="Medio", tracking=True)
    last_name_father = fields.Char(string="Apellido Paterno", tracking=True)
    last_name_mother = fields.Char(string="Apellido Materno", tracking=True)
    birthplace = fields.Char(string="Lugar de Nacimiento", tracking=True)
    birthdate = fields.Date(string="Fecha de Nacimiento", tracking=True)
    nationality = fields.Char(string="Nacionalidad", tracking=True)
    gender = fields.Selection(GENDER_SELECTION, string="Género", tracking=True)
    age = fields.Integer(string="Edad", tracking=True)
    marital_status = fields.Selection(MARITAL_STATUS_SELECTION, string="Estado Civil", tracking=True)
    social_security_number = fields.Char(string="Número de Seguro Social", tracking=True)
    rfc = fields.Char(string="RFC", tracking=True)
    curp = fields.Char(string="CURP", tracking=True)
    address_street = fields.Char(string="Calle y Número", tracking=True)
    address_neighborhood = fields.Char(string="Colonia", tracking=True)
    address_city = fields.Char(string="Municipio", tracking=True)
    number_phone = fields.Char(string="Número de teléfono", tracking=True)
    personal_email = fields.Char(string="Correo electrónico", tracking=True)
    live_with = fields.Char(string="Con quién vive", tracking=True)
    rent_amount = fields.Float(string="Monto semanal de renta", tracking=True)
    infonavit_credit_amount = fields.Float(string="Monto semanal de Infonavit", tracking=True)
    transports = fields.Char(string="Cantidad de transportes y Tiempo de traslado", tracking=True)
    requested_job_position = fields.Char(string="Puesto que solicita", tracking=True)
    monthly_expenses = fields.Float(string="Gastos mensuales aproximados", tracking=True)
    availability = fields.Char(string="Disponibilidad para empezar a trabajar", tracking=True)
    dependents = fields.Char(string="Personas que dependen de ti", tracking=True)
    foreign_nationality = fields.Boolean(string="Cuenta con nacionalidad extranjera", tracking=True)
    daily_activities = fields.Text(string="Describa sus actividades diarias", tracking=True)

    recruiter_comments = fields.Char(string="Comentarios del reclutador", tracking=True)
    recruiter_id = fields.Many2one('hr.employee', string="Reclutador", tracking=True)

    employee_id = fields.Many2one('hr.employee', string="Empleado relacionado", tracking=True)
    employee_number = fields.Char(related="employee_id.x_studio_numero", string="Número de empleado", tracking=True)

    expedient_status = fields.Boolean(string="Estado de carga", default=False, tracking=True)
    has_complete_survey = fields.Boolean(string='Tiene Encuesta Completada', tracking=True)
    status = fields.Boolean(string="Status", tracking=True)

    # Campaña
    campaign_id = fields.Many2one('tyt_recruitment.campaign', string="Campaña", tracking=True)
    campaign_turn = fields.Selection(related="campaign_id.turn", string="Turno", tracking=True)
    campaign_requsition = fields.Many2one(related="campaign_id.requisition_id", string="Requisición", tracking=True)

    days_of_week_ids = fields.One2many("tyt_recruitment.attendance_days_of_week", 'applicant_id', string="Asistencia detalle")

    computed_name = fields.Char(
        string="Nombre completo",
        compute="_compute_full_name"
    )

    @api.depends('name', 'last_name_father', 'last_name_mother')
    def _compute_full_name(self):
        for rec in self:
            rec.computed_name = f"{rec.last_name_father or ''} {rec.last_name_mother or ''} {rec.name or ''}".strip().upper()

    def show_job_application(self):

        job_application = self.env['tyt_recruitment.job_application'].search([('applicant_id', '=', self.id)], limit=1)
        if job_application:
            return {
                'name': 'Vista Form del Registro',
                'type': 'ir.actions.act_window',
                'res_model': 'tyt_recruitment.job_application',
                'view_mode': 'form',
                'res_id': job_application.id,
                'views': [(False, 'form')], 
                'target': 'current',
            }
        else:
            return {
                'type': 'ir.actions.act_window_close'
            }

    def open_requisition_view(self):
        
        if self.campaign_id.requisition_id:
            return {
                'name': 'Vista Form del Registro',
                'type': 'ir.actions.act_window',
                'res_model': 'tyt_recruitment.requisition',
                'view_mode': 'form',
                'res_id': self.campaign_id.requisition_id.id,
                'views': [(False, 'form')], 
                'target': 'current',
            }
        else:
            return {
                'type': 'ir.actions.act_window_close'
            }

    def open_user_input_view(self):
        
        if len(self.days_of_week_ids) == 1:
            _logger.info(f"len(self.days_of_week_ids) : {len(self.days_of_week_ids) }")
            survey_ids = self.days_of_week_ids.attendance_id.surveys_ids.survey_id.ids
            _logger.info(f"survey_ids {len(survey_ids)}")
            question = self.env['survey.question'].sudo().search([
                ('is_a_guest_question', '=', True),
                ('survey_id', 'in', survey_ids)
            ])
            _logger.info(f"question {len(question)}")
            answer = self.env['survey.user_input.line'].sudo().search([
                ('question_id', 'in', question.ids),
                ('value_char_box', '=', self.employee_number)
            ])
            _logger.info(f"answer {len(answer)}")

            inputs = self.env['survey.user_input'].sudo().search([('id', 'in', answer.user_input_id.ids)])
            _logger.info(f"inputs {len(inputs)}")
            if inputs:
                return {
                    'name': 'Lista de encuestas realizadas por el aplicante',
                    'type': 'ir.actions.act_window',
                    'res_model': 'survey.user_input',
                    'view_mode': 'tree',
                    'target': 'current',
                    'domain': [('id', 'in', inputs.ids)]
                }
            else:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Exámenes resueltos',
                        'message': 'Usted ha resuelto 0 exámenes.',
                        'type': 'success',  
                        'sticky': False
                    }
                }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Duplicado',
                    'message': 'Existe más de un registro de asistencia incorrecto, comuníquese con su administrador.',
                    'type': 'success',  
                    'sticky': False
                }
            }
        
class DataAcademic(models.Model):
    _name = 'tyt_recruitment.data_academic'
    _description = 'tyt_recruitment.data_academic'
    _inherit = ['mail.thread']

    degree = fields.Char(string="Último grado de estudios", tracking=True)
    institution = fields.Char(string="Institución académica", tracking=True)
    specification = fields.Char(string="Comprobante de estudio", tracking=True)

    job_application_id = fields.Many2one('tyt_recruitment.job_application', string="Referencias", ondelete='cascade', tracking=True)

class FamilyDataDetail(models.Model):
    _name = 'tyt_recruitment.family_data_detail'
    _description = 'tyt_recruitment.family_data_detail'
    _inherit = ['mail.thread']

    type = fields.Char(string="Tipo", tracking=True)
    name = fields.Char(string="Nombre", tracking=True)
    occupation = fields.Char(string="Ocupación", tracking=True)
    phone_number = fields.Char(string="Teléfono", tracking=True)

class JobHistory(models.Model):
    _name = 'tyt_recruitment.job_history'
    _description = 'tyt_recruitment.job_history'
    _inherit = ['mail.thread']

    company_name = fields.Char(string="Nombre de la compañía", tracking=True)
    start_date = fields.Date(string="Desde", tracking=True)
    end_date = fields.Date(string="Hasta", tracking=True)
    separation_reason = fields.Char(string="Motivo de serparación", tracking=True)
    weekly_salary = fields.Char(string="Salario semanal", tracking=True)

    job_application_id = fields.Many2one('tyt_recruitment.job_application', string="Solicitud", ondelete='cascade', tracking=True)

class JobReference(models.Model):
    _name = 'tyt_recruitment.reference'
    _description = 'tyt_recruitment.reference'
    _inherit = ['mail.thread']

    name = fields.Char(string="Nombre completo", tracking=True)
    type = fields.Char(string="Tipo", tracking=True)
    occupation = fields.Char(string="Ocupación/Giro", tracking=True)
    phone_number = fields.Char(string="Teléfono", tracking=True)

    job_application_id = fields.Many2one('tyt_recruitment.job_application', string="Referencias", ondelete='cascade', tracking=True)

class Child(models.Model):
    _name = 'tyt_recruitment.child'
    _description = 'tyt_recruitment.child'
    _inherit = ['mail.thread']

    name = fields.Char(string="Nombre", tracking=True)
    age = fields.Char(string="Edad", tracking=True) 

    job_application_id = fields.Many2one('tyt_recruitment.job_application', string="Aplicante", ondelete='cascade', tracking=True)