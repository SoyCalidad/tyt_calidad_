# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class PlanCateg(models.Model):
    _name = 'comunication.plan.categ'
    _description = "Categoria de plan comunicaciones"

    name = fields.Char(
        string=u'Nombre',
        required=True,
    )
    sequence_id = fields.Many2one(
        string=u'Secuencia de ediciones',
        comodel_name='ir.sequence',
        ondelete='restrict',
    )

    @api.model
    def create(self, values):
        sequence = self.env['ir.sequence'].sudo().create({
            'name': 'Secuencia de '+values.get('name'),
            'active': True,
            'prefix': 'Edición-nro.',
            'padding': 4,
            'number_next': 1,
            'number_increment': 1,
        })
        values['sequence_id'] = sequence.id
        result = super(PlanCateg, self).create(values)
        return result

    def unlink(self):
        for categ in self:
            categ.sequence_id.unlink()
        return super(PlanCateg, self).unlink()

    plan_ids = fields.One2many(
        string='plan',
        comodel_name='comunication.plan',
        inverse_name='categ_id',
    )


class Plan(models.Model):
    _name = "comunication.plan"
    _inherit = ['mgmtsystem.validation.mail', 'mgmtsystem.code']
    _description = "Programa de comunicaciones"

    line_ids = fields.One2many(
        string=u'Lineas',
        comodel_name='comunication.plan.line',
        inverse_name='plan_id',
        copy=True,
    )

    linetrack_ids = fields.One2many(
        string=u'Lineas',
        comodel_name='comunication.plan.line',
        inverse_name='plan_id',
        domain=[('state', 'in', ('on_track', 'closed'))],
        copy=False,
    )

    name = fields.Char(
        string=u'Nombre',
    )

    @api.depends('categ_id', 'reference')
    def _compute_name(self):
        for record in self:
            if not record.categ_id:
                record.name = ''
            record.name = ("%s %s") % (record.categ_id.name, record.numero)

    reference = fields.Char(
        string="Referencia externa",
        readonly=True,
        copy=False,
        default='Sin definir'
    )

    type = fields.Selection([
        ('internal', 'Interna'),
        ('external', 'Externa'),
        ('both', 'Interna y Externa'),
    ], string='Tipo de comunicación')

    categ_id = fields.Many2one(
        string=u'Categoría',
        comodel_name='comunication.plan.categ',
        ondelete='restrict',
    )

    @api.onchange('categ_id')
    def _onchange_categ_id(self):
        self.name = self.categ_id.name

    sequence_id = fields.Many2one(
        string=u'Secuencia de ediciones',
        comodel_name='ir.sequence',
        related='categ_id.sequence_id',
    )

    def _default_edition(self):
        process = self.env['res.company'].browse(
            self.env.user.company_id.id).comunication_process_id
        if process:
            edition = self.env['process.edition'].search([
                ('process_id', '=', process.id),
                ('state', '=', 'validate_ok'),
                ('active', '=', True),
            ], order='create_date desc', limit=1)
            return edition
        else:
            return

    numero = fields.Char(
        string="Numero de secuencia",
        readonly=True,
        required=True,
        copy=False,
        default='Sin definir'
    )

    date_elaborate = fields.Date(
        string=u'Fecha elaboración',
        default=fields.Datetime.now,
        copy=False,
    )
    date_review = fields.Date(
        string=u'Fecha revisado',
        copy=False,
    )
    date_validate = fields.Date(
        string=u'Fecha validado',
        copy=False,
    )

    state = fields.Selection(
        string=u'Estado',
        selection=[
            ('elaborate', 'En elaboración'),
            ('review', 'En revisión'),
            ('validate', 'En validación'),
            ('validate_ok', 'Validado'),
            ('on_track', 'En seguimiento'),
            ('closed', 'Terminado'),
            ('cancel', 'Obsoleto')
        ],
        default='elaborate',
        copy=False,
    )

    def unlink(self):
        for plan in self:
            if plan.state not in ('cancel'):
                raise UserError(
                    _('No puedes eliminar un plan que se encuentre en proceso. Deberías volverlo obsoleto.'))
        return super(Plan, self).unlink()

    def create_action(self, vuser_id):
        action = self.env.ref('hola_calidad.p_mail_activity_action').read()[0]
        self.env.cr.execute("""SELECT id FROM ir_model
                          WHERE model = %s""", (str(self._name),))
        info = self.env.cr.dictfetchall()
        if info:
            model_id = info[0]['id']
        action['context'] = {
            'default_res_id': self.ids[0],
            'default_res_model': self._name,
            'default_res_model_id': model_id,
            'default_user_id': vuser_id,
        }
        return action

    def action_reset_all_aproval(self):
        for training in self.line_ids:
            training.write({'aproval': True})

    def send_cancel(self):
        for training in self.line_ids:
            training.send_cancel()
        self.state = 'cancel'

    def send_on_track(self):
        for training in self.line_ids:
            training.send_on_track()
        self.state = 'on_track'

    def send_closed(self):
        for training in self.line_ids:
            training.send_closed()
        self.state = 'closed'

    def open_line_ids(self):
        """Método para abrir las lineas relacionadas al programa de comunicaciones
        """
        result = self.env.ref(
            'mgmtsystem_comunication.plan_line_action').read()[0]
        result['domain'] = [('id', 'in', self.line_ids.ids)]
        result['context'] = {'default_plan_id': self.id}
        return result


