# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class PlanInfrastructureLine(models.Model):
    _name = 'mgmtsystem.infrastructure.line'

    plani_id = fields.Many2one(
        string=u'Programa de infraestructura',
        comodel_name='mgmtsystem.infrastructure',
        ondelete='restrict',
    )
    equipment_id = fields.Many2one(
        string=u'Equipo',
        comodel_name='maintenance.equipment',
        ondelete='restrict',
    )
    name = fields.Char(u'Nombre')
    category_id = fields.Many2one(
        string=u'Categoría',
        comodel_name='maintenance.equipment.category',
    )
    cost = fields.Float(
        string=u'Costo',
        store=True,
    )
    employee_id = fields.Many2one(
        string=u'Responsable',
        comodel_name='hr.employee',
        ondelete='restrict',
    )
    department_id = fields.Many2one(
        string=u'Departamento',
        comodel_name='hr.department',
        ondelete='restrict',
    )
    assign_date = fields.Date(
        string=u'Fecha de adquisición',
        store=True,
    )
    location = fields.Char(
        string=u'Ubicación',
        store=True,
    )
    scrap_date = fields.Date(
        string=u'Fecha de desecho',
        store=True,
    )

    @api.depends('equipment_id')
    def _compute_has_attachments(self):
        for each in self:
            nbr_attach = self.env['infrastructure.line.document'].search_count([
                '&', ('res_model', '=', 'mgmtsystem.infrastructure.line'), ('res_id', '=', each.id)])
            each.has_attachments = bool(nbr_attach)

    has_attachments = fields.Boolean('Tiene documentos', compute='_compute_has_attachments')

    @api.onchange('equipment_id')
    def _onchange_equipment_id(self):
        self.name = self.equipment_id.name
        self.category_id = self.equipment_id.category_id
        self.cost = self.equipment_id.cost
        self.employee_id = self.equipment_id.employee_id
        self.department_id = self.equipment_id.department_id
        self.assign_date = self.equipment_id.assign_date
        self.location = self.equipment_id.location
        self.scrap_date = self.equipment_id.scrap_date

    aproval = fields.Boolean(
        string=u'Aprobada',
    )
    observations = fields.Char(
        string=u'Observaciones',
    )

    def action_see_attachments(self):
        domain = [
            '&', ('res_model', '=', 'mgmtsystem.infrastructure.line'), ('res_id', '=', self.id),]
        attachment_view = self.env.ref('mgmtsystem_infrastructure.view_document_file_kanban_infrastructure_line')
        return {
            'name': _('Adjuntos'),
            'domain': domain,
            'res_model': 'infrastructure.line.document',
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
            'context': "{'default_res_model': '%s','default_res_id': %d}" % ('mgmtsystem.infrastructure.line', self.id)
        }


