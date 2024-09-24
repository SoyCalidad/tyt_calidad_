# -*- coding: utf-8 -*-

from odoo import api, models, fields
import uuid
from io import BytesIO
import base64

class ProspectGroup(models.Model):
    _name = 'tyt_recruitment.pgroup'
    _description = 'Grupo de Prospectos'
    _rec_name = 'register_date'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'iso_base.email_basic']
    
    week = fields.Integer(string='Semana', required=True, tracking=True)
    prospects = fields.Integer(string='Prospect', required=True, tracking=True)
    turn_m = fields.Char(string='T/M', required=True, tracking=True)
    turn_v = fields.Char(string='T/V', required=True, tracking=True)
    group = fields.Integer(string='Grupo', required=True, tracking=True)
    register_date = fields.Datetime(string="Fecha de registro", default=fields.Datetime.now, tracking=True)
    state = fields.Selection([('draft', "En creación"),('sent', "Enviado"),], string="Estado", required=True, tracking=True, default='draft')
    access_token = fields.Char(string="Access Token", default=lambda self: str(uuid.uuid4()), readonly=True, copy=False)

    # site_id = fields.Many2One(string='Site', required=True)
    site_id = fields.Char(string='Sitio', required=True, tracking=True)
    prospect_ids = fields.One2many("tyt_recruitment.prospect", "group_id", string='Prospectos', tracking=True)

    access_token = fields.Char(string="Access Token", default=lambda self: str(uuid.uuid4()), readonly=True, copy=False)
    employee_ids = fields.Many2many('hr.employee', string="Empleados relacionados")

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
        template = self.env.ref('tyt_recruitment.mail_template_prospects')

        # Generar el archivo XLS y adjuntarlo al correo

        report = self.env.ref('tyt_recruitment.action_report_report_pgroup')

        generated_report = report._render_xlsx('tyt_recruitment.action_report_report_pgroup', docids=self.id, data=())
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
            'default_model': 'tyt_recruitment.pgroup',
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

class Prospect(models.Model):
    _name = 'tyt_recruitment.prospect'
    _description = 'Prospecto'

    names = fields.Char(string='Nombre', required=True)
    paternal_surname = fields.Char(string='Apellido paterno', required=True)
    maternal_surname = fields.Char(string='Apellido materno', required=True)
    employee_number = fields.Integer(string='Número de empleado', required=True)
    phone_number = fields.Char(string='Teléfono', required=True)
    birthday = fields.Date(string='Fecha de nacimiento', required=True)
    place_birth = fields.Char(string='Lugar de nacimiento', required=True)
    rfc = fields.Char(string='RFC', required=True)
    curp = fields.Char(string='CURP', required=True)
    nss = fields.Char(string='NSS', required=True)

    group_id = fields.Many2one("tyt_recruitment.pgroup")