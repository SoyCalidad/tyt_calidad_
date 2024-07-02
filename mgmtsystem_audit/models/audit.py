# -*- coding: utf-8 -*-


from datetime import datetime

from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError, Warning


class AuditTeam(models.Model):
    _name = "audit.team"
    _description = "Equipo de auditoría"

    name = fields.Char(
        string='Nombre',
        required=True,
    )
    user_ids = fields.Many2many(
        string='Miembros',
        comodel_name='res.partner',
    )


class Audit(models.Model):
    _name = "audit.audit"
    _inherit = ['mgmtsystem.validation.mail', 'mgmtsystem.code']
    _description = "Plan de auditoría"

    responsable_id = fields.Many2one('res.users', string='Responsable')

    plan_id = fields.Many2one(
        string=u'Programa',
        comodel_name='audit.plan',
        ondelete='cascade',
    )

    name = fields.Char(
        string=u'Actividad',
        required=True,
    )
    auditor_id = fields.Reference(selection=[('res.partner', 'Auditor externo'), (
        'hr.employee', 'Auditor interno'), ], string="Auditor")
    team_id = fields.Many2one(
        string=u'Equipo',
        comodel_name='audit.team',
        ondelete='cascade',
    )
    location = fields.Char(u'Lugar de auditoría')
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

    @api.onchange('month_training')
    def _onchange_month_training(self):
        if not self.month_training:
            return
        datetmp = datetime(year=datetime.today(
        ).year, month=int(self.month_training), day=datetime.today().day)

        self.date_init = datetmp
        self.date_fin = datetmp

    date_init = fields.Datetime(
        string=u'Fecha de inicio',
        default=fields.Datetime.now,
        copy=False,
    )
    date_fin = fields.Datetime(
        string=u'Fecha de finalización',
        copy=False,
    )

    duration = fields.Float(
        string=u'Duración',
    )

    @api.onchange('date_init', 'date_fin')
    def _onchange_date(self):
        for record in self:
            if record.date_fin and record.date_init:
                duration = record.date_fin - record.date_init
                record.duration = duration.days * 24 + duration.seconds / 3600

    type = fields.Selection(
        string=u'Tipo',
        selection=[('I', 'Interna'), ('E', 'Externa')],
    )
    process_id = fields.Many2one(
        string='Proceso',
        comodel_name='mgmt.process',
        ondelete='cascade',
        domain=[('active','=',True)]
    )
    aproval = fields.Boolean(
        string=u'Aprobado',
        default=False,
    )
    observations = fields.Text(
        string=u'Observaciones/Alcance',
        required=True,
    )
    golds = fields.Text(
        string=u'Objetivos',
    )

    report_count = fields.Integer(
        string=u'Informes',
        compute='_compute_report_count',
        store=False,
    )

    @api.depends('report_ids')
    def _compute_report_count(self):
        for record in self:
            record.report_count = len(record.report_ids) or 0

    report_ids = fields.One2many(
        string=u'Reportes',
        comodel_name='audit.report',
        inverse_name='audit_id',
    )

    line_ids = fields.One2many(
        string=u'Lineas',
        comodel_name='audit.line',
        inverse_name='audit_id',
    )

    def action_notify_employee(self):
        for each in self:
            self.env.cr.execute("""SELECT id FROM ir_model 
                            WHERE model = %s""", (str(each._name),))
            info = self.env.cr.dictfetchall()
            if info:
                model_id = info[0]['id']
            message = ""
            for e in each.line_ids:
                datetime = e.datetime.strftime(
                    '%d/%m/%Y') if e.datetime else ''
                if e.employee_id.user_id:
                    self.env['mail.activity'].create({
                        'res_id': each.ids[0],
                        'res_model_id': model_id,
                        'res_model': each._name,
                        'summary': 'Invitación',
                        'note': 'Queda cordialmente invitado a la auditoría: "'+e.name+'" el '+datetime,
                        'date_deadline': e.datetime,
                        'user_id': e.employee_id.user_id.id,
                    })
                elif e.employee_id.parent_id:
                    if e.employee_id.parent_id.user_id:
                        self.env['mail.activity'].create({
                            'res_id': each.ids[0],
                            'res_model_id': model_id,
                            'res_model': each._name,
                            'summary': 'Invitación a empleado',
                            'note': 'El empleado '+e.employee_id.name+' queda cordialmente invitado a la auditoría: '+e.name+' el '+datetime,
                            'date_deadline': e.datetime,
                            'user_id': e.employee_id.parent_id.user_id.id,
                        })
                else:
                    employee_id = e.employee_id.name if e.employee_id else ''
                    message = message + '<li>' + employee_id + '</li>'
            if message != "":
                each.message_post(
                    body='Empleados que no recibieron notificación:<br></br>'+message)
            each.send_send()

    def get_emails(self):
        emails = []
        for each in self.line_ids:
            if each.employee_id.work_email:
                emails.append(tools.email_normalize(each.employee_id.work_email))
        work_emails = ','.join(
            [x.employee_id.work_email for x in self.line_ids if x.employee_id and x.employee_id.work_email])

        return work_emails

    def action_mail_send(self):
        '''
        Send a email with the audit plan and schedule to the employees
        '''
        self.ensure_one()
        template = 'mgmtsystem_audit.email_template_mgmtsystem_audit'
        self.send_send()
        return self.notify_users_by_email(template)

    def open_audit_report_form(self):
        return {
            'res_model': 'audit.report',
            'type': 'ir.actions.act_window',
            'context': {'default_audit_id': self.id},
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'view_id': self.env.ref("mgmtsystem_audit.view_audit_report_form").id,
        }


