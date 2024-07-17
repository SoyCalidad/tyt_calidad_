from odoo import models, api, fields, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError


class NcReport(models.TransientModel):
    _name = "wizard.nc.report"
    _inherit = 'mgmtsystem.code'
    _description = "Reporte de No conformidades y Acciones"

    date_init = fields.Date(
        string='Fecha inicio',
        default=fields.Date.context_today,
        required=True,
    )

    date_fin = fields.Date(
        string='Fecha finalización',
        default=fields.Date.context_today,
        required=True,
    )

    validation_date = fields.Date('Fecha de validación')

    def export_nc_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'wizard.nc.report'
        datas['form'] = self.read()[0]
        datas['code'] = self.code
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        return self.env.ref('mgmtsystem_nonconformity.report_nc_xlsx').report_action(self, data=datas)

    def export_nc_ac_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'wizard.nc.report'
        datas['form'] = self.read()[0]
        datas['code'] = self.code
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        return self.env.ref('mgmtsystem_nonconformity.report_nc_ac_xlsx').report_action(self, data=datas)


class NonConformityType(models.Model):
    _name = 'mgmtsystem.nonconformity.type'
    _description = 'Tipo de No conformidad'

    name = fields.Char(string='Nombre')
    description = fields.Text(string='Descripción')


class MgmtsystemNonconformityCauseWhy(models.Model):
    _inherit = 'mgmtsystem.nonconformity.cause_why'

    # One2many references

    nc_cause_id = fields.Many2one(
        'mgmtsystem.nonconformity', string='Causa (No conformidad)')
    nc_why_id = fields.Many2one(
        'mgmtsystem.nonconformity', string='¿Por qué? (No conformidad)')


