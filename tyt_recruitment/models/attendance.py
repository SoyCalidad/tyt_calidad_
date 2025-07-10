# -*- coding: utf-8 -*-

from odoo import api, models, fields, http
from odoo.http import request
import uuid
from io import BytesIO
import base64
from datetime import datetime
from urllib.parse import quote

from ..utils.constants import ATTENDANCE_STATE

import logging
_logger = logging.getLogger(__name__)

class Attendance(models.Model):
    _name = 'tyt_recruitment.attendance'
    _description = 'Asistencia'
    _rec_name = 'id'
    _inherit = ['mail.thread']

    trainer = fields.Many2one('hr.employee', string="Entrenador", tracking=True)
    center = fields.Char( string="Centro", tracking=True)
    week = fields.Char( string="Semana", tracking=True)
    turn = fields.Selection([('T/M', 'T/M'), ('T/V', 'T/V'), ('T/N', 'T/N')], string="Turno lista de prospectos", tracking=True)

    income = fields.Char( string="Ingresos", compute="_compute_income", store=True, tracking=True)
    returns = fields.Char( string="Regresos", compute="_compute_returns", tracking=True, default="0")
    desertion = fields.Char( string="Deserción", tracking=True, default="0")

    days = fields.Integer(string="Días de capacitación", store=True, tracking=True)

    state = fields.Selection(ATTENDANCE_STATE, string='Estado', default='doing', tracking=True)

    attendance_days_of_week_ids = fields.One2many("tyt_recruitment.attendance_days_of_week", "attendance_id", string="Días de asistencia")
    kardex_by_applicant_ids = fields.One2many("tyt_recruitment.kardex_by_applicant", "attendance_id", string="Kardex de asistencia")
    kardex_by_applicant_two_ids = fields.One2many("tyt_recruitment.kardex_by_applicant", "attendance_id", string="Kardex de asistencia 2")

    view_kardex = fields.Boolean(string="Ver kardex", default=False, tracking=True)
    view_kardex_certificate = fields.Boolean(string="Ver kardex certificación", default=False, tracking=True)

    recruiter = fields.Char(string="Reclutador", tracking=True)
    campaign_id = fields.Many2one("tyt_recruitment.campaign", string="Campaña", ondelete='cascade', tracking=True)
    campaign_ids = fields.Many2many('tyt_recruitment.campaign', string="Campañas relacionadas", relation='tyt_att_camp_rel')
    requisition_id = fields.Many2one("tyt_recruitment.requisition", ondelete='cascade', tracking=True)

    survey_counter = fields.Integer(string="Cantidad de exámenes", compute="_compute_survey_counter", store=True, tracking=True)
    surveys_ids = fields.One2many('tyt_recruitment.survey_attendance', 'attendance_id', string="Exámenes")

    @api.depends('kardex_by_applicant_ids.login')
    def _compute_income(self):
        for record in self:
            record.income = sum(1 for kardex in record.kardex_by_applicant_ids if kardex.login)

    @api.depends(
        'attendance_days_of_week_ids.day1', 'attendance_days_of_week_ids.day2',
        'attendance_days_of_week_ids.day3', 'attendance_days_of_week_ids.day4',
        'attendance_days_of_week_ids.day5', 'attendance_days_of_week_ids.day6',
        'attendance_days_of_week_ids.day7', 'attendance_days_of_week_ids.day8',
        'attendance_days_of_week_ids.day9', 'attendance_days_of_week_ids.day10',
        'attendance_days_of_week_ids.day11', 'attendance_days_of_week_ids.day12',
        'attendance_days_of_week_ids.day13', 'attendance_days_of_week_ids.day14',
        'attendance_days_of_week_ids.day15', 'attendance_days_of_week_ids.day16',
        'attendance_days_of_week_ids.day17', 'attendance_days_of_week_ids.day18',
        'attendance_days_of_week_ids.day19', 'attendance_days_of_week_ids.day20',
    )
    def _compute_returns(self):
        for record in self:
            total = 0
            for attendance_day in record.attendance_days_of_week_ids:
                found_b = False
                for i in range(3, 21):  # Recorremos day1 a day20
                    day_field = f'day{i}'
                    day_value = getattr(attendance_day, day_field, None)
                    if day_value and getattr(day_value, 'tag', None) == 'B':
                        found_b = True
                        break  # Si ya encontramos uno con 'B', no revisamos los demás
                if found_b:
                    total += 1
            record.returns = total

    @api.onchange('income', 'returns')
    def _onchange_desertion(self):
        total = len(self.attendance_days_of_week_ids)
        returns = int(self.returns)
        if total > 0 and returns > 0:
            desertion_calculate = str( ( returns*100 )/total ) + "%"
        else:
            desertion_calculate = "0"
        self.write({'desertion': desertion_calculate})

    @api.depends('surveys_ids')
    def _compute_survey_counter(self):
        for record in self:
            record.survey_counter = len(record.surveys_ids)

    def action_view_kardex(self):
        self.view_kardex = True

        for kardex_applicant in self.kardex_by_applicant_ids:
            for index, survey in enumerate(self.surveys_ids):
                employee_number = kardex_applicant.attendance_days_of_week_id.applicant_id.employee_number

                answer = self.env['survey.user_input.line'].sudo().search([
                    ('survey_id', '=', survey.survey_id.id),
                    ('value_char_box', '=', employee_number)
                ], limit=1)

                field_name = f"exam{index+1}"
                value = "0.0"

                if answer and employee_number:
                    value = str(answer.user_input_id.scoring_percentage)

                if hasattr(kardex_applicant, field_name):
                    setattr(kardex_applicant, field_name, value)
            
    def action_view_kardex_certificate(self):
        self.view_kardex_certificate = True

    def action_send_concession(self):
        self.ensure_one()
        lang = self.env.context.get('lang')
        template = self.env.ref('tyt_recruitment.mail_template_attendance_concession')

        # Generar el archivo XLS y adjuntarlo al correo

        report = self.env.ref('tyt_recruitment.action_report_report_concession')

        generated_report = report._render_xlsx('tyt_recruitment.action_report_report_concession', docids=self.id, data=())
        data_record = base64.b64encode(generated_report[0])
        ir_values = {
        'name': 'Invoice Report',
        'type': 'binary',
        'datas': data_record,
        'store_fname': data_record,
        'mimetype': 'application/vnd.ms-excel',
        'res_model': 'account.move',
        }
        attachment = self.env['ir.attachment'].sudo().create(ir_values)

        # attachment = self._create_attachment()

        context = {
            'default_model': 'tyt_recruitment.attendance',
            'default_template_id': template.id if template else None,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'default_email_to': "",
            'default_subject': template.subject,
            'default_body_html': template.body_html,
            'default_attachment_ids': [(6, 0, [attachment.id])]
        }
        return {
            'name': 'Previsualizar Correo',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': context,
        }

    def rubric_view_json(self, rubric_id):
        return {
            'name': 'Vista Form del Registro',
            'type': 'ir.actions.act_window',
            'res_model': 'tyt_recruitment.evaluation_rubric',
            'view_mode': 'form',
            'res_id': rubric_id,
            'views': [(False, 'form')], 
            'target': 'current',
        }

    def action_view_evaluation_rubric(self):
        current_rubric = self.env['tyt_recruitment.evaluation_rubric'].search([('attendance_id', '=', self.id)], limit=1)
        if current_rubric:
            # Redirect to evaluation rubric
            return self.rubric_view_json(current_rubric.id)
        else:
            # Creating a new evaluation rubric
            rubric_data = {
                'attendance_id': self.id
            }
            new_rubric = self.env['tyt_recruitment.evaluation_rubric'].sudo().create(rubric_data)

            # Creating new input evaluations
            details = request.env['tyt_recruitment.detail_evaluation_rubric'].search([])
            for detail in details:
                new_input_evaluation_data = {
                    'evaluation_rubric_id': new_rubric.id,
                    'detail_evaluation_rubric_id': detail.id
                }
                self.env['tyt_recruitment.input_evaluation_rubric'].sudo().create(new_input_evaluation_data)

            return self.rubric_view_json(new_rubric.id)

