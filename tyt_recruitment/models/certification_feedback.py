# -*- coding: utf-8 -*-

from odoo import api, models, fields, http
from odoo.http import request
import uuid
from io import BytesIO
import base64
from datetime import datetime
from urllib.parse import quote

from ..utils.constants import FEEDBACK_STATE

import logging
_logger = logging.getLogger(__name__)

class CertificationFeeback(models.Model):
    _name = 'tyt_recruitment.certification_feedback'
    _description = 'Rúbrica de evaluación al expositor'
    _rec_name = 'id'
    _inherit = ['mail.thread']

    date = fields.Date(string="Fecha", tracking=True)

    name = fields.Char(string="Nombre", tracking=True)
    evaluation_average = fields.Float(string="Promedio de Evaluación", tracking=True)

    group = fields.Char(string="Grupo", tracking=True)
    campaign = fields.Char(string="Campaña", tracking=True)
    trainner = fields.Char(string="Entrenador", tracking=True)

    applicant_signature = fields.Binary(string="Firma del aplicante", tracking=True)
    quality_signature = fields.Binary(string="Firma del Técnico de calidad", tracking=True)
    manager_signature = fields.Binary(string="Firma del responsable de capacitación y calidad", tracking=True)

    strengths = fields.Text(string="Fortalezas", tracking=True)
    opportunity_areas = fields.Text(string="Areas de Oportunidad", tracking=True)
    suggestions_quality_technician = fields.Text(string="Sugerencias del Técnico de Calidad", tracking=True)
    prospectus_commitments = fields.Text(string="Compromisos Prospecto", tracking=True)

    state = fields.Selection(FEEDBACK_STATE, string='Estado', default='doing', tracking=True)

    quality_technician = fields.Many2one('hr.employee', string="Tecnico de Calidad", tracking=True)
    training_and_quality_manager = fields.Many2one('hr.employee', string="Responsable de Capacitación y Calidad", tracking=True)
    kardex_id = fields.Many2one('tyt_recruitment.kardex_by_applicant', string="Kardex del aplicante")

    @api.model_create_multi
    def create(self, vals):
        registro = super(CertificationFeeback, self).create(vals)

        if registro.kardex_id and registro.kardex_id.attendance_id:
            group = str(registro.kardex_id.attendance_id.id) or ""
            trainer = registro.kardex_id.attendance_id.trainer.name or ""
            campaign = registro.kardex_id.attendance_id.campaign_id.display_name or ""
            applicant_name = registro.kardex_id.applicant_name or ""
            evaluation_average = registro.kardex_id.average or 0.0
        
            registro.write({
                'group': group,
                'campaign': campaign,
                'trainner': trainer,
                'name': applicant_name,
                'evaluation_average': evaluation_average
            })
        
        return registro

    @api.onchange('quality_signature', 'manager_signature')
    def _compute_state(self):

        if self.quality_signature and self.manager_signature:
            self.state = 'finalized'
        else:
            self.state = 'doing'
    
    def action_view_notify(self):
        self.ensure_one()

        # Obtener correos
        emails = filter(None, [
            self.quality_technician.work_email, 
            self.training_and_quality_manager.work_email,
        ])

        # Unir los correos con coma
        email_to = ",".join(emails) if emails else False  

        # Obtener plantilla de correo
        template = self.env.ref('tyt_recruitment.email_template_certification_feedback', raise_if_not_found=False)

        # Actualizar estado
        self.state = 'notified'
        
        if template and email_to:
            template.with_context(email_to=email_to).send_mail(self.id, force_send=True)