class MgmtsystemNonconformity(models.Model):
    _name = "mgmtsystem.nonconformity"
    _description = "No conformidad"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'mgmtsystem.code']
    _order = "create_date desc"

    name = fields.Char('Nombre',
                       required=True
                       )
    ref = fields.Char(
        'Referencia',
    )
    system_id = fields.Many2one(
        'mgmtsystem.context.system', string='Identificador', default=lambda self: self.env.ref('hola_calidad.policy_system_1'))
    # Compute data
    number_of_nonconformities = fields.Integer(
        '# de No conformidades', readonly=True, default=1)
    days_since_updated = fields.Integer(
        readonly=True,
        compute='_compute_days_since_updated',
        store=True)
    number_of_days_to_close = fields.Integer(
        '# de dias al cierre',
        compute='_compute_number_of_days_to_close',
        store=True,
        readonly=True)
    closing_date = fields.Datetime('Fecha de cierre', readonly=True)

    partner_id = fields.Many2one('res.partner', 'Auditor')
    reference = fields.Char('Referencia de')
    user_id = fields.Many2one(
        'res.users',
        'Autor',
        default=lambda self: self.env.user,
        tracking=True
    )
    description = fields.Text('Descripción', required=True)
    image = fields.Image("Image", max_width=1024, max_height=1024)

    iso_9001_requeriments_ids = fields.Many2many(
        'iso_9001.requirement', string='Requisitos de la norma (ISO 9001)')
    nc_output = fields.Boolean('¿Es una salida no conforme?')
    source = fields.Char('Fuente')

    state = fields.Selection(
        [('draft', 'Borrador'),
         ('pending', 'Plan de acción'),
         ('open', 'En proceso'),
         ('done', 'Cerrado'),
         ('cancel', 'Cancelado')],
        default='draft',
        string='Estado',
        group_expand='_group_expand_states'
    )

    def _group_expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    kanban_state = fields.Selection(
        [('normal', 'In Progress'),
         ('done', 'Ready for next stage'),
         ('blocked', 'Blocked')],
        'Estado del kanban',
        default='normal',
        tracking=True
        required=True, copy=False)

    def send_acction(self):
        self.write({'state': 'pending'})

    def send_process(self):
        self.write({'state': 'open'})

    def send_cerrado(self):
        self.write({'state': 'done'})

    def send_cancel(self):
        self.write({'state': 'cancel'})

    # 2. Root Cause Analysis
    @api.model
    def _get_causes(self):
        return self.env['mgmtsystem.nonconformity.cause'].search([('is_base', '=', True)]).ids

    investigation_method = fields.Selection([
        ('cause', 'Análisis causa-efecto'),
        ('why', '5 ¿Por qué?'),
    ], string='Metodo de investigación')

    cause_ids = fields.One2many(
        'mgmtsystem.nonconformity.cause_why', 'nc_cause_id', string='Causas')

    why_ids = fields.One2many(
        'mgmtsystem.nonconformity.cause_why', 'nc_why_id', string='¿Por qué?')

    root_cause = fields.Char(string='Causa raiz')

    severity_id = fields.Many2one(
        'mgmtsystem.nonconformity.severity',
        'Severidad',
    )
    analysis = fields.Text('Analisis')

    # 3. Action Plan
    action_ids = fields.Many2many(
        'mgmtsystem.action',
        'mgmtsystem_nonconformity_action_rel',
        'nonconformity_id',
        'action_id',
        'Acciones',
    )
    o_action_ids = fields.Many2many(
        'mgmtsystem.action',
        'mgmtsystem_nonconformity_action_rel',
        'nonconformity_id',
        'action_id',
        'Acción de seguimiento',
    )

    action_comments = fields.Text(
        'Comentarios del plan',
    )

    effect = fields.Text('Efecto')
    conclusions = fields.Text(string='Conclusiones')

    # 4. Effectiveness Evaluation
    evaluation_comments = fields.Text(
        'Comentarios de la evaluación',
    )

    report_id = fields.Many2one(
        string='Auditoría origen',
        comodel_name='audit.report',
        ondelete='cascade',
    )

    type_id = fields.Many2one('mgmtsystem.nonconformity.type', string='Tipo')

    type = fields.Selection(
        string='Tipo',
        selection=[
            ('na', 'NA'),
            ('mayor', 'Mayor'),
            ('menor', 'Menor'),
        ],
        default='na',
    )

    employee_id = fields.Many2one(
        string='Responsable',
        comodel_name='hr.employee',
        ondelete='cascade',
    )
    process_id = fields.Many2one(
        string='Proceso afectado',
        comodel_name='mgmt.categ',
        ondelete='cascade',
    )
    auditor_id = fields.Reference(selection=[('res.partner', 'Auditor externo'), (
        'hr.employee', 'Auditor interno'), ], string="Auditor")
    team_id = fields.Many2one(
        string='Equipo',
        comodel_name='maintenance.team',
        ondelete='cascade',
    )
    audit_team_id = fields.Many2one(
        string='Equipo de auditoría',
        comodel_name='audit.team',
        ondelete='cascade',
    )
    # Fechas

    nc_create_date = fields.Datetime(
        'Fecha de creación', default=lambda self: self.create_date)
    date_found = fields.Date(
        string='Fecha de hallazgo',
        default=fields.Date.context_today,
    )
    date_limit = fields.Date(
        string='Fecha límite',
        default=fields.Date.context_today,
    )

    action_count = fields.Integer(
        string='Acciones', compute='_compute_action_ids')

    @api.depends('action_ids')
    def _compute_action_ids(self):
        for each in self:
            each.action_count = len(each.action_ids)

    # Multi-company
    company_id = fields.Many2one(
        'res.company',
        'Compañia',
        default=lambda self: self.env.user.company_id.id)

    def _get_all_actions(self):
        self.ensure_one()
        return (
            self.action_ids)

    @api.constrains('state')
    def _check_open_with_action_comments(self):
        for nc in self:
            if nc.state == 'done':
                for action in nc.action_ids:
                    if action.state not in ['done', 'cancel']:
                        # if action:
                        raise models.ValidationError(
                            _("Se requiere validar el plan de acción para poner una No conformidad en cerrado"))

    @api.model
    def _elapsed_days(self, dt1_text, dt2_text):
        res = 0
        if dt1_text and dt2_text:
            dt1 = fields.Datetime.from_string(dt1_text)
            dt2 = fields.Datetime.from_string(dt2_text)
            res = (dt2 - dt1).days
        return res

    @api.depends('write_date')
    def _compute_days_since_updated(self):
        for nc in self:
            nc.days_since_updated = self._elapsed_days(
                nc.create_date,
                nc.write_date)

    @api.constrains('date_limit')
    def _check_date_limit(self):
        for record in self:
            if record.date_limit and record.date_found and (record.date_limit < record.date_found):
                raise ValidationError(
                    _('La fecha de límite no puede ser menor a la fecha de hallazgo'))

    @api.model
    def default_get(self, fields_list):
        res = super(MgmtsystemNonconformity, self).default_get(fields_list)
        vals = []
        for cause in self.env['mgmtsystem.nonconformity.cause'].search([('is_base', '=', True)]):
            vals.append((0, 0, {'cause_id': cause.id, 'description': '', 'attachment_ids': [
                        (6, 0, [])], 'subcause_ids': [(6, 0, [])]}))
        res.update({'cause_ids': vals, })
        return res
