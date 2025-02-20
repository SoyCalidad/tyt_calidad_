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

    trainer = fields.Many2one('hr.employee', string="Entrenador")
    center = fields.Char( string="Centro")
    week = fields.Char( string="Semana")
    turn = fields.Selection([('T/M', 'T/M'), ('T/V', 'T/V'), ('T/N', 'T/N')], string="Turno lista de prospectos")

    income = fields.Char( string="Ingresos", compute="_compute_income", store=True)
    returns = fields.Char( string="Regresos")
    desertion = fields.Char( string="Deserción")

    days = fields.Integer(string="Días de capacitación", store=True)

    state = fields.Selection(ATTENDANCE_STATE, string='Estado', default='doing')

    attendance_days_of_week_ids = fields.One2many("tyt_recruitment.attendance_days_of_week", "attendance_id", string="Días de asistencia")
    kardex_by_applicant_ids = fields.One2many("tyt_recruitment.kardex_by_applicant", "attendance_id", string="Kardex de asistencia")
    kardex_by_applicant_two_ids = fields.One2many("tyt_recruitment.kardex_by_applicant", "attendance_id", string="Kardex de asistencia 2")

    view_kardex = fields.Boolean(string="Ver kardex", default=False)
    view_kardex_certificate = fields.Boolean(string="Ver kardex certificación", default=False)

    recruiter = fields.Char(string="Reclutador")
    campaign_id = fields.Many2one("tyt_recruitment.campaign", string="Campaña", ondelete='cascade')
    requisition_id = fields.Many2one("tyt_recruitment.requisition", ondelete='cascade')

    survey_counter = fields.Integer(string="Cantidad de exámenes", compute="_compute_survey_counter", store=True)
    surveys_ids = fields.One2many('tyt_recruitment.survey_attendance', 'attendance_id', string="Exámenes")

    @api.depends('kardex_by_applicant_ids.login')
    def _compute_income(self):
        for record in self:
            record.income = sum(1 for kardex in record.kardex_by_applicant_ids if kardex.login)

    @api.depends('surveys_ids')
    def _compute_survey_counter(self):
        for record in self:
            record.survey_counter = len(record.surveys_ids)

    def action_view_kardex(self):
        
        self.view_kardex = True

        for kardex_applicant in self.kardex_by_applicant_ids:
            for index, survey in enumerate(self.surveys_ids):
                
                answer = self.env['survey.user_input.line'].sudo().search([
                    ('survey_id', '=', survey.survey_id.id),
                    ('value_char_box', '=', kardex_applicant.attendance_days_of_week_id.applicant_id.social_security_number)
                ], limit=1)

                field_name = f"exam{index+1}"
                value = "0.0"

                if answer: 
                    value = str(answer.user_input_id.scoring_percentage)

                if hasattr(kardex_applicant, field_name):
                    setattr(kardex_applicant, field_name, value)
            
    def action_view_kardex_certificate(self):
        self.view_kardex_certificate = True

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

    tag = fields.Char(required=True, string="Etiqueta")
    name = fields.Char(required=True, string="Nombre")

class TagNameController(http.Controller):
    @http.route('/tag_name_list', auth='public', website=True)
    def tag_name_list(self):
        records = request.env['tyt_recruitment.tag_attendance'].search([])
        return request.render('tyt_recruitment.tag_name_list', {'records': records})
    
