# -*- coding: utf-8 -*-

import smtplib
import ssl
import tempfile
from datetime import datetime
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pytz
from odoo import _, api, fields, models
from odoo.exceptions import (RedirectWarning, UserError, ValidationError,
                             Warning)


class RecordMeeting(models.Model):
    _name = "record.meeting"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'mgmtsystem.code', 'iso_base.email_basic']
    _description = "Actas de reunion"

    name = fields.Char(
        string=u'Titulo',
        required=True,
    )

    document_id = fields.Many2one(
        string=u'Procedimiento',
        comodel_name='process.edition',
        domain="[('state', '=', 'validate_ok')]",
        ondelete='restrict',
    )
    resume = fields.Text(
        string=u'Motivo',
    )
    reference = fields.Char(
        string='Referencia',
    )

    user_id = fields.Many2one(
        string=u'Encargado',
        comodel_name='res.users',
        default=lambda self: self.env.user,
        required=True,
    )

    locate = fields.Char(
        string='Lugar',
    )

    date_release = fields.Datetime(
        string=u'Fecha y hora de reunión',
        default=fields.Datetime.now,
    )
    pre_line_ids = fields.One2many(
        string=u'Agenda Lineas',
        comodel_name='record.meeting.preline',
        inverse_name='record_id',
        copy=True,
    )
    line_ids = fields.One2many(
        string=u'Acuerdos Lineas',
        comodel_name='record.meeting.line',
        inverse_name='record_id',
        copy=True,
    )
    assistance_emp_ids = fields.One2many(
        string=u'Asistencias (interno)',
        comodel_name='assistance.meeting',
        inverse_name='record_id',
        copy=True,
    )
    assistance_par_ids = fields.One2many(
        string=u'Asistencias (externo)',
        comodel_name='assistance.meeting',
        inverse_name='record2_id',
        copy=True,
    )
    employee_ids = fields.Many2many(
        string=u'Convocados internos',
        comodel_name='hr.employee',
        relation='employee_record_rel',
        column1='employee_id',
        column2='record_id',
        copy=True,
    )

    partner_ids = fields.Many2many('res.partner', string='Convocados externos')

    line_id = fields.Many2one(
        string=u'Origen',
        comodel_name='comunication.plan.line',
        ondelete='cascade',
    )

    state = fields.Selection(
        string=u'Estado',
        selection=[
            ('elaborate', 'Convocatoria'),
            ('in_process', 'Ejecución'),
            ('close', 'Cierre'),
        ],
        default='elaborate'
    )

    count_in_process = fields.Integer(
        string=u'# lineas en proceso',
        compute='_compute_count_in_process',
        store=False,
    )

    @api.depends('line_ids')
    def _compute_count_in_process(self):
        for record in self:
            num = self.env['record.meeting.line'].search_count(
                [('record_id', '=', record.id), ('state', '=', 'in_process')])
            record.count_in_process = num

    def send_in_process(self):
        lines_emp = [(5, 0, 0)]
        lines_par = [(5, 0, 0)]

        for e in self.employee_ids:
            data = {
                'record_id': self.id,
                'employee_id': e.id,
                'assistance': 'A',
            }
            lines_emp.append((0, 0, data))

        for p in self.partner_ids:
            data = {
                'record2_id': self.id,
                'partner_id': p.id,
                'assistance': 'A',
            }
            lines_par.append((0, 0, data))

        self.assistance_emp_ids = lines_emp
        self.assistance_par_ids = lines_par

        lines = []
        for e in self.pre_line_ids:
            line = self.env['record.meeting.line'].create({
                'record_id': self.id,
                'name': e.name or "No definido",
                'employee_id': e.employee_id.id,
                'partner_id': e.partner_id.id,
            })
            lines.append(line.id)
        self.line_ids = lines

        # Get the partners ins self.partner_ids and self.employee_ids
        partners = self.partner_ids | self.employee_ids.mapped('user_id.partner_id')
        date_release = self.date_release.strftime("%d/%m/%Y %H:%M")
        self.notify_users_by_system(partners, "Convocatoria a reunión (Nombre: {}) (Fecha: {})".format(self.name, date_release))

        self.state = 'in_process'

    def send_close(self):
        record_meeting_line_approval = self.env['ir.config_parameter'].sudo().get_param(
            'mgmtsystem_comunication.record_meeting_line_approval')
        all_line_ids_checked = all(line.check for line in self.line_ids)
        if record_meeting_line_approval and not all_line_ids_checked:
            raise UserError('No se puede cerrar la reunión, existen lineas sin aprobar')
        self.state = 'close'

    def create_record(self):
        cline_ids = self.env['record.meeting.line'].search(
            [('record_id', '=', self.id), ('state', '=', 'in_process')])
        other_record = self.create({
            'name': '%s:%s' % ("Re", self.name),
            'document_id': self.document_id.id,
            'resume': self.resume,
            'employee_id': self.employee_id.id,
            'partner_ids': self.partner_id.id,
            'date_release': fields.Datetime.now(self)
        })
        other_record.line_ids = cline_ids.ids
        other_record.employee_ids = self.employee_ids
        ###
        action = self.env.ref(
            'mgmtsystem_comunication.record_meeting_action').read()[0]
        action['views'] = [
            (self.env.ref('mgmtsystem_comunication.view_record_meeting_form').id, 'form')]
        action['res_id'] = other_record.id
        return action

    def get_email_list(self):
        for record in self:
            if not record.employee_ids:
                continue
            else:
                res_list = []
                for each in record.employee_ids:
                    if each.work_email:
                        res_list.append(each.work_email)
                    else:
                        continue
                res = ','.join(res_list)
            return res

    def action_mail_send(self):
        '''
        This function opens a window to compose an email
        '''
        self.ensure_one()
        timezone = pytz.timezone(self._context.get(
            'tz') or self.env.user.tz or 'UTC')
        template = self.env.ref(
            'mgmtsystem_comunication.email_template_record_meeting_2')
        for record in self:
            date_release = record.date_release.astimezone(timezone)

            subject = "Convocatoria a reunión (Nombre: {}) (Fecha: {})".format(
                record.name, date_release)
            body_html = """<div style="margin: 0px; padding: 0px;">
                    <p style="margin: 0px; padding: 0px; font-size: 13px;">
        Queda cordialmente invitado a la reunión {} con fecha {}
                        <br />
                        <br />
        Se adjunta acta de reunión:
                    </p>
                </div>""".format(record.name, date_release)
            template.write(
                {'email_to': record.get_email_list(), 'subject': subject, 'body_html': body_html})
            template.send_mail(self.id, force_send=True)
            record.state = 'in_process'
        lines = []
        for e in self.pre_line_ids:
            line = self.env['record.meeting.line'].create({
                'record_id': self.id,
                'name': e.name or "No definido",
                'employee_id': e.employee_id.id,
                'partner_id': e.partner_id.id,
            })
            lines.append(line.id)
        self.line_ids = lines

        lines_emp = [(5, 0, 0)]
        lines_par = [(5, 0, 0)]

        for e in self.employee_ids:
            data = {
                'record_id': self.id,
                'employee_id': e.id,
                'assistance': 'A',
            }
            lines_emp.append((0, 0, data))

        for p in self.partner_ids:
            data = {
                'record2_id': self.id,
                'partner_id': p.id,
                'assistance': 'A',
            }
            lines_par.append((0, 0, data))

        self.assistance_emp_ids = lines_emp
        self.assistance_par_ids = lines_par


        return True