class PlanInfrastructure(models.Model):
    _name = 'mgmtsystem.infrastructure'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Programa de infraestructura"

    lines_ids = fields.One2many(
        string=u'Lineas',
        comodel_name='mgmtsystem.infrastructure.line',
        inverse_name='plani_id',
        copy=True,
    )

    equipment_ids = fields.Many2many(
        string=u'Bienes',
        comodel_name='maintenance.equipment',
        relation='equipment_plani_rel',
        column1='equipment_id',
        column2='plani_id',
    )

    name = fields.Char(
        string=u'Nombre',
        required=True,
        default="Inventariado"
    )

    numero = fields.Char(
        string = "Numero de secuencia", 
        readonly = True, 
        required = True, 
        copy = False, 
        default = 'Sin definir'
    )

    have_equipment = fields.Boolean(string=u'Pasaron equipamentos')

    def _default_edition(self):
        process = self.env['res.company'].browse(self.env.user.company_id.id).infrastructure_process_id
        if process:
            edition = self.env['process.edition'].search([
                    ('process_id','=',process.id),
                    ('state', '=', 'validate_ok'),
                    ('active', '=', True),
            ], order='create_date desc', limit=1)
            return edition
        else:
            return

    edition_id = fields.Many2one(
        string=u'Procedimiento',
        comodel_name='process.edition',
        domain="[('state', '=', 'validate_ok'),('active', '=', True)]",
        ondelete='cascade',
        default=_default_edition,
    )

    elaborate_ids = fields.Many2many(
        string=u'Elaborado', 
        comodel_name='res.users', 
        relation='plani_user_elaborate', 
        column1='user_id', 
        column2='elaborate_id', 
        default=lambda self: self.env.user
    )
    review_ids = fields.Many2many(
        string=u'Revisado', 
        comodel_name='res.users', 
        relation='plani_user_review', 
        column1='user_id', 
        column2='review_id'
    )
    validate_ids = fields.Many2many(
        string=u'Validado', 
        comodel_name='res.users', 
        relation='plani_user_validate', 
        column1='user_id', 
        column2='validate_id'
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
            ('cancel', 'Obsoleto')
        ],
        default='elaborate',
        copy=False,
    )

    def write(self, values):
        message = ""

        if values.get('numero', 'Sin definir') == 'Sin definir' and values.get('state', False) == 'validate_ok':
            values['numero'] = self.env['ir.sequence'].next_by_code('planinfra.sequence') or 'Sin definir'

        if values.get('state', False):
            state1 = dict(self._fields['state'].selection).get(self.state)
            state2 = dict(self._fields['state'].selection).get(values.get('state'))
            message = message + _("<li>Estado: %s &rarr; %s</li>") % (state1, state2)
        if values.get('date_elaborate', False):
            message = message + _("<li>Fecha de elaboración: %s &rarr; %s</li>") % (self.date_elaborate, values.get('date_elaborate'))
        if values.get('date_review', False):
            message = message + _("<li>Fecha de revisión: %s &rarr; %s</li>") % (self.date_review, values.get('date_review'))
        if values.get('date_validate', False):
            message = message + _("<li>Fecha de validación: %s &rarr; %s</li>") % (self.date_validate, values.get('date_validate'))

        result = super(PlanInfrastructure, self).write(values)

        if message != "":
            self.message_post(body=message)

        return result

    def unlink(self):
        """
        for plan in self:
            if plan.state not in ('elaborate'):
                raise UserError(_('No puedes eliminarlo si se encuentra en proceso. Deberías volverlo obsoleto.'))
        """
        return super(PlanInfrastructure, self).unlink()

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
        for line in self.lines_ids:
            line.write({'aproval': True})

    def show_equipments(self):
        self.have_equipment = False

    def action_send_equipments(self):
        lines = [(5, 0, 0)]
        for equipment in self.equipment_ids:
            data = {
                'plani_id': self.id,
                'equipment_id': equipment.id,
                'name' : equipment.name,
                'category_id' : equipment.category_id,
                'cost' : equipment.cost,
                'employee_id' : equipment.employee_id,
                'department_id' : equipment.department_id,
                'assign_date' : equipment.assign_date,
                'location' : equipment.location,
                'scrap_date' : equipment.scrap_date,
            }
            lines.append((0, 0, data))
        self.lines_ids = lines
        self.have_equipment = True

    def send_elaborate(self):
        if not self.elaborate_ids:
            raise UserError('Ingrese los usuarios de Elaborado')
        self.write({'state': 'elaborate'})
        if self.elaborate_ids:
            pass

    def send_review(self):
        if not self.review_ids:
            raise UserError('Ingrese los usuarios de Revisado')
        self.write({
            'state': 'review',
            'date_elaborate': fields.Date.context_today(self),
            'date_review': fields.Date.context_today(self),
            })
        if self.review_ids:
            pass

    def send_validate(self):
        if not self.validate_ids:
            raise UserError('Ingrese los usuarios de Validado')
        for line in self.lines_ids:
            if not line.aproval:
                raise UserError(_('Todas las lineas deben estar revisadas'))
        self.write({
            'state': 'validate',
            'date_review': fields.Date.context_today(self),
            'date_validate': fields.Date.context_today(self),
            })
        for line in self.lines_ids:
            line.write({'aproval': False})
        if self.validate_ids:
            pass

    def send_validate_ok(self):
        for line in self.lines_ids:
            if not line.aproval:
                raise UserError(_('Todas las lineas deben que estar validadas'))
            line.write({'state': 'validate_ok'})
        for equipment in self.lines_ids:
            data = {
                'name' : equipment.name,
                'category_id' : equipment.category_id.id,
                'cost' : equipment.cost,
                'employee_id' : equipment.employee_id.id or False,
                'department_id' : equipment.department_id.id or False,
                'assign_date' : equipment.assign_date,
                'location' : equipment.location,
                'scrap_date' : equipment.scrap_date,
            }
            equipment.equipment_id.write(data)
        self.write({
            'state': 'validate_ok',
            'date_validate': fields.Date.context_today(self),
            })

    def send_cancel(self):
        for line in self.lines_ids:
            line.write({'state': 'cancel'})
        self.write({'state': 'cancel'})


class InfrastructureLineDocument(models.Model):
    _name = 'infrastructure.line.document'
    _description = "Training Document"
    _inherits = {
        'ir.attachment': 'ir_attachment_id',
    }
    _order = "priority desc, id desc"

    ir_attachment_id = fields.Many2one('ir.attachment', string='Related attachment', required=True, ondelete='cascade')
    active = fields.Boolean('Active', default=True)
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority", help='Gives the sequence')


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    state = fields.Selection(
        string=u'Estado',
        selection=[
            ('1new', 'Nueva solicitud'), 
            ('2approved', 'Aprobada'),
            ('3in_process', 'En proceso'),
            ('4repaired', 'Mantenimiento realizado'),
            ('5scrap', 'Desecho'),
        ],
        default='1new',
    )
    responsable_id = fields.Many2one(
        string=u'Encargado de validación',
        comodel_name='res.users',
        ondelete='cascade',
    )

    def send_new(self):
        self.state = '1new'

    def send_approved(self):
        self.state = '2approved'

    def send_in_process(self):
        self.state = '3in_process'

    def send_repaired(self):
        self.state = '4repaired'

    def send_scrap(self):
        self.state = '5scrap'

    def action_notify_employee(self):
        for each in self:
            if not each.responsable_id:
                raise UserError(_('Seleccione un encargado para validar'))
            self.env.cr.execute("""SELECT id FROM ir_model 
                            WHERE model = %s""", (str(each._name),))
            info = self.env.cr.dictfetchall()
            if info:
                model_id = info[0]['id']
                self.env['mail.activity'].create({
                    'res_id': each.ids[0],
                    'res_model_id': model_id,
                    'res_model': each._name,
                    'summary': 'Por hacer',
                    'note': 'Mantenimiento por aprobar',
                    'date_deadline': each.request_date,
                    'user_id': each.responsable_id.id,
                })