class AuditLine(models.Model):
    _name = 'audit.line'
    _order = 'sequence, name, datetime'

    audit_id = fields.Many2one(
        string=u'Auditoría',
        comodel_name='audit.audit',
        ondelete='restrict',
    )

    name = fields.Text(
        string=u'Proceso/Función',
        required=True,
    )

    datetime = fields.Datetime(
        string=u'Fecha de auditoría',
        default=lambda self: self.audit_id.date_init
    )
    department_id = fields.Many2one(
        string=u'Departamento',
        comodel_name='hr.department',
        ondelete='cascade',
    )
    employee_id = fields.Many2one(
        string=u'Responsable',
        comodel_name='hr.employee',
    )
    observations = fields.Text(u'Observaciones')

    auditor_ids = fields.Many2many('res.partner', string='Auditores')
    sequence = fields.Integer(
        string=u'Secuencia',
        default=10,
    )

    @api.constrains('datetime')
    def _check_datetime(self):
        for record in self:
            if not record.audit_id:
                return
            if record.datetime and record.audit_id.date_init and record.datetime < record.audit_id.date_init:
                raise ValidationError(
                    _('La fecha de %s no puede ser anterior a la fecha de inicio de auditoría') % (record.name))


class AuditReport(models.Model):
    _name = "audit.report"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'mgmtsystem.code']

    audit_id = fields.Many2one(
        string=u'Auditoría',
        comodel_name='audit.audit',
        ondelete='restrict',
    )

    line_ids = fields.One2many(
        string=u'Lineas',
        comodel_name='report.line',
        inverse_name='report_id',
        copy=True,
    )

    name = fields.Char(
        string=u'Nombre',
        required=True,
    )
    datetime_ = fields.Datetime(string='Fecha', related='audit_id.date_init')
    location = fields.Char(u'Lugar de auditoría')
    standard = fields.Char(
        string=u'Requisito de la norma',
    )
    scope = fields.Text(u'Alcance', required=True)
    golds = fields.Text(
        string=u'Objetivos',
    )
    auditor_id = fields.Reference(selection=[('res.partner', 'Auditor externo'), (
        'hr.employee', 'Auditor interno'), ], string="Auditor")
    team_id = fields.Many2one(
        string=u'Equipo',
        comodel_name='audit.team',
        ondelete='cascade',
    )
    state = fields.Selection(
        string=u'Estado',
        selection=[
            ('draft', 'Borrador'),
            ('in_process', 'Pendiente'),
            ('close', 'Concluido'),
        ],
        default='draft',
    )

    conclusions = fields.Text('Conclusiones')

    @api.onchange('audit_id')
    def _onchange_audit_id(self):
        self.name = 'Informe de '+self.audit_id.name if self.audit_id else ""
        self.location = self.audit_id.location
        self.auditor_id = self.audit_id.auditor_id
        self.team_id = self.audit_id.team_id
        self.scope = self.audit_id.observations
        self.golds = self.audit_id.golds
        self.scope = self.audit_id.observations
        datas = [(5, 0, 0)]
        for line in self.audit_id.line_ids:
            data = {
                'report_id': self.id,
                'name': line.name,
                'employee_id': line.employee_id.id,
                'date_audit': line.datetime,
                # 'nc_id': line.type_id.id,
            }
            datas.append((0, 0, data))
        self.line_ids = datas

    def send_final(self):
        self.write({'state': 'close'})