class PlanLine(models.Model):
    _name = "comunication.plan.line"
    _inherit = ['mgmtsystem.validation.mail', 'mgmtsystem.code']
    _description = "Plan de Comunicaciones"
    _rec_name = 'resume'

    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])

    plan_id = fields.Many2one(
        string=u'Programa',
        comodel_name='comunication.plan',
        ondelete='restrict',
    )
    name = fields.Char(
        string=u'Nombre',
        required=False,
    )

    reference = fields.Char(
        string="Referencia",
        readonly=True,
        required=True,
        copy=False,
        default='Sin definir'
    )

    resume = fields.Text(
        string=u'Qué se comunica',
        required=True,
    )
    date_release = fields.Date(
        string=u'Cuándo',
        required=True,
        default=fields.Datetime.now,
    )
    employee_ids = fields.Many2many(
        string=u'Empleados',
        comodel_name='hr.employee',
    )
    partner_ids = fields.Many2many(
        string=u'Contactos',
        comodel_name='res.partner',
    )
    via = fields.Char(
        string=u'Cómo',
    )
    frequency_id = fields.Many2one('mgmtsystem.frequency', string='Frecuencia')
    user_id = fields.Many2one(
        string=u'Quién',
        comodel_name='res.users',
        required=True,
    )
    type = fields.Selection(
        string=u'Tipo',
        selection=[('interna', 'Interna'), ('externa', 'Externa'),
                   ('both', 'Interna y Externa')],
        default='interna',
    )
    reprogramming = fields.Boolean(
        string=u'¿Reprogramación?',
    )
    date_reprogramming = fields.Date(
        string=u'Fecha',
    )
    aproval = fields.Boolean(
        string=u'Aprobado',
        default=False,
    )
    action_id = fields.Many2one(
        string=u'Acción',
        comodel_name='mgmtsystem.action',
        ondelete='cascade',
    )

    observations = fields.Text(
        string=u'Observaciones',
    )

    record_ids = fields.One2many(
        string=u'Actas de reunion',
        comodel_name='record.meeting',
        inverse_name='line_id',
    )
    records_count = fields.Integer(
        string=u'# de actas',
        compute='_compute_records_count',
        store=False,
    )

    @api.depends('record_ids')
    def _compute_records_count(self):
        for record in self:
            record.records_count = ''
            record.records_count = len(record.record_ids) or ''

    def send_on_track(self):
        self.state = 'on_track'

    def send_closed(self):
        self.state = 'closed'

    def send_cancel(self):
        self.state = 'cancel'

    @api.depends('plan_id')
    def _compute_has_attachments(self):
        for each in self:
            nbr_attach = each.env['comunication.plan.line.document'].search_count([
                '&', ('res_model', '=', 'comunication.plan.line'), ('res_id', '=', each.id)])
            each.attachs_count = nbr_attach or 0
            each.has_attachments = bool(nbr_attach)

    has_attachments = fields.Boolean(
        'Tiene documentos', compute='_compute_has_attachments', store=False)

    attachs_count = fields.Integer(
        string=u'# de adjuntos',
        compute='_compute_has_attachments',
        store=False,
    )

    @api.onchange('action_id')
    def _onchange_action_id(self):
        for each in self:
            each.date_release = each.action_id.date_deadline if each.action_id else None

    def action_see_attachments(self):
        domain = [
            '&', ('res_model', '=', 'comunication.plan.line'), ('res_id', '=', self.id), ]
        attachment_view = self.env.ref(
            'mgmtsystem_comunication.view_document_file_kanban_line_document')
        return {
            'name': _('Adjuntos'),
            'domain': domain,
            'res_model': 'comunication.plan.line.document',
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
            'context': "{'default_res_model': '%s','default_res_id': %d}" % ('comunication.plan.line', self.id)
        }

    def action_create_record(self):
        name = 'Acta de reunión de %s' % (self.resume)
        record = self.env['record.meeting'].create({
            'name': name,
            'line_id': self.id,
        })
        record.partner_ids = [(6, 0, self.partner_ids.ids)]
        record.employee_ids = [(6, 0, self.employee_ids.ids)]
        value = {
            'name': _('Actas de reunión'),
            'view_mode': 'form',
            'res_model': 'record.meeting',
            'res_id': record.id,
            'type': 'ir.actions.act_window',
        }
        return value

    def get_send_to_emails(self):
        work_emails = ','.join(
            [x.work_email for x in self.employee_ids if x.work_email])
        return work_emails


class LineDocument(models.Model):
    _name = 'comunication.plan.line.document'
    _description = "Documentos en lineas del Plan de comunicación"
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
