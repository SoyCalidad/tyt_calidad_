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

    request_date = fields.Date(string='Fecha')
    requisition = fields.Char(string='Requisición')
    site = fields.Char(string='Sitio')

    signature_image = fields.Binary(string="Firma del solicitante")

    # Campos relacionados para acceder al nombre y apellidos del aplicante
    applicant_name = fields.Char(related="applicant_id.name", string="Nombre", store=True)
    applicant_last_name_father = fields.Char(related="applicant_id.last_name_father", string="Apellido Paterno", store=True)
    applicant_last_name_mother = fields.Char(related="applicant_id.last_name_mother", string="Apellido Materno", store=True)
    applicant_employee_number = fields.Char(related="applicant_id.employee_number", string="Número de empleado", store=True)
    applicant_number_phone = fields.Char(related="applicant_id.number_phone", string="Teléfono", store=True)
    applicant_birthdate = fields.Date(related="applicant_id.birthdate", string="Fecha de nacimiento", store=True)
    applicant_birthplace = fields.Char(related="applicant_id.birthplace", string="Lugar de nacimiento", store=True)
    applicant_rfc = fields.Char(related="applicant_id.rfc", string="Aplicante RFC", store=True)
    applicant_curp = fields.Char(related="applicant_id.curp", string="Aplicante CURP", store=True)
    applicant_social_security_number = fields.Char(related="applicant_id.social_security_number", string="Aplicante NNS", store=True)       

    campaign_id = fields.Many2one('tyt_recruitment.campaign', string="Campaña")
    campaign_turn = fields.Selection(related="campaign_id.turn", string="Turno")
    recruiter_id = fields.Many2one(related='applicant_id.recruiter_id', string="Reclutador")

    applicant_id = fields.Many2one('tyt_recruitment.applicant')
    applicant_status = fields.Boolean( related="applicant_id.status", string="Aprobado", required=True, tracking=True)

    academics_ids = fields.One2many('tyt_recruitment.data_academic', 'job_application_id', string="Formación académica")
    children_ids = fields.One2many('tyt_recruitment.child', 'job_application_id', string="Hijos")
    answer_ids = fields.One2many('tyt_recruitment.answer', 'job_application_id', string="Respuestas")
    job_history_ids = fields.One2many('tyt_recruitment.job_history', 'job_application_id', string="Historial laboral")
    reference_ids = fields.One2many('tyt_recruitment.reference', 'job_application_id', string="Referencia laboral")

    father_data_id = fields.Many2one('tyt_recruitment.family_data_detail', string="Datos del padre")
    mother_data_id = fields.Many2one('tyt_recruitment.family_data_detail', string="Datos de la madre")
    spouse_data_id = fields.Many2one('tyt_recruitment.family_data_detail', string="Datos del cónyuge")

    complete_survey_id = fields.One2many("tyt_recruitment.complete_survey", 'job_application_id', string="Encuesta de salud")
    has_complete_survey = fields.Boolean(string='Tiene Encuesta Completada', compute='compute_has_complete_survey')

    birth_certificate = fields.Binary(string="Acta de nacimiento")
    birth_certificate_filename = fields.Char(string="Nombre del Archivo - ")
    birth_certificate_state = fields.Boolean(string="Estado - Acta de nacimiento", default=False)
    birth_certificate_approved = fields.Boolean(string="Estado de aprobación - Acta de nacimiento", default=False)

    rfc = fields.Binary(string="RFC")
    rfc_filename = fields.Char(string="Nombre del Archivo - RFC")
    rfc_state = fields.Boolean(string="Estado - RFC", default=False)
    rfc_approved = fields.Boolean(string="Estado de aprobación - RFC", default=False)

    curp = fields.Binary(string="CURP")
    curp_filename = fields.Char(string="Nombre del Archivo - CURP")
    curp_state = fields.Boolean(string="Estado - CURP", default=False)
    curp_approved = fields.Boolean(string="Estado de aprobación - CURP", default=False)

    study_certificate = fields.Binary(string="Comprobante de estudio")
    study_certificate_filename = fields.Char(string="Nombre del Archivo - Comprobante de estudio")
    study_certificate_state = fields.Boolean(string="Estado - Comprobante de estudio", default=False)
    study_certificate_approved = fields.Boolean(string="Estado de aprobación - Comprobante de estudio", default=False)

    proposed_letter = fields.Binary(string="Carta propuesta")
    proposed_letter_filename = fields.Char(string="Nombre del Archivo - Carta propuesta")
    proposed_letter_state = fields.Boolean(string="Estado - Carta propuesta", default=False)
    proposed_letter_approved = fields.Boolean(string="Estado de aprobación - Carta propuesta", default=False)

    ine = fields.Binary(string="INE")
    ine_filename = fields.Char(string="Nombre del Archivo - INE")
    ine_state = fields.Boolean(string="Estado - INE", default=False)
    ine_approved = fields.Boolean(string="Estado de aprobación - INE", default=False)

    reference_validation = fields.Binary(string="Validación de referencias")
    reference_validation_filename = fields.Char(string="Nombre del Archivo - Validación de referencias")
    reference_validation_state = fields.Boolean(string="Estado - Validación de referencias", default=False)
    reference_validation_approved = fields.Boolean(string="Estado de aprobación - Validación de referencias", default=False)
    
    utility_bill = fields.Binary(string="Comprobante de domicilio")
    utility_bill_filename = fields.Char(string="Nombre del Archivo - Comprobante de domicilio")
    utility_bill_state = fields.Boolean(string="Estado - Comprobante de domicilio", default=False)
    utility_bill_approved = fields.Boolean(string="Estado de aprobación - Comprobante de domicilio", default=False)

    psychometric = fields.Binary(string="Psicométrico")
    psychometric_filename = fields.Char(string="Nombre del Archivo - Psicométrico")
    psychometric_state = fields.Boolean(string="Estado - Psicométrico", default=False)
    psychometric_approved = fields.Boolean(string="Estado de aprobación - Psicométrico", default=False)

    snn = fields.Binary(string="SNN")
    snn_filename = fields.Char(string="Nombre del Archivo - SNN")
    snn_state = fields.Boolean(string="Estado - SNN", default=False)
    snn_approved = fields.Boolean(string="Estado de aprobación - SNN", default=False)

    interbank_key = fields.Binary(string="Clabe interbancaria")
    interbank_key_filename = fields.Char(string="Nombre del Archivo - Clabe interbancaria")
    interbank_key_state = fields.Boolean(string="Estado - Clabe interbancaria", default=False)
    interbank_key_approved = fields.Boolean(string="Estado de aprobación - Clabe interbancaria", default=False)

    value_proposition = fields.Binary(string="Propuesta de valor")
    value_proposition_filename = fields.Char(string="Nombre del Archivo - Propuesta de valor")
    value_proposition_state = fields.Boolean(string="Estado - Propuesta de valor", default=False)
    value_proposition_approved = fields.Boolean(string="Estado de aprobación - Propuesta de valor", default=False)

    expedient_status = fields.Boolean(string="Estado 01", default=False)
    status_approved = fields.Float(string="Estado 02", default=0)
    status_loaded = fields.Float(string="Estado 03", default=0)

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

    @api.model
    def unlink(self):
        for record in self:
            # Aquí puedes agregar la lógica personalizada
            if record.some_field == 'value':
                _logger.info("removedddddddddddddddddddddddd")
                _logger.info(record.some_field)
        return super(JobApplication, self).unlink()

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
    
    name = fields.Char(string="Nombre")
    reference = fields.Char(string="Medio")
    last_name_father = fields.Char(string="Apellido Paterno")
    last_name_mother = fields.Char(string="Apellido Materno")
    birthplace = fields.Char(string="Lugar de Nacimiento")
    birthdate = fields.Date(string="Fecha de Nacimiento")
    nationality = fields.Char(string="Nacionalidad")
    gender = fields.Selection(GENDER_SELECTION, string="Género")
    age = fields.Integer(string="Edad")
    marital_status = fields.Selection(MARITAL_STATUS_SELECTION, string="Estado Civil")
    social_security_number = fields.Char(string="Número de Seguro Social")
    rfc = fields.Char(string="RFC")
    curp = fields.Char(string="CURP")
    address_street = fields.Char(string="Calle y Número")
    address_neighborhood = fields.Char(string="Colonia")
    address_city = fields.Char(string="Municipio")
    number_phone = fields.Char(string="Número de teléfono")
    personal_email = fields.Char(string="Correo electrónico")
    live_with = fields.Char(string="Con quién vive")
    rent_amount = fields.Float(string="Monto semanal de renta")
    infonavit_credit_amount = fields.Float(string="Monto semanal de Infonavit")
    transports = fields.Char(string="Cantidad de transportes y Tiempo de traslado")
    requested_job_position = fields.Char(string="Puesto que solicita")
    monthly_expenses = fields.Float(string="Gastos mensuales aproximados")
    availability = fields.Char(string="Disponibilidad para empezar a trabajar")
    dependents = fields.Char(string="Personas que dependen de ti")
    foreign_nationality = fields.Boolean(string="Cuenta con nacionalidad extranjera")
    daily_activities = fields.Text(string="Describa sus actividades diarias")

    recruiter_comments = fields.Char(string="Comentarios del reclutador")
    recruiter_id = fields.Many2one('hr.employee', string="Reclutador")

    employee_id = fields.Many2one('hr.employee', string="Empleado relacionado")
    employee_number = fields.Char(related="employee_id.x_studio_numero", string="Número de empleado")

    expedient_status = fields.Boolean(string="Estado de carga", default=False)
    has_complete_survey = fields.Boolean(string='Tiene Encuesta Completada')
    status = fields.Boolean(string="Status")

    # Campaña
    campaign_id = fields.Many2one('tyt_recruitment.campaign', string="Campaña")
    campaign_turn = fields.Selection(related="campaign_id.turn", string="Turno")
    campaign_requsition = fields.Many2one(related="campaign_id.requisition_id", string="Requisición")

    days_of_week_ids = fields.One2many("tyt_recruitment.attendance_days_of_week", 'applicant_id', string="Asistencia detalle")

    computed_name = fields.Char(
        string="Nombre completo",
        compute="_compute_full_name"
    )

    @api.depends('name', 'last_name_father', 'last_name_mother')
    def _compute_full_name(self):
        for rec in self:
            rec.computed_name = f"{rec.name or ''} {rec.last_name_father or ''} {rec.last_name_mother or ''}".strip()

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

            survey_ids = self.days_of_week_ids.attendance_id.surveys_ids.survey_id.ids

            question = self.env['survey.question'].sudo().search([
                ('is_a_guest_question', '=', True),
                ('survey_id', 'in', survey_ids)
            ])

            answer = self.env['survey.user_input.line'].sudo().search([
                ('question_id', 'in', question.ids),
                ('value_char_box', '=', self.social_security_number)
            ])

            inputs = self.env['survey.user_input'].sudo().search([('id', 'in', answer.user_input_id.ids)])

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
                    'type': 'ir.actions.act_window_close'
                }
        
