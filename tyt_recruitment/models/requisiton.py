# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.http import request
import uuid
from io import BytesIO
import base64
from datetime import datetime

import logging
_logger = logging.getLogger(__name__)

class Requisition(models.Model):
    _name = 'tyt_recruitment.requisition'
    _description = 'Requisición'
    _rec_name = 'request_date'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'iso_base.email_basic']

    request_date = fields.Date(required=True, string="Fecha de solicitud", tracking=True)
    closing_date = fields.Date(required=True, string="Fecha de cierre", tracking=True)
    state = fields.Selection([('draft', "En creación"),('sent', "Enviado"),], string="Estado", required=True, tracking=True, default='draft')

    site_id = fields.Many2one("x_sitio", string='Sitio', tracking=True, store=True)
    periodo_id = fields.Many2one("x_periodo", string='Semana', tracking=True)
    campaign_ids = fields.One2many("tyt_recruitment.campaign", "requisition_id", string="Campaña", tracking=True)
    employee_ids = fields.Many2many('hr.employee', string="Empleados relacionados")

    access_token = fields.Char(string="Access Token", default=lambda self: str(uuid.uuid4()), readonly=True, copy=False)

    @api.model
    def default_get(self, fields_list):
        vals = super(Requisition, self).default_get(fields_list)
        
        current_user = self.env.user

        if current_user.x_studio_sitio:
            vals['site_id'] = current_user.x_studio_sitio.id
        
        current_date = datetime.now().date()
        
        current_period = request.env['x_periodo'].sudo().search([
            ('x_studio_f1', '<=', current_date),
            ('x_studio_f2', '>=', current_date),
            ('x_studio_tipo_periodo', '>=', 'Semana')
        ], limit=1)

        _logger.info('periodo_id')
        _logger.info(current_period.id)
        _logger.info('Current x_studio_f1')
        _logger.info(current_period.x_studio_f1)
        _logger.info('Current x_studio_f1')
        _logger.info(current_period.x_studio_f2)

        if current_period:
            vals['periodo_id'] = current_period.id
            vals['request_date'] = current_period.x_studio_f1
            vals['closing_date'] = current_period.x_studio_f2

        return vals

    @api.model
    def create(self, vals):
        current_user = self.env.user

        if current_user.x_studio_sitio:
            vals['site_id'] = current_user.x_studio_sitio.id
        
        current_date = datetime.now().date()
        
        current_period = request.env['x_periodo'].sudo().search([
            ('x_studio_f1', '<=', current_date),
            ('x_studio_f2', '>=', current_date),
            ('x_studio_tipo_periodo', '>=', 'Semana')
        ], limit=1)

        if current_period:
            vals['periodo_id'] = current_period.id
            vals['request_date'] = current_period.x_studio_f1
            vals['closing_date'] = current_period.x_studio_f2

        return super(Requisition, self).create(vals)

    def get_emails(self):
        emails = []
        for requisition in self:
            for employee in requisition.employee_ids:
                if employee.work_email:
                    emails.append(employee.work_email)
        return ','.join(emails)

    def get_share_url(self):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        share_url = f'{base_url}/recruitment/{self.id}/{self.access_token}'
        return share_url

    def _create_attachment(self):
        report_obj = self.env['report.tyt_recruitment.report_requisition']
        report_stream = BytesIO()
        
        # Genera el archivo XLSX usando el método generate_xlsx_report
        report_content = report_obj.generate_xlsx_report(None, None, self)
        report_stream.write(report_content)
        report_stream.seek(0)
        
        encoded_content = base64.b64encode(report_stream.getvalue()).decode('ascii')
        
        attachment = self.env['ir.attachment'].create({
            'name': 'requisition_report.xlsx',
            'type': 'binary',
            'datas': encoded_content,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'res_model': self._name,
            'res_id': self.id,
        })
        return attachment

    def action_open_popup(self):
        self.ensure_one()
        lang = self.env.context.get('lang')
        template = self.env.ref('tyt_recruitment.mail_template_requisition')

        # Generar el archivo XLS y adjuntarlo al correo

        report = self.env.ref('tyt_recruitment.action_report_report_requisition')

        generated_report = report._render_xlsx('tyt_recruitment.action_report_report_requisition', docids=self.id, data=())
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
            'default_model': 'tyt_recruitment.requisition',
            'default_template_id': template.id if template else None,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'default_email_to': self.get_emails(),
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
    
    def action_confirm(self):
        self.ensure_one()
        self.state ='sent'
        return {'type': 'ir.actions.client', 'tag':'reload'}
    
    @api.onchange('state')
    def _onchange_state(self):
        if self.state == 'sent':
            for field in self.fields_get():
                if field not in ('state', 'id'):  # Exclude 'state' and 'id' fields from readonly
                    self[field].readonly = True
    
class Campaign(models.Model):
    _name = 'tyt_recruitment.campaign'
    _description = 'Campania'
    # _rec_name = 'tag_id.name'

    current_staff = fields.Integer(required=True, string="Personal actual", tracking=True)
    goal_staff = fields.Integer(required=True, string="Personal objetivo", tracking=True)
    request_staff = fields.Integer(required=True, string="Personal requerido", tracking=True)
    turn = fields.Selection([('T/M', 'T/M'), ('T/V', 'T/V'), ('T/N', 'T/N')], string="Turno", tracking=True)
    priority = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], string="Prioridad", tracking=True)


    requisition_id = fields.Many2one("tyt_recruitment.requisition")
    tag_id = fields.Many2one('hr.department', string='Dept', options={'no_create': True}, required=True)

    def action_open_job_application(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/job_application/'+str(self.requisition_id.id)+'/'+ str(self.requisition_id.site_id.id)+'/'+str(self.id),
            'target': 'new', 
        }

    def action_close_applicant_list(self):
        return {'type': 'ir.actions.act_window_close'}
    
    def action_open_applicant_list(self):

        tag_id = self.env.context.get('tag_id')
        applicants = request.env['tyt_recruitment.applicant'].sudo().search([('campaign_id', '=', int(tag_id))])
        _logger.info(len(applicants))

        return {
            'name': 'Lista de aplicantes',
            'type': 'ir.actions.act_window',
            'res_model': 'tyt_recruitment.applicant',
            'view_mode': 'tree',
            'target': 'new',
            'domain': [('id', 'in', applicants.ids)],
            'context': {
                'default_message': 'Este es un mensaje personalizado para la lista de candidatos.'
            }
        }