class AttendanceState(models.Model):
    _name = 'tyt_recruitment.tag_attendance'
    _description = 'Estado'
    _rec_name = 'tag'
    _inherit = ['mail.thread']

    tag = fields.Char(required=True, string="Etiqueta", tracking=True)
    name = fields.Char(required=True, string="Nombre", tracking=True)

class TagNameController(http.Controller):
    @http.route('/tag_name_list', auth='public', website=True)
    def tag_name_list(self):
        records = request.env['tyt_recruitment.tag_attendance'].search([])
        return request.render('tyt_recruitment.tag_name_list', {'records': records})
    
class DaysOfWeek(models.Model):
    _name = 'tyt_recruitment.attendance_days_of_week'
    _description = 'Días de la semana'
    _inherit = ['mail.thread']

    day1 = fields.Many2one('tyt_recruitment.tag_attendance', string="01", tracking=True)
    day2 = fields.Many2one('tyt_recruitment.tag_attendance', string="02", tracking=True)
    day3 = fields.Many2one('tyt_recruitment.tag_attendance', string="03", tracking=True)
    day4 = fields.Many2one('tyt_recruitment.tag_attendance', string="04", tracking=True)
    day5 = fields.Many2one('tyt_recruitment.tag_attendance', string="05", tracking=True)
    day6 = fields.Many2one('tyt_recruitment.tag_attendance', string="06", tracking=True)
    day7 = fields.Many2one('tyt_recruitment.tag_attendance', string="07", tracking=True)
    day8 = fields.Many2one('tyt_recruitment.tag_attendance', string="08", tracking=True)
    day9 = fields.Many2one('tyt_recruitment.tag_attendance', string="09", tracking=True)
    day10 = fields.Many2one('tyt_recruitment.tag_attendance', string="10", tracking=True)
    day11 = fields.Many2one('tyt_recruitment.tag_attendance', string="11", tracking=True)
    day12 = fields.Many2one('tyt_recruitment.tag_attendance', string="12", tracking=True)
    day13 = fields.Many2one('tyt_recruitment.tag_attendance', string="13", tracking=True)
    day14 = fields.Many2one('tyt_recruitment.tag_attendance', string="14", tracking=True)
    day15 = fields.Many2one('tyt_recruitment.tag_attendance', string="15", tracking=True)
    day16 = fields.Many2one('tyt_recruitment.tag_attendance', string="16", tracking=True)
    day17 = fields.Many2one('tyt_recruitment.tag_attendance', string="17", tracking=True)
    day18 = fields.Many2one('tyt_recruitment.tag_attendance', string="18", tracking=True)
    day19 = fields.Many2one('tyt_recruitment.tag_attendance', string="19", tracking=True)
    day20 = fields.Many2one('tyt_recruitment.tag_attendance', string="20", tracking=True)

    opday1 = fields.Many2one('tyt_recruitment.tag_attendance', string="OPE día 01", tracking=True)
    opday2 = fields.Many2one('tyt_recruitment.tag_attendance', string="OPE día 02", tracking=True)

    prospect_turn = fields.Selection(related="attendance_id.turn", string="Turno lista de prospectos", tracking=True)
    right_turn = fields.Char(string="Turno correcto", tracking=True)
    observations = fields.Char(string="Observaciones", tracking=True)
    experience = fields.Char(string="Experiencia", tracking=True)
    reason_for_withdrawal = fields.Many2one("hr.applicant.refuse.reason", string="Motivo de rechazo", tracking=True)

    
    applicant_id = fields.Many2one("tyt_recruitment.applicant", string="Aplicante", ondelete='cascade', tracking=True)
    recruiter = fields.Many2one(related="applicant_id.recruiter_id", string="Reclutador", tracking=True)
    login = fields.Char(related="applicant_id.employee_number", string="Login", tracking=True)

    applicant_name = fields.Char(related="applicant_id.name", string="Nombre", store=True, tracking=True)
    applicant_nss = fields.Char(related="applicant_id.social_security_number", string="Número de Seguro Social", tracking=True)

    attendance_id = fields.Many2one('tyt_recruitment.attendance', string="Lista de asistencia", ondelete='cascade', tracking=True)

    full_name = fields.Char(string="Nombre Completo", compute="_compute_full_name", store=True)

    campaign_id = fields.Many2one('tyt_recruitment.campaign', string="Campaña", ondelete='cascade', tracking=True)

    @api.depends('applicant_id.name', 'applicant_id.last_name_father', 'applicant_id.last_name_mother')
    def _compute_full_name(self):
        for record in self:
            if record.applicant_id:
                name = record.applicant_id.name or ''
                last_name_father = record.applicant_id.last_name_father or ''
                last_name_mother = record.applicant_id.last_name_mother or ''
                record.full_name = f"{last_name_father} {last_name_mother} {name}".strip().upper()
            elif record.applicant_name:
                record.full_name = record.applicant_name.upper()
            else:
                record.full_name = ''

    @api.onchange('day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'day7', 'day8', 'day9', 'day10', 'day11', 'day12', 'day13', 'day14', 'day15', 'day16', 'day17', 'day18', 'day19', 'day20')
    def _onchange_days(self):
        if not self.applicant_id.employee_id:
            for field_name in ['day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'day7', 'day8', 'day9', 'day10', 'day11', 'day12', 'day13', 'day14', 'day15', 'day16', 'day17', 'day18', 'day19', 'day20']:
                _logger.info(field_name)
                _logger.info(self.applicant_id.name)
                employee = self.env['hr.employee'].search([('segurosocial', '=', self.applicant_id.social_security_number)], limit=1)

                if self[field_name].tag == 'A':
                    if employee.id and not self.login:
                        self.applicant_id.write({'employee_id': employee.id})

    def show_applicant_details(self):

        if self.applicant_id:
            return {
                'name': 'Vista Form de los detalles del aplicante',
                'type': 'ir.actions.act_window',
                'res_model': 'tyt_recruitment.applicant',
                'view_mode': 'form',
                'res_id': self.applicant_id.id,
                'view_id': self.env.ref('tyt_recruitment.tyt_recruitment_prospect_view_form').id,
                'target': 'current',
            }
        else:
            return {
                'type': 'ir.actions.act_window_close'
            }

class SurveyAttendance(models.Model):
    _name = 'tyt_recruitment.survey_attendance'
    _description = 'Encuesta de capacitación'
    _inherit = ['mail.thread']

    survey_id = fields.Many2one('survey.survey', string="Examen", tracking=True)
    title = fields.Char(related='survey_id.title', string='Título', tracking=True)
    
    attendance_id = fields.Many2one('tyt_recruitment.attendance', string="Lista de asistencia", tracking=True)

class KardexAttendance(models.Model):
    _name = 'tyt_recruitment.kardex_by_applicant'
    _description = 'Kardex de capacitación'
    _inherit = ['mail.thread']

    experience = fields.Char(string="Experiencia", tracking=True)
    time = fields.Char(string="Tiempo", tracking=True)

    exam1 = fields.Char(string="Examen 1", tracking=True)
    exam2 = fields.Char(string="Examen 2", tracking=True)
    exam3 = fields.Char(string="Examen 3", tracking=True)
    exam4 = fields.Char(string="Examen 4", tracking=True)
    exam5 = fields.Char(string="Examen 5", tracking=True)
    exam6 = fields.Char(string="Examen 6", tracking=True)
    exam7 = fields.Char(string="Examen 7", tracking=True)
    exam8 = fields.Char(string="Examen 8", tracking=True)
    exam9 = fields.Char(string="Examen 9", tracking=True)
    exam10 = fields.Char(string="Examen 10", tracking=True)
    exam11 = fields.Char(string="Examen 11", tracking=True)
    exam12 = fields.Char(string="Examen 12", tracking=True)
    exam13 = fields.Char(string="Examen 13", tracking=True)
    exam14 = fields.Char(string="Examen 14", tracking=True)
    exam15 = fields.Char(string="Examen 15", tracking=True)

    comments = fields.Char(string="Comentarios", tracking=True)

    certification1 = fields.Char(string="Certificado 1", tracking=True)
    certification2 = fields.Char(string="Certificado 2", tracking=True)
    certification3 = fields.Char(string="Certificado 3", tracking=True)
    comments_quality = fields.Char(string="Comentario - técnico de calidad", tracking=True)

    accreditation_status = fields.Selection(
        selection=[
            ('certifica', 'Certifica'),
            ('no_certifica', 'No certifica'),
        ],
        string="Estatus de certificación",
        tracking=True
    )
    concession = fields.Boolean(string="Concesión", tracking=True)
    observation = fields.Char(string="Observaciones", tracking=True)

    attendance_days_of_week_id = fields.Many2one('tyt_recruitment.attendance_days_of_week', string="Kardex de asistencia", ondelete='cascade', tracking=True)
    applicant_id = fields.Many2one(related="attendance_days_of_week_id.applicant_id", string="Aplicante", ondelete='cascade', tracking=True)
    login = fields.Char(related="applicant_id.employee_number", string="Login")
    marital_status = fields.Selection(related="applicant_id.marital_status", string="Estado civil", tracking=True)
    applicant_name = fields.Char(related="applicant_id.computed_name", string="Nombre completo", tracking=True)

    attendance_id = fields.Many2one('tyt_recruitment.attendance', string="Lista de asistencia", ondelete='cascade', tracking=True)
    survey_counter = fields.Integer(related="attendance_id.survey_counter", string="Contandor de exámenes", tracking=True)

    average = fields.Float(string="Promedio", compute="_compute_average_score", store=True, tracking=True)
    highest_score = fields.Float(string="Promedio alto", compute="_compute_highest_score", store=True, tracking=True)

    certification_feedback_ids = fields.One2many('tyt_recruitment.certification_feedback', 'kardex_id', string="Certificación de retroalimentación")
    has_certification_feedback = fields.Boolean(string="Tiene retroalimentación", compute="_compute_has_certification_feedback", tracking=True)

    @api.onchange('accreditation_status')
    def _onchange_accreditation_status(self):
        if self.accreditation_status == 'no_certifica':
            self.concession = True
        else:
            self.concession = False

    @api.depends('certification_feedback_ids')
    def _compute_has_certification_feedback(self):
        for record in self:
            record.has_certification_feedback = bool(record.certification_feedback_ids)
            _logger.info(record.has_certification_feedback)

    @api.depends('survey_counter', 'exam1', 'exam2', 'exam3', 'exam4', 'exam5',
                 'exam6', 'exam7', 'exam8', 'exam9', 'exam10', 'exam11',
                 'exam12', 'exam13', 'exam14', 'exam15')
    def _compute_average_score(self):
        for record in self:
            total = 0
            count = 0
            for i in range(1, record.survey_counter + 1):
                exam_field = f"exam{i}"
                score = getattr(record, exam_field, None)
                try:
                    total += float(score)
                    count += 1
                except ValueError:
                    continue
            record.average = total / count if count > 0 else 0

    def action_open_certification_feedback_form(self):
        
        url = f"/certification_feedback/{self.id}/"
        
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new', 
        }
        
    def action_new_certification_feedback(self):

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'tyt_recruitment.certification_feedback',
            'view_mode': 'form',
            'view_id': self.env.ref('tyt_recruitment.view_certification_feedback_simple_form').id,
            'target': 'new',
            'context': {'default_kardex_id': self.id},
        }
    
    def action_message_certification_feedback(self):

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Retroalimentación - Técnico de calidad',
                'message': 'Ya ha completado los datos de esta retroalimentación',
                'type': 'success',  
                'sticky': False
            }
        }

    @api.depends('survey_counter', 'exam1', 'exam2', 'exam3', 'exam4', 'exam5',
             'exam6', 'exam7', 'exam8', 'exam9', 'exam10', 'exam11',
             'exam12', 'exam13', 'exam14', 'exam15')
    def _compute_highest_score(self):
        for record in self:
            highest_score = 0
            for i in range(1, record.survey_counter + 1):
                exam_field = f"exam{i}"
                score = getattr(record, exam_field, None)
                if score:
                    try:
                        score_value = float(score)
                        highest_score = max(highest_score, score_value)
                    except ValueError:
                        continue
            record.highest_score = highest_score


class ReasonForWithdrawal(models.Model):
    _name = 'tyt_recruitment.reason_for_withdrawal'
    _description = 'Motivo de la baja'
    _rec_name = 'text'

    text = fields.Char(required=True, string="Motivo")