class DataAcademic(models.Model):
    _name = 'tyt_recruitment.data_academic'
    _description = 'tyt_recruitment.data_academic'

    degree = fields.Char(string="Último grado de estudios")
    institution = fields.Char(string="Institución académica")
    specification = fields.Char(string="Comprobante de estudio")

    job_application_id = fields.Many2one('tyt_recruitment.job_application', string="Referencias", ondelete='cascade')

class FamilyDataDetail(models.Model):
    _name = 'tyt_recruitment.family_data_detail'
    _description = 'tyt_recruitment.family_data_detail'

    type = fields.Char(string="Tipo")
    name = fields.Char(string="Nombre")
    occupation = fields.Char(string="Ocupación")
    phone_number = fields.Char(string="Teléfono")

class JobHistory(models.Model):
    _name = 'tyt_recruitment.job_history'
    _description = 'tyt_recruitment.job_history'

    company_name = fields.Char(string="Nombre de la compañía")
    start_date = fields.Date(string="Desde")
    end_date = fields.Date(string="Hasta")
    separation_reason = fields.Char(string="Motivo de serparación")
    weekly_salary = fields.Char(string="Salario semanal")

    job_application_id = fields.Many2one('tyt_recruitment.job_application', string="Solicitud", ondelete='cascade')

class JobReference(models.Model):
    _name = 'tyt_recruitment.reference'
    _description = 'tyt_recruitment.reference'

    name = fields.Char(string="Nombre completo")
    type = fields.Char(string="Tipo")
    occupation = fields.Char(string="Ocupación/Giro")
    phone_number = fields.Char(string="Teléfono")

    job_application_id = fields.Many2one('tyt_recruitment.job_application', string="Referencias", ondelete='cascade')

class Child(models.Model):
    _name = 'tyt_recruitment.child'
    _description = 'tyt_recruitment.child'

    name = fields.Char(string="Nombre")
    age = fields.Char(string="Edad") 

    job_application_id = fields.Many2one('tyt_recruitment.job_application', string="Aplicante", ondelete='cascade')