class RecordMeetingPreline(models.Model):
    _name = "record.meeting.preline"
    _description = "Agenda"

    name = fields.Char(
        string=u'Tema',
        required=False,
    )
    record_id = fields.Many2one(
        string=u'Acta de reunión',
        comodel_name='record.meeting',
        ondelete='cascade',
        required=True,
    )
    duration = fields.Float(string='Duración (hrs)', digits=(16, 2))

    user_id = fields.Many2one('res.users', string='Responsable')

    employee_id = fields.Many2one('hr.employee', string='Responsable interno')

    partner_id = fields.Many2one('res.partner', string='Responsable externo')


class RecordMeetingLine(models.Model):
    _name = "record.meeting.line"
    _description = "Acuerdo"
    _rec_name = 'resume'

    record_id = fields.Many2one(
        string=u'Acta de reunión',
        comodel_name='record.meeting',
        ondelete='cascade',
    )

    name = fields.Char(
        string=u'Tema',
        required=True,
    )

    detail = fields.Html(
        string=u'Detalle',
    )
    resume = fields.Html(
        string=u'Acuerdos',
    )

    date_ini = fields.Datetime(
        string=u'Fecha de inicio',
        default=fields.Date.context_today
    )
    date_release = fields.Date(
        string=u'Fecha límite',
    )

    action_ids = fields.Many2many(
        string='Acciones',
        comodel_name='mgmtsystem.action',
        relation='record_meeting_line_action',
        column1='action_id',
        column2='line_id',
    )

    user_id = fields.Many2one(
        string=u'Responsable',
        comodel_name='res.users',
        ondelete='restrict',
    )

    employee_id = fields.Many2one('hr.employee', string='Responsable interno')

    partner_id = fields.Many2one('res.partner', string='Responsable externo')

    state = fields.Selection(
        string='Estado',
        selection=[('in_process', 'En ejecución'), ('close', 'Realizado')],
        default='in_process',
    )
    check = fields.Boolean('Realizado')

    @api.onchange('record_id')
    def _onchange_record_id(self):
        if not self.record_id:
            return
        self.date_release = self.record_id.date_release

    def send_in_process(self):
        self.state = 'in_process'

    def send_close(self):
        self.state = 'close'

    @api.onchange('check')
    def _onchange_check(self):
        if self.check:
            self.state = 'close'
        else:
            self.state = 'in_process'


class AssistanceMeeting(models.Model):
    _name = "assistance.meeting"

    record_id = fields.Many2one(
        string=u'Acta de reunión',
        comodel_name='record.meeting',
        ondelete='cascade',
    )
    record2_id = fields.Many2one(
        string=u'Acta de reunión',
        comodel_name='record.meeting',
        ondelete='cascade',
    )
    employee_id = fields.Many2one(
        string=u'Empleado',
        comodel_name='hr.employee',
        ondelete='restrict',
    )
    partner_id = fields.Many2one('res.partner', string='Contacto')
    datetime = fields.Datetime(
        string=u'Fecha y hora',
    )
    assistance = fields.Selection(
        string=u'Asistencia',
        selection=[('A', 'Asistió'), ('T', 'Tardanza'), ('F', 'Faltó')],
        default='A',
    )

    @api.onchange('assistance')
    def _onchange_field(self):
        if not self.assistance:
            return
        self.datetime = fields.Datetime.now(self)
