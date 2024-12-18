# -*- coding: utf-8 -*-

from odoo import api, models, fields, http
from odoo.http import request
import uuid
from io import BytesIO
import base64
from datetime import datetime
from urllib.parse import quote

import logging
_logger = logging.getLogger(__name__)

class Attendance(models.Model):
    _name = 'tyt_recruitment.attendance'
    _description = 'Asistencia'
    _rec_name = 'id'

    trainer = fields.Many2one('hr.employee', string="Entrenador", tracking=True)
    center = fields.Char( string="Centro", tracking=True)
    week = fields.Char( string="Semana", tracking=True)
    turn = fields.Selection([('T/M', 'T/M'), ('T/V', 'T/V'), ('T/N', 'T/N')], string="Turno lista de prospectos", tracking=True)

    income = fields.Char( string="Ingresos", tracking=True)
    returns = fields.Char( string="Regresos", tracking=True)

    days = fields.Integer(string="Días", store=True)

    attendance_days_of_week_ids = fields.One2many("tyt_recruitment.attendance_days_of_week", "attendance_id", string="Días de asistencia")

    recruiter = fields.Char(string="Reclutador", tracking=True)
    campaign_id = fields.Many2one("tyt_recruitment.campaign", ondelete='cascade')
    requisition_id = fields.Many2one("tyt_recruitment.requisition", ondelete='cascade')

    examen1 = fields.Many2one('survey.survey', string="Examen 1")
    examen2 = fields.Many2one('survey.survey', string="Examen 2")
    examen3 = fields.Many2one('survey.survey', string="Examen 3")
    examen4 = fields.Many2one('survey.survey', string="Examen 4")
    
class AttendanceState(models.Model):
    _name = 'tyt_recruitment.tag_attendance'
    _description = 'Estado'
    _rec_name = 'tag'

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

    login = fields.Char(string="Login")
    recruiter = fields.Char(string="Reclutador")
    prospect_turn = fields.Selection(related="attendance_id.turn", string="Turno lista de prospectos", tracking=True)
    right_turn = fields.Char(string="Turno correcto")
    observations = fields.Char(string="Observaciones")
    experience = fields.Char(string="Experiencia")
    reason_for_withdrawal = fields.Many2one("tyt_recruitment.reason_for_withdrawal", string="Motivo de la baja")

    
    applicant_id = fields.Many2one("tyt_recruitment.applicant", string="Aplicante", ondelete='cascade')
    applicant_name = fields.Char(related="applicant_id.name", string="Nombre", store=True)
    applicant_nss = fields.Char(related="applicant_id.social_security_number", string="Número de Seguro Social")

    attendance_id = fields.Many2one('tyt_recruitment.attendance', string="Lista de asistencia", ondelete='cascade')

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

class ReasonForWithdrawal(models.Model):
    _name = 'tyt_recruitment.reason_for_withdrawal'
    _description = 'Motivo de la baja'
    _rec_name = 'text'

    text = fields.Char(required=True, string="Motivo", tracking=True)