class DaysOfWeek(models.Model):
    _name = 'tyt_recruitment.attendance_days_of_week'
    _description = 'Días de la semana'

    day1 = fields.Many2one('tyt_recruitment.tag_attendance', string="01")
    day2 = fields.Many2one('tyt_recruitment.tag_attendance', string="02")
    day3 = fields.Many2one('tyt_recruitment.tag_attendance', string="03")
    day4 = fields.Many2one('tyt_recruitment.tag_attendance', string="04")
    day5 = fields.Many2one('tyt_recruitment.tag_attendance', string="05")
    day6 = fields.Many2one('tyt_recruitment.tag_attendance', string="06")
    day7 = fields.Many2one('tyt_recruitment.tag_attendance', string="07")
    day8 = fields.Many2one('tyt_recruitment.tag_attendance', string="08")
    day9 = fields.Many2one('tyt_recruitment.tag_attendance', string="09")
    day10 = fields.Many2one('tyt_recruitment.tag_attendance', string="10")
    day11 = fields.Many2one('tyt_recruitment.tag_attendance', string="11")
    day12 = fields.Many2one('tyt_recruitment.tag_attendance', string="12")
    day13 = fields.Many2one('tyt_recruitment.tag_attendance', string="13")
    day14 = fields.Many2one('tyt_recruitment.tag_attendance', string="14")
    day15 = fields.Many2one('tyt_recruitment.tag_attendance', string="15")
    day16 = fields.Many2one('tyt_recruitment.tag_attendance', string="16")
    day17 = fields.Many2one('tyt_recruitment.tag_attendance', string="17")
    day18 = fields.Many2one('tyt_recruitment.tag_attendance', string="18")
    day19 = fields.Many2one('tyt_recruitment.tag_attendance', string="19")
    day20 = fields.Many2one('tyt_recruitment.tag_attendance', string="20")

    opday1 = fields.Many2one('tyt_recruitment.tag_attendance', string="OPE día 01")
    opday2 = fields.Many2one('tyt_recruitment.tag_attendance', string="OPE día 02")

    prospect_turn = fields.Selection(related="attendance_id.turn", string="Turno lista de prospectos")
    right_turn = fields.Char(string="Turno correcto")
    observations = fields.Char(string="Observaciones")
    experience = fields.Char(string="Experiencia")
    reason_for_withdrawal = fields.Many2one("hr.applicant.refuse.reason", string="Motivo de rechazo")

    
    applicant_id = fields.Many2one("tyt_recruitment.applicant", string="Aplicante", ondelete='cascade')
    recruiter = fields.Many2one(related="applicant_id.recruiter_id", string="Reclutador")
    login = fields.Char(related="applicant_id.employee_number", string="Login")

    applicant_name = fields.Char(related="applicant_id.name", string="Nombre", store=True)
    applicant_nss = fields.Char(related="applicant_id.social_security_number", string="Número de Seguro Social")

    attendance_id = fields.Many2one('tyt_recruitment.attendance', string="Lista de asistencia", ondelete='cascade')

    @api.onchange('day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'day7', 'day8', 'day9', 'day10', 'day11', 'day12', 'day13', 'day14', 'day15', 'day16', 'day17', 'day18', 'day19', 'day20')
    def _onchange_days(self):
        if not self.applicant_id.employee_id:
            for field_name in ['day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'day7', 'day8', 'day9', 'day10', 'day11', 'day12', 'day13', 'day14', 'day15', 'day16', 'day17', 'day18', 'day19', 'day20']:
                _logger.info(field_name)
                _logger.info(self.applicant_id.name)
                if self[field_name].tag == 'A':
                    employee = self.env['hr.employee'].search([('l10n_mx_nss', '=', self.applicant_id.social_security_number)], limit=1)
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

    survey_id = fields.Many2one('survey.survey', string="Examen")
    title = fields.Char(related='survey_id.title', string='Título')
    
    attendance_id = fields.Many2one('tyt_recruitment.attendance', string="Lista de asistencia")

class KardexAttendance(models.Model):
    _name = 'tyt_recruitment.kardex_by_applicant'
    _description = 'Kardex de capacitación'

    login = fields.Char(string="#")

    experience = fields.Char(string="Experiencia")
    time = fields.Char(string="Tiempo")

    exam1 = fields.Char(string="Examen 1")
    exam2 = fields.Char(string="Examen 2")
    exam3 = fields.Char(string="Examen 3")
    exam4 = fields.Char(string="Examen 4")
    exam5 = fields.Char(string="Examen 5")
    exam6 = fields.Char(string="Examen 6")
    exam7 = fields.Char(string="Examen 7")
    exam8 = fields.Char(string="Examen 8")
    exam9 = fields.Char(string="Examen 9")
    exam10 = fields.Char(string="Examen 10")
    exam11 = fields.Char(string="Examen 11")
    exam12 = fields.Char(string="Examen 12")
    exam13 = fields.Char(string="Examen 13")
    exam14 = fields.Char(string="Examen 14")
    exam15 = fields.Char(string="Examen 15")

    comments = fields.Char(string="Comentarios")

    certification1 = fields.Char(string="Certificado 1")
    certification2 = fields.Char(string="Certificado 2")
    certification3 = fields.Char(string="Certificado 3")
    comments_quality = fields.Char(string="Comentario - técnico de calidad")

    accreditation_status = fields.Char(string="Estatus de certificación")
    concession = fields.Char(string="Concesión")
    observation = fields.Char(string="Observaciones")

    attendance_days_of_week_id = fields.Many2one('tyt_recruitment.attendance_days_of_week', string="Kardex de asistencia", ondelete='cascade')
    applicant_id = fields.Many2one(related="attendance_days_of_week_id.applicant_id", string="Aplicante", ondelete='cascade')
    marital_status = fields.Selection(related="applicant_id.marital_status", string="Estado civil")
    applicant_name = fields.Char(related="applicant_id.computed_name", string="Nombre completo")

    attendance_id = fields.Many2one('tyt_recruitment.attendance', string="Lista de asistencia", ondelete='cascade')
    survey_counter = fields.Integer(related="attendance_id.survey_counter", string="Contandor de exámenes")

    average = fields.Float(string="Promedio", compute="_compute_average_score", store=True)
    highest_score = fields.Float(string="Promedio alto", compute="_compute_highest_score", store=True)

    certification_feedback_ids = fields.One2many('tyt_recruitment.certification_feedback', 'kardex_id', string="Certificación de retroalimentación")
    has_certification_feedback = fields.Boolean(string="Tiene retroalimentación", compute="_compute_has_certification_feedback")

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