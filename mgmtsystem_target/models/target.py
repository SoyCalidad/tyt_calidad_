"""Introduce el modelo Goal que maqueta los Objetivo de calidad de la organización
"""

from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.exceptions import (AccessError, RedirectWarning, UserError,
                             ValidationError, Warning)
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class TargetResources(models.Model):
    _name = 'mgmtsystem.target.resources'
    _description = 'Recursos de objetivos'

    name = fields.Char(string='Nombre')


class MgmtsystemTargetCategory(models.Model):
    _name = 'mgmtsystem.target.category'
    _description = 'Categoría de objetivo'

    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(string='Color Index')
    target_ids = fields.Many2many(
        'mgmtsystem.target', 'target__category__rel', 'category_id', 'tar_id',  string='Objetivos')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "¡Ya existe una categoría con ese nombre!"),
    ]


class Target(models.Model):
    _name = 'mgmtsystem.target'
    _inherit = ['mgmtsystem.validation.mail', 'mgmtsystem.code']
    _description = 'Objetivo'

    do_stage = fields.Boolean(string='Etapa de acción', default=False)
    do_state = fields.Selection([
        ('plan', 'Planificación'),
        ('active', 'Activo'),
        ('inactive', 'Inactivo'),
    ], string='Etapas', default='plan')
    state = fields.Selection(selection_add=[('active', 'En seguimiento'),
                                            ('inactive', 'Inactivo'),
                                            ('closed', 'Finalizado')])
    process_id = fields.Many2one('mgmt.process', domain=[
                                 ('active', '=', True)], string='Procedimiento')
    system_id = fields.Many2one(
        'mgmtsystem.context.system', string='Identificador', default=lambda self: self.env.ref('hola_calidad.policy_system_1'))
    name = fields.Text(string='Nombre del objetivo', required=True)
    source = fields.Selection([
        ('foda', 'FODA'),
        ('self', 'Propia')
    ], string='Fuente', default='self')

    department_id = fields.Many2one(
        'hr.department', string='Departamento principal')
    department_ids = fields.Many2many('hr.department', string='Departamentos')

    category_ids = fields.Many2many(
        'mgmtsystem.target.category', 'target__category__rel', 'tar_id', 'category_id', string='Categorías')

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Responsable',
        default=lambda self: self.env.user)

    description = fields.Text(string='Descripción')
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True, default=lambda self: self.env.user.company_id)
    process_ids = fields.Many2many(
        comodel_name='mgmt.process', relation='process_target_rel', string='Procesos secundarios', domain=[('active', '=', True)])
    process_ids_2 = fields.Many2many(
        comodel_name='mgmt.categ', relation='process_target_rel_2', string='Procesos secundarios', domain=[('active', '=', True)])
    process_count = fields.Integer(
        compute='_compute_process_count', string='Procesos')
    indicator_ids = fields.One2many(
        'mgmtsystem.indicator', 'target_id', string='Indicadores', copy=True)
    indicator_count = fields.Integer(
        compute='_compute_indicator_count', string='# de indicadores')
    goal_progress = fields.Float(
        compute='_compute_goal_progress', string='Progreso')
    action_ids = fields.Many2many(comodel_name='mgmtsystem.action',
                                  relation='action_target_rel',
                                  column1='action_id',
                                  column2='target_id',
                                  string='Acciones')
    actions_count = fields.Integer(
        compute='_compute_actions_count', string='Acciones')

    requirements = fields.Text(string='Requisitos')

    risk_ids = fields.Many2many('matrix.block.line', relation='target_risk_rel',
                                string='Riesgos', domain=[('type', '=', 'risk')])
    risks_count = fields.Integer(
        compute='_compute_risks_count', string='Riesgos')

    opp_ids = fields.Many2many('matrix.block.line', relation='target_op_rel',
                               string='Oportunidades', domain=[('type', '=', 'opportunity')])
    opps_count = fields.Integer(
        compute='_compute_opps_count', string='Oportunidades')

    @api.depends('risk_ids')
    def _compute_risks_count(self):
        for each in self:
            each.risks_count = 0
            if each.risk_ids:
                each.risks_count = len(each.risk_ids)

    @api.depends('opp_ids')
    def _compute_opps_count(self):
        for each in self:
            each.opps_count = 0
            if each.opp_ids:
                each.opps_count = len(each.opp_ids)

    parent_edition = fields.Many2one(
        comodel_name='mgmtsystem.target', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='mgmtsystem.target', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    def _copy_edition(self):
        new_edition = self.copy({
            'version': self.version,
            'state': 'cancel',
            'deactivate_date': fields.Date.today(),
            'parent_edition': self.id,
            'elaboration_step': [(6, 0, self.elaboration_step.ids)],
            'review_step': [(6, 0, self.review_step.ids)],
            'validation_step': [(6, 0, self.validation_step.ids)],
        })
        return new_edition

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_target.target_cancel_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result

    source_model = fields.Many2one('ir.model', string='Modelo')

    @api.depends('indicator_ids')
    def _compute_goal_progress(self):
        for each in self:
            if not each.indicator_ids:
                each.goal_progress = 0
            progress = 0
            for indicator in each.indicator_ids:
                progress = progress + indicator.c_goal_progress
            each.goal_progress = float(
                progress/len(each.indicator_ids)) if len(each.indicator_ids) > 0 else 0

    @api.depends('process_ids')
    def _compute_process_count(self):
        for each in self:
            each.process_count = len(each.process_ids)

    def proceed_to_do_stage(self):
        for line in self.indicator_ids:
            line.do_stage()
        self.state = 'active'
        return self.open_indicator_view()

    def open_indicator_view(self):
        ids_ = [x.id for x in self.indicator_ids]
        domain = [('id', 'in', ids_)]
        action_rec = self.env.ref(
            'mgmtsystem_target.indicator_action_2').read()[0]
        action_rec['domain'] = domain
        return action_rec

    def send_finish(self):
        self.write({'state': 'closed'})

    def current_indicator_progress(self):
        res = []
        for each in self.indicator_ids:
            res.append(each.goal_id.current_goal_progress())

    @api.depends('action_ids')
    def _compute_actions_count(self):
        for each in self:
            total = 0
            if each.action_ids:
                total = len(each.action_ids)
            each.actions_count = total

    def action_target_views(self):
        action_rec = self.env.ref(
            'mgmtsystem_target.show_ac_target_action').read()[0]
        ids = self.action_ids.ids
        domain = [('id', 'in', ids)]
        action_rec['domain'] = domain
        return action_rec

    def action_risk_views(self):
        action_rec = self.env.ref(
            'mgmtsystem_target.show_risk_target_action').read()[0]
        ids = []
        for each in self:
            for lin in each.risk_ids:
                ids.append(lin.id)
        domain = [('id', 'in', ids), ('type', '=', 'risk')]
        action_rec['domain'] = domain
        return action_rec

    def action_opp_views(self):
        action_rec = self.env.ref(
            'mgmtsystem_target.show_risk_target_action').read()[0]
        ids = []
        for each in self:
            for lin in each.opp_ids:
                ids.append(lin.id)
        domain = [('id', 'in', ids), ('type', '=', 'opportunity')]
        action_rec['domain'] = domain
        return action_rec

    @api.depends('indicator_ids')
    def _compute_indicator_count(self):
        for each in self:
            each.indicator_count = len(each.indicator_ids)

    def action_indicator_action(self):
        action_rec = self.env.ref(
            'mgmtsystem_target.indicator_action_2').read()[0]
        ctx = dict(self.env.context)
        action_rec['views'] = [
            (self.env.ref('mgmtsystem_target.indicator_view_graph').id, 'graph')]
        ctx.update({'search_default_target_id': self.ids[0]})
        action_rec['context'] = ctx
        return action_rec

    def migrate_department_to_many2many(self):
        for each in self:
            each.department_ids = [(6, 0, each.department_id.ids)]

    # @api.onchange('indicator_ids')
    # def _onchange_indicator_ids(self):
    #     for each in self.indicator_ids:
    #         if each.action_id:
    #             each.origin = self.source_model.id


class Goal(models.Model):
    _name = 'mgmtsystem.goal'
    _description = 'Meta'

    name = fields.Char(string='Nombre')
    type = fields.Selection([
        ('num', 'Numérico'),
        ('per', 'Porcentaje')
    ], string='Tipo de medición')
    value = fields.Float(string='Valor estimado', digits=(16, 2))

    user_id = fields.Many2one(
        'res.users',
        string='Responsable',
        default=lambda self: self.env.user)

    def write(self, values):
        return super().write(values)


class Indicator(models.Model):
    _name = 'mgmtsystem.indicator'
    _inherit = ['mail.thread', 'mail.activity.mixin',
                'iso_base.email_basic', 'mgmtsystem.code']
    _description = 'Indicador'

    user_id = fields.Many2one(
        'res.users',
        string='Responsable',
        default=lambda self: self.env.user)

    name = fields.Char(string='Nombre')
    name_objetivo = fields.Many2one(
        'mgmtsystem.target', string='Nombre del objetivo')
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True, default=lambda self: self.env.user.company_id)
    do_state = fields.Selection([
        ('plan', 'Borrador'),
        ('tracked', 'En seguimiento'),
        ('accomplished', 'Logrado'),
        ('accomplished_observation', 'Logrado con observaciones'),
        ('caducated', 'Caducado'),
        ('cancel', 'Cancelado'),
    ], string='Etapas', group_expand='_expand_groups', default='plan', copy=False)

    @api.model
    def _expand_groups(self, states, domain, order):
        return ['plan', 'tracked', 'accomplished', 'caducated', 'cancel']
    target_id = fields.Many2one('mgmtsystem.target', string='Objetivo')
    goal_id = fields.Many2one('mgmtsystem.goal', string='Meta')
    description = fields.Text(string='Descripción')
    action_id = fields.Many2one(
        'mgmtsystem.action', string='Qué se va a hacer')

    estimated_start_date = fields.Date(
        string='Fecha de inicio estimada', default=fields.Date.today,)
    start_date = fields.Date(
        default=fields.Date.context_today, string='Fecha de inicio')
    term_date = fields.Date(
        default=fields.Date.context_today, string='Fecha de Finalización')
    measurement_frequency = fields.Many2one(
        'mgmtsystem.target.frequency', string='Frecuencia de Medición', domain=[('type', '=', 'freq')],)
    history_ids = fields.One2many(
        'mgmtsystem.indicator.history', 'indicator_id', string='Indicador')
    goal_value = fields.Float(
        compute='_compute_current_goal_progress', string='Valor de la meta', store=True)
    c_goal_progress = fields.Float(
        compute='_compute_c_goal_progress', string='Progreso actual')
    last_medition = fields.Many2one(
        'mgmtsystem.indicator.history', compute='_compute_current_goal_progress', string='Última medición')
    nonconformity_ids = fields.Many2many(
        'mgmtsystem.nonconformity', string='No conformidades', relation='nonconformity_indicator')

    resources = fields.Text(string='Recursos')

    formula = fields.Char(string='Fórmula')

    categ_id = fields.Many2one(
        related='target_id.process_id', string='Proceso')
    category_ids = fields.Many2many(
        related='target_id.category_ids', string='Categorías')

    def open_form_view(self):
        view_id = self.env.ref('mgmtsystem_target.indicator_view_form').id
        context = self._context.copy()
        return {
            'name': 'Periodos',
            'view_type': 'form',
            'view_mode': 'tree',
            'views': [(view_id, 'form')],
            'res_model': 'mgmtsystem.indicator',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'target': 'new',
            'context': context,
        }

    @api.depends('action_ids')
    def _compute_actions_count(self):
        self.action_count = len(self.action_ids)

    def do_stage(self):
        self.do_state = 'plan'

    def do_tracked(self):
        if not self.history_ids:
            raise ValidationError('Cree un cronograma primero')
        self.do_state = 'tracked'

    def do_accomplished(self):
        self.do_state = 'accomplished'

    def do_accomplished_observation(self):
        self.do_state = 'accomplished_observation'

    def do_cancel(self):
        self.do_state = 'cancel'

    def do_caducated(self):
        self.do_state = 'caducated'

    @api.onchange('term_date')
    def _onchange_term_date(self):
        if self.term_date and self.start_date:
            date = self.start_date
            finish_date = self.term_date
            if finish_date < date:
                raise UserError(
                    'La fecha de finalización no puede ser menor a la fecha de inicio')
        if self.term_date and self.start_date and self.measurement_frequency:
            date = self.start_date
            finish_date = self.term_date
            if date + self.measurement_frequency.get() > finish_date:
                raise UserError(
                    'El plazo dado sobrepasa la fecha de finalización'
                )

    def create_history(self):
        if self.do_state not in ('plan', 'open'):
            raise UserError(
                'Solo se puede crear un cronograma en la etapa de planificación o abierto')
        for each in self.history_ids:
            each.unlink()
        if self.start_date and self.term_date and self.measurement_frequency:
            if self.measurement_frequency.years == 0 and self.measurement_frequency.months == 0 and self.measurement_frequency.weeks == 0 and self.measurement_frequency.days == 0:
                raise UserError(
                    'La frecuencia de medición no es válida. Todos los valores son 0')
            history = self.env['mgmtsystem.indicator.history']
            date = self.start_date
            finish_date = self.term_date
            history.create(
                {
                    'indicator_id': self.id,
                    'date': date,
                    'goal_value': self.goal_id.value,
                }
            )
            while date <= finish_date:
                date = date + self.measurement_frequency.get()
                if date.weekday() == 5:
                    date -= timedelta(days=1)
                if date.weekday() == 6:
                    date += timedelta(days=1)

                history.create(
                    {
                        'indicator_id': self.id,
                        'date': date,
                        'goal_value': self.goal_id.value,
                    }
                )
        else:
            raise UserError('Introduzca una fecha de inicio y un plazo')

    @api.depends('history_ids')
    def _compute_current_goal_progress(self):
        for each in self:
            if not each.history_ids:
                each.goal_value = 0
                each.do_state = 'plan'

            else:
                # If all the history records are accomplished, the indicator is accomplished
                each.do_state = 'accomplished' if all(
                    each.history_ids.mapped('accomplished')) else 'tracked'

                # Get the current progress of the indicator, based on the total of accomplished records
                each.goal_value = each.history_ids.filtered(
                    lambda x: x.accomplished)[-1].real_result if each.history_ids.filtered(lambda x: x.accomplished) else 0
                
                

    @api.depends('history_ids', 'do_state')
    def _compute_c_goal_progress(self):
        # Get the quantiy of records in history_ids with accomplished field as True as percentage of the total
        for each in self:
            if not each.history_ids:
                each.c_goal_progress = 0
            else:
                each.c_goal_progress = len(each.history_ids.filtered(
                    lambda x: x.accomplished)) / len(each.history_ids) * 100
            if each.c_goal_progress == 100:
                each.do_state = 'accomplished'

    def mail_reminder(self):
        now = datetime.now() + timedelta(days=7)
        date_now = now.date()
        match = self.search([])
        for i in match:
            # Loop through history_ids
            for his in i.history_ids:
                if his.date:
                    exp_date = fields.Date.from_string(his.date)
                    if date_now == exp_date:
                        # Get user ID for indicator
                        user_id = i.user_id or None
                        # If user ID exists, notify users by activity
                        if user_id:
                            notify_content = 'Medición de indicador'
                            i.notify_users_by_activity(user_id, notify_content)


class MeasurementHistory(models.Model):
    _name = 'mgmtsystem.indicator.history'
    _description = 'Historial de medición'

    indicator_id = fields.Many2one('mgmtsystem.indicator', string='Indicador')
    date = fields.Date(string='Fecha')
    goal_value = fields.Float(string='Meta del periodo', digits=(16, 2))
    expected_result = fields.Float(string='Valor planificado', digits=(16, 2))
    real_result = fields.Float(string='Valor medido', digits=(16, 2))
    comments = fields.Text(string='Comentarios')
    accomplished = fields.Boolean(string='Marcar como logrado')


class MeasurementPeriod(models.Model):
    _name = "mgmtsystem.target.frequency"
    _description = "Periodo de tiempo"

    name = fields.Char(string='Nombre',
                       translate=True, required=True)
    active = fields.Boolean(string="Activo", default=True)
    note = fields.Text(string='Descripción', translate=True)
    company_id = fields.Many2one('res.company', string='Compañia',
                                 required=True, default=lambda self: self.env.user.company_id)
    years = fields.Integer(string='Número de Años', required=True, default=0)
    months = fields.Integer(string='Número de Meses', required=True, default=0)
    weeks = fields.Integer(string='Número de Semanas',
                           required=True, default=0)
    days = fields.Integer(string='Número de Días', required=True, default=0)
    type = fields.Selection([
        ('term', 'Periodo'),
        ('freq', 'Frecuencia'),
    ], string='Tipo')

    def get(self):
        "Return the relativedelta"
        return relativedelta(
            years=self.years,
            days=self.days,
            weeks=self.weeks,
            months=self.months,
        )

    @api.constrains('line_ids')
    def _check_lines(self):
        pass

    def compute(self, value, date_ref=False):
        date_ref = date_ref or fields.Date.today()


class Action(models.Model):
    _inherit = 'mgmtsystem.action'

    target_ids = fields.Many2many(
        comodel_name='mgmtsystem.target',
        relation='action_target_rel',
        column1='target_id',
        column2='action_id',
        string='Objetivos')
    targets_count = fields.Integer(
        compute='_compute_targets_count', string='Indicadores')

    @api.depends('target_ids')
    def _compute_targets_count(self):
        for each in self:
            each.targets_count = len(self.target_ids)

    @api.model
    def _default_origin(self):
        self.origin = 1


class Process(models.Model):
    _inherit = 'mgmt.process'

    target_ids = fields.Many2many(
        comodel_name='mgmtsystem.target', relation='process_target_rel', string='Objetivos')
    targets_count = fields.Integer(
        compute='_compute_targets_count', string='Objetivos')

    @api.depends('target_ids')
    def _compute_targets_count(self):
        for each in self:
            if each.target_ids:
                each.targets_count = len(self.target_ids)
            else:
                each.targets_count = 0