class img_adjunt(models.Model):
    _name = "img.adjunt"

    name = fields.Char(
        string=u'Nombre',
        help="Nombre de la img",
        required=True,

    )
    image_attached = fields.Binary("Adjunto",
                                   attachment=True,
                                   help="This field holds the image used as avatar for \
        this contact, limited to 1024x1024px",
                                   )

    report_line_id = fields.Many2one(
        comodel_name='report.line',
        string="Nombre del Proceso/función",
        help="Nombre del proceso o funcion // Primero se debe de crar el proceso  ",
        default="",
    )


class ReportLine(models.Model):
    _name = "report.line"

    report_id = fields.Many2one(
        string=u'Reporte',
        comodel_name='audit.report',
        ondelete='restrict',
    )

    name = fields.Text(
        string=u'Proceso/Función',
        required=True,
    )
    date_audit = fields.Date(
        string=u'Fecha de auditoría',
        default=fields.Date.context_today,
    )
    partner_id = fields.Many2one(
        string=u'Auditado',
        comodel_name='res.partner',
    )
    employee_id = fields.Many2one('hr.employee', string='Empleado')
    datetime = fields.Datetime(
        string=u'Fecha de hallazgo',
    )
    found = fields.Text(u'Hallazgo')
    image_attached = fields.Binary("Adjunto",
                                   attachment=True,
                                   help="This field holds the image used as avatar for \
        this contact, limited to 1024x1024px",
                                   )

    observations = fields.Text(u'Observaciones')

    @api.depends('report_id')
    def _compute_has_attachments(self):
        for each in self:
            nbr_attach = self.env['report.line.document'].search_count([
                '&', ('res_model', '=', 'report.line'), ('res_id', '=', each.id)])
            each.has_attachments = bool(nbr_attach)

    has_attachments = fields.Boolean(
        'Tiene documentos', compute='_compute_has_attachments')

    def action_see_attachments(self):
        domain = [
            '&', ('res_model', '=', 'report.line'), ('res_id', '=', self.id), ]
        attachment_view = self.env.ref(
            'mgmtsystem_audit.view_document_file_kanban_report_line')
        return {
            'name': _('Adjuntos'),
            'domain': domain,
            'res_model': 'report.line.document',
            'type': 'ir.actions.act_window',
            'view_id': attachment_view.id,
            'views': [(attachment_view.id, 'kanban'), (False, 'form')],
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                        Haga clic para cargar archivos de evidencia
                    </p><p>
                        Utilice esta función para almacenar cualquier archivo.
                    </p>'''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % ('report.line', self.id)
        }


class ReportLineDocument(models.Model):
    _name = 'report.line.document'
    _description = "Documento de reporte de auditoría"
    _inherits = {
        'ir.attachment': 'ir_attachment_id',
    }
    _order = "priority desc, id desc"

    ir_attachment_id = fields.Many2one(
        'ir.attachment', string='Documentos adjuntos', required=True, ondelete='cascade')
    active = fields.Boolean('Activo', default=True)
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Bajo'),
        ('2', 'Alto'),
        ('3', 'Muy alto')], string="Prioridad", help='Da la secuencia')
