# -*- coding: utf-8 -*-

from odoo import api, models, fields, http
from odoo.http import request
import uuid
from io import BytesIO
import base64
from datetime import datetime
from urllib.parse import quote

from ..utils.constants import RUBRIC_STATE

import logging
_logger = logging.getLogger(__name__)

class EvaluationRubric(models.Model):
    _name = 'tyt_recruitment.evaluation_rubric'
    _description = 'Rúbrica de evaluación al expositor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'id'

    status_approved = fields.Float(string="Estado de aprobación", default=0)

    date = fields.Date(string="Fecha", tracking=True)
    auditor = fields.Many2one('hr.employee', string="Auditor", tracking=True)

    attendance_id = fields.Many2one('tyt_recruitment.attendance', string="Capacitación")
    week = fields.Char(related="attendance_id.week", string="Semana", tracking=True)
    coach = fields.Many2one(related="attendance_id.trainer", string="Entrenador", tracking=True)
    campaign = fields.Many2one(related="attendance_id.campaign_id", string="Campaña", tracking=True)
    
    signature = fields.Binary(string="Firma", widget="signature", store=True)
    state = fields.Selection(RUBRIC_STATE, string='Estado', default='doing')

    input_evaluation_rubric_ids = fields.One2many('tyt_recruitment.input_evaluation_rubric', 'evaluation_rubric_id', string="Detalles")

    @api.onchange('input_evaluation_rubric_ids')
    def _onchange_check_approved(self):
        
        if self.input_evaluation_rubric_ids:
            all_yes = sum(1 for input in self.input_evaluation_rubric_ids if input.compliance == 'yes')
            self.status_approved = (all_yes / len(self.input_evaluation_rubric_ids)) * 100
        else:
            self.status_approved = 0

    @api.depends('kardex_by_applicant_ids.login')
    def _compute_income(self):
        for record in self:
            record.income = sum(1 for kardex in record.kardex_by_applicant_ids if kardex.login)

    @api.depends('surveys_ids')
    def _compute_survey_counter(self):
        for record in self:
            record.survey_counter = len(record.surveys_ids)

    @api.onchange('signature')
    def _compute_state(self):

        if self.signature:
            self.state = 'signed'
        else:
            self.state = 'doing'

    def action_save_signature(self):
        if self.signature:
            # Guardar el valor del campo signature
            self.sudo().write({'signature': self.signature})
            
            # Mostrar un mensaje de éxito
            return {
                'type': 'ir.actions.act_window_close',
            }
     
    def action_view_signature(self):
        default_signature = False
        if self.signature:
            default_signature = self.signature
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Firma de Rúbrica',
            'res_model': 'tyt_recruitment.evaluation_signature_wizard',
            'view_mode': 'form',
            'target': 'new',
            'view_id': self.env.ref('tyt_recruitment.evaluation_signature_wizard_form').id,
            'context': { 'default_evaluation_rubric_id': self.id}
        }
    
    def action_view_validate_and_notify(self):
        self.ensure_one()

        self.state = 'validated_notified'

        user = self.env.user

        return {
            'name': 'Enviar informe',
            'type': 'ir.actions.act_window',
            'res_model': 'mail.compose.message',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_model': 'tyt_recruitment.evaluation_rubric',
                'default_template_id': self.env.ref('tyt_recruitment.email_template_rubric_signature').id,
                'default_email_from': user.email,
                'default_email_to': self.auditor.work_email,
                'default_res_ids': [self.id],
            }
        }

class EvaluationRubric(models.Model):
    _name = 'tyt_recruitment.detail_evaluation_rubric'
    _description = 'Pregunta de rúbrica de evaluación al expositor'
    _rec_name = 'id'

    weighing = fields.Integer(string="Ponderación", tracking=True)
    concept = fields.Char(string="Concepto", tracking=True)
    description = fields.Text(string="Descripción", tracking=True)

class EvaluationRubric(models.Model):
    _name = 'tyt_recruitment.input_evaluation_rubric'
    _description = 'Respuesta de rúbrica de evaluación al expositor'
    _rec_name = 'id'  

    compliance = fields.Selection([('yes', 'Sí'), ('no', 'No')], string="Cumple", tracking=True)
    comment = fields.Char(string="Comentario", tracking=True)

    evaluation_rubric_id = fields.Many2one('tyt_recruitment.evaluation_rubric', string="Rúbrica de evaluación")
    detail_evaluation_rubric_id = fields.Many2one('tyt_recruitment.detail_evaluation_rubric', string="Respuesta")

    weighing = fields.Integer(related='detail_evaluation_rubric_id.weighing', string="Ponderación")
    concept = fields.Char(related='detail_evaluation_rubric_id.concept', string="Ponderación")
    description = fields.Text(related='detail_evaluation_rubric_id.description', string="Ponderación")
    
    evalutation_rubric_id = fields.Many2one('tyt_recruitment.evaluation_rubric', string="Componente de rúbrica")

class EvaluationSignatureWizard(models.TransientModel):
    _name = 'tyt_recruitment.evaluation_signature_wizard'
    _description = 'Wizard para capturar la firma en la rúbrica de evaluación'

    evaluation_rubric_id = fields.Many2one('tyt_recruitment.evaluation_rubric', string="Evaluación", required=True)
    signature = fields.Binary(string="Firma", widget="signature")

    def action_save_signature(self):
        if self.signature:
            self.evaluation_rubric_id.write({
                'signature': self.signature,
                'state': 'signed'
            })
        return {'type': 'ir.actions.act_window_close'}