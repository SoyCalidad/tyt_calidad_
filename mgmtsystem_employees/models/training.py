# -*- coding: utf-8 -*-

import smtplib
import ssl
import base64
import tempfile
from datetime import date, datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


from odoo import _, api, fields, models
from odoo.exceptions import RedirectWarning, UserError, ValidationError, Warning


class Training(models.Model):
    _name = "mgmtsystem.plan.training"
    _inherit = ['mgmtsystem.validation.mail', 'mgmtsystem.code']
    _description = "Plan de Capacitaciones"
    _order = 'date_training, month_training asc'

    plan_id = fields.Many2one(
        string='Programa',
        comodel_name='mgmtsystem.plan',
        ondelete='cascade',
    )

    name = fields.Char(
        string=u'Tema',
        required=True,
    )
    informed = fields.Boolean(string='Comunicado')

    responsible_ex_id = fields.Many2one('res.partner', string='Responsable')
    responsible_in_id = fields.Many2one('hr.employee', string='Responsable')
    responsible_status = fields.Boolean(string='Responsable externo')

    exponent_id = fields.Reference(
        selection=[('hr.employee', 'Expositor interno'),
                   ('res.partner', 'Expositor externo'), ],
        string="Expositor")
    month_training = fields.Selection([
        ('1', 'Enero'),
        ('2', 'Febrero'),
        ('3', 'Marzo'),
        ('4', 'Abril'),
        ('5', 'Mayo'),
        ('6', 'Junio'),
        ('7', 'Julio'),
        ('8', 'Agosto'),
        ('9', 'Septiembre'),
        ('10', 'Octubre'),
        ('11', 'Noviembre'),
        ('12', 'Diciembre'),
    ],
        string=u'Mes',
        required=True,
    )
    date_training = fields.Datetime(
        string=u'Fecha',
        tracking=True
    )

    duration = fields.Float(
        string=u'Duración',
    )
    minutes_duration = fields.Float(
        compute='_compute_minutes_duration'
    )
    type = fields.Selection(
        string=u'Tipo',
        selection=[('I', 'Interna'), ('E', 'Externa')],
    )
    aproval = fields.Boolean(
        string=u'Aprobado',
        default=False,
    )

    reference = fields.Char(
        string="Referencia",
        readonly=True,
        required=True,
        copy=False,
        default='Sin definir'
    )

    observations = fields.Text(
        string=u'Observaciones',
    )

    state = fields.Selection(
        string=u'Estado',
        selection=[
            ('elaborate', 'En elaboración'),
            ('validate_ok', 'Validado'),
            ('in_process', 'En proceso'),  # incluye etapa de evaluación
            ('final', 'Finalizado'),
            ('caducated', 'Caducado'),
            ('cancel', 'Obsoleto'),
        ],
        default='elaborate',
        copy=False,
    )

    line_ids = fields.One2many(
        string=u'Asistentes',
        comodel_name='mgmtsystem.plan.training.line',
        inverse_name='training_id',
    )

    employee_ids = fields.Many2many(
        string=u'Empleados',
        comodel_name='hr.employee',
        relation='employee_training_rel',
        column1='employee_id',
        column2='training_id',
    )

    @api.depends('duration')
    def _compute_minutes_duration(self):
        for each in self:
            each.minutes_duration = round(each.duration * 60)

    def action_notify_employee(self):
        for each in self:
            self.env.cr.execute("""SELECT id FROM ir_model
                            WHERE model = %s""", (str(each._name),))
            info = self.env.cr.dictfetchall()
            if info:
                model_id = info[0]['id']
            message = ""
            for e in each.employee_ids:
                try:
                    if e.user_id:
                        self.env['mail.activity'].create({
                            'res_id': each.ids[0],
                            'res_model_id': model_id,
                            'res_model': each._name,
                            'summary': 'Invitación',
                            'note': 'Queda cordialmente invitado a la capacitación ' + each.name + ' el ' + each.date_training.strftime('%d/%m/%Y'),
                            'date_deadline': each.date_training,
                            'user_id': e.user_id.id,
                        })
                    elif e.parent_id:
                        if e.parent_id.user_id:
                            self.env['mail.activity'].create({
                                'res_id': each.ids[0],
                                'res_model_id': model_id,
                                'res_model': each._name,
                                'summary': 'Invitación a empleado',
                                'note': 'El empleado '+e.name+' queda cordialmente invitado a la capacitación '+each.name+' el '+each.date_training.strftime('%d/%m/%Y'),
                                'date_deadline': each.date_training,
                                'user_id': e.parent_id.user_id.id,
                            })
                    else:
                        message = message + '<li>'+e.name+'</li>'
                except:
                    pass
            if message != "":
                each.message_post(
                    body='Empleados que no recibieron notificación:<br></br>'+message)

    def action_print_survey(self):
        typesurvey = self._context.get('typesurvey', False)
        if typesurvey == 'employee':
            return self.employee_survey_id.action_print_survey()
        if typesurvey == 'exponent':
            return self.exponent_survey_id.action_print_survey()
        if typesurvey == 'efficiency':
            return self.efficiency_survey_id.action_print_survey()

    def get_employees_work_emails(self):
        emails = []
        for each in self:
            for e in each.employee_ids:
                if e.work_email:
                    emails.append(e.work_email)
        return emails

    def action_mail_send(self):
        '''
        This function opens a window to compose an email, with the edi purchase template message loaded by default
        '''
        self.ensure_one()
        template = 'mgmtsystem_employees.email_template_mgmtsystem_plan_training'
        return self.notify_users_by_email(template)

    employee_survey_id = fields.Many2one(
        string=u'Formulario de empleado',
        comodel_name='survey.survey',
        ondelete='cascade',
    )

    exponent_survey_id = fields.Many2one(
        string=u'Formulario de expositor',
        comodel_name='survey.survey',
        ondelete='cascade',
    )

    efficiency_survey_id = fields.Many2one(
        string=u'Formulario de eficiencia',
        comodel_name='survey.survey',
        ondelete='cascade',
    )

    def send_process(self):
        lines = [(5, 0, 0)]
        for e in self.employee_ids:
            data = {
                'training_id': self.id,
                'employee_id': e.id,
                'assistance': 'A',
            }
            lines.append((0, 0, data))
        self.line_ids = lines
        self.write({'state': 'in_process'})

    def send_final(self):
        self.write({'state': 'final'})

    def send_cancel(self):
        self.write({'state': 'cancel'})

    def write(self, values):
        if values.get('reference', 'Sin definir') == 'Sin definir' and values.get('state', False) == 'validate_ok':
            values['reference'] = self.env['ir.sequence'].next_by_code(
                'capacitacion.sequence') or 'Sin definir'

        result = super(Training, self).write(values)
        return result


class TrainingLine(models.Model):
    _name = "mgmtsystem.plan.training.line"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Linea de capacitaciones"

    training_id = fields.Many2one(
        string=u'Capacitacion',
        comodel_name='mgmtsystem.plan.training',
        ondelete='cascade',
    )

    name = fields.Char(
        string=u'Nombre',
        related='training_id.name',
        readonly=True,
        store=True,
    )

    state = fields.Selection(
        string=u'Estado',
        selection=[
            ('elaborate', 'En elaboración'),
            ('validate_ok', 'Validado'),
            ('in_process', 'En proceso'),
            ('final', 'Finalizado'),
            ('caducated', 'Caducado'),
            ('cancel', 'Obsoleto'),
        ],
        related='training_id.state',
        readonly=True,
        store=True
    )

    employee_id = fields.Many2one(
        string=u'Empleado',
        comodel_name='hr.employee',
        required=True,
    )

    department = fields.Char(
        string=u'Departamento',
        related='employee_id.department_id.name',
        readonly=True,
        store=True
    )

    assistance = fields.Selection(
        string=u'Asistencia',
        selection=[
            ('A', 'Asistió'),
            ('T', 'Tarde'),
            ('F', 'Faltó'),
        ],
        default='A',
        required=True,
    )

    state_test = fields.Selection(
        string=u'Estado de prueba',
        selection=[('disapproved', 'Desaprobado'), ('approved', 'Aprobado')]
    )

    observations = fields.Text(
        string=u'Observaciones',
    )

    @api.depends('employee_id')
    def _compute_has_attachments(self):
        for each in self:
            nbr_attach = each.env['training.document'].search_count([
                '&', ('res_model', '=', 'mgmtsystem.plan.training.line'), ('res_id', '=', each.id)])
            each.has_attachments = bool(nbr_attach)

    has_attachments = fields.Boolean(
        'Tiene documentos', compute='_compute_has_attachments')

    note = fields.Float(
        string=u'Nota',
        store=True,
        readonly=False,
    )

    employee_survey_id = fields.Many2one(
        string=u'Formulario de empleado',
        comodel_name='survey.survey',
        related='training_id.employee_survey_id',
        ondelete='cascade',
    )
    emresponse_id = fields.Many2one(
        'survey.user_input', "Respuesta empleado", ondelete="set null", )

    exponent_survey_id = fields.Many2one(
        string=u'Formulario de expositor',
        comodel_name='survey.survey',
        related='training_id.exponent_survey_id',
        ondelete='cascade',
    )
    exresponse_id = fields.Many2one(
        'survey.user_input', "Respuesta expositor", ondelete="set null", )

    efficiency_survey_id = fields.Many2one(
        string=u'Formulario de eficiencia',
        comodel_name='survey.survey',
        related='training_id.efficiency_survey_id',
        ondelete='cascade',
    )
    efresponse_id = fields.Many2one(
        'survey.user_input', "Respuesta eficiencia", ondelete="set null", oldname="response")

    confirm = fields.Boolean(string='Confirmación')

    def action_start_survey(self):
        self.ensure_one()
        typesurvey = self._context.get('typesurvey', False)
        if typesurvey == 'employee':
            if not self.emresponse_id:
                response = self.env['survey.user_input'].create(
                    {'survey_id': self.employee_survey_id.id})
                self.emresponse_id = response.id
            else:
                response = self.emresponse_id
            return self.employee_survey_id.with_context(survey_token=response.token).action_start_survey()
        if typesurvey == 'exponent':
            if not self.exresponse_id:
                response = self.env['survey.user_input'].create(
                    {'survey_id': self.exponent_survey_id.id})
                self.exresponse_id = response.id
            else:
                response = self.exresponse_id
            return self.exponent_survey_id.with_context(survey_token=response.token).action_start_survey()
        if typesurvey == 'efficiency':
            if not self.efresponse_id:
                response = self.env['survey.user_input'].create(
                    {'survey_id': self.efficiency_survey_id.id})
                self.efresponse_id = response.id
            else:
                response = self.efresponse_id
            return self.efficiency_survey_id.with_context(survey_token=response.token).action_start_survey()

    def action_print_survey(self):
        self.ensure_one()
        typesurvey = self._context.get('typesurvey', False)
        if typesurvey == 'employee':
            if not self.emresponse_id:
                return self.employee_survey_id.action_print_survey()
            else:
                response = self.emresponse_id
                return self.employee_survey_id.with_context(survey_token=response.token).action_print_survey()
        if typesurvey == 'exponent':
            if not self.emresponse_id:
                return self.exponent_survey_id.action_print_survey()
            else:
                response = self.emresponse_id
                return self.exponent_survey_id.with_context(survey_token=response.token).action_print_survey()
        if typesurvey == 'efficiency':
            if not self.emresponse_id:
                return self.efficiency_survey_id.action_print_survey()
            else:
                response = self.emresponse_id
                return self.efficiency_survey_id.with_context(survey_token=response.token).action_print_survey()

    def action_see_attachments(self):
        domain = [
            '&', ('res_model', '=', 'mgmtsystem.plan.training.line'), ('res_id', '=', self.id), ]
        attachment_view = self.env.ref(
            'mgmtsystem_employees.view_document_file_kanban_training')
        return {
            'name': _('Adjuntos'),
            'domain': domain,
            'res_model': 'training.document',
            'type': 'ir.actions.act_window',
            'view_id': attachment_view.id,
            'views': [(attachment_view.id, 'kanban'), (False, 'form')],
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                        Haga clic para cargar archivos de la capacitación
                    </p><p>
                        Utilice esta función para almacenar cualquier archivo.
                    </p>'''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % ('mgmtsystem.plan.training.line', self.id)
        }

    def print_certficate(self):
        return self.env.ref('mgmtsystem_employees.action_report_training_certificate').report_action(self.id)


class TrainingDocument(models.Model):
    """ Extension of ir.attachment only used in MRP to handle archivage
    and basic versioning.
    """
    _name = 'training.document'
    _description = "Training Document"
    _inherits = {
        'ir.attachment': 'ir_attachment_id',
    }
    _order = "priority desc, id desc"

    ir_attachment_id = fields.Many2one(
        'ir.attachment', string='Related attachment', required=True, ondelete='cascade')
    active = fields.Boolean('Active', default=True)
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority", help='Gives the sequence order when displaying a list of MRP documents.')
