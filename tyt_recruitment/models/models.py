# -*- coding: utf-8 -*-

from odoo import api, models, fields, tools
import uuid
from io import BytesIO
import base64
from datetime import datetime

class Requisition(models.Model):
    _name = 'tyt_recruitment.requisition'
    _description = 'Requisición'
    _rec_name = 'request_date'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'iso_base.email_basic']

    request_date = fields.Datetime(required=True, string="Fecha de solicitud", tracking=True)
    closing_date = fields.Datetime(required=True, string="Fecha de cierre", tracking=True)
    week = fields.Char(string="Semana", default="0", tracking=True)
    state = fields.Selection([('draft', "En creación"),('sent', "Enviado"),], string="Estado", required=True, tracking=True, default='draft')

    campaign_ids = fields.One2many("tyt_recruitment.campaign", "requisition_id", string="Campaña", tracking=True)
    employee_ids = fields.Many2many('hr.employee', string="Empleados relacionados")

    access_token = fields.Char(string="Access Token", default=lambda self: str(uuid.uuid4()), readonly=True, copy=False)

    @api.onchange('request_date')
    def _onchange_request_date(self):
        if self.request_date:
            date_obj = self.request_date.date()
            week_num = date_obj.isocalendar()[1]
            self.week = str(week_num)
        else:
            self.week = "0"

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

    current_staff = fields.Integer(required=True, string="Personal actual", tracking=True)
    goal_staff = fields.Integer(required=True, string="Personal objetivo", tracking=True)
    request_staff = fields.Integer(required=True, string="Personal requerido", tracking=True)
    turn = fields.Selection([('T/M', 'T/M'), ('T/V', 'T/V'), ('T/N', 'T/N')], string="Turno", tracking=True)
    priority = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], string="Prioridad", tracking=True)


    requisition_id = fields.Many2one("tyt_recruitment.requisition")
    tag_id = fields.Many2one('hr.department', string='Dept', options={'no_create': True}, required=True)
    # tag_id = fields.Many2one("tyt_recruitment.tag", string="Campaña")

class Tag(models.Model):
    _name = 'tyt_recruitment.tag'
    _description = 'Etiqueta'

    name = fields.Char(required=True, help="Rellene el campo", tracking=True)