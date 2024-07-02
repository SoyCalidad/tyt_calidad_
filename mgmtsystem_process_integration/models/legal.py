from odoo import api, fields, models
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class LegalPlan(models.Model):
    _name = 'legal.plan'
    _inherit = ['legal.plan', 'model.origin.abstract']

    target_ids = fields.Many2many('mgmtsystem.target', string='Objetivos')
    targets_count = fields.Integer(
        compute='_compute_indicators_count', string='Objetivos')

    nonconformity_ids = fields.Many2many(
        'mgmtsystem.nonconformity', string='No conformidades')
    nonconformities_count = fields.Integer(
        compute='_compute_nonconformities_count', string='No conformidades')

    action_ids = fields.Many2many('mgmtsystem.action', string='Acciones')
    actions_count = fields.Integer(
        compute='_compute_actions_count', string='Acciones')

    @api.depends('action_ids')
    def _compute_actions_count(self):
        for each in self:
            each.actions_count = len(each.action_ids)

    # Ayuda a ingresar el modelo de origen, no se guarda en la base de datos
    def compute_model_id(self):
        for record in self:
            record.model_id = self.env['ir.model'].search(
                [('model', '=', self._name)], limit=1)

    model_id = fields.Many2one(
        string='Modelo',
        comodel_name='ir.model',
        ondelete='cascade',
        compute=compute_model_id,
        store=False,
    )

    def write(self, values):
        """if not self.env.user.has_group('mgmtsystem_legal.group_legal_all'):
            if self.env.user.id !='1' :
                if self.elaborate_ids != self.env.user:
                    raise UserError('Error: Sin permisos de Edición!')"""
        result = super(LegalPlan, self).write(values)
        self.verify_origin()
        return result

    # def exist_origin(self, type, type_id):
    #     sql = ""
    #     if type == 'action':
    #         sql = "select count(*) from mgmtsystem_action m join mgmtsystem_action_origin as o on o.action_id = m.id "
    #     if type == 'nc':
    #         sql = "select count(*) from mgmtsystem_nonconformity m join mgmtsystem_nonconformity_origin as o on o.nc_id = m.id "
    #     if type == 'target':
    #         sql = "select count(*) from mgmtsystem_target m join mgmtsystem_target_origin as o on o.target_id = m.id "
    #     sql = ("%s where m.id = %s and o.origin_model_id = %s and o.origin_int_id = %s") % (
    #         sql, type_id, self.model_id.id, self.id)
    #     self.env.cr.execute(sql)
    #     res_all = self.env.cr.fetchall()
    #     if res_all[0][0] == 0:
    #         return False
    #     return True

    @api.onchange('history_ids.line_ids')
    def _onchange_history_ids(self):
        ids_action = self.action_ids.ids
        for history in self.history_ids:
            for line in history.line_ids:
                if line.proposal_action_id:
                    ids_action.append(line.proposal_action_id.id)
        self.action_ids = ids_action

    # Verifica que los origenes tengan de origen el presente
    # def verify_origin(self):
    #     if self.action_ids:
    #         for action in self.action_ids:
    #             if not self.exist_origin('action', action.id):
    #                 action.write({
    #                     'origin_model_id': self.model_id.id,
    #                     'origin_int_id': self.id})
    #     if self.nonconformity_ids:
    #         for nonconformity in self.nonconformity_ids:
    #             if not self.exist_origin('nc', nonconformity.id):
    #                 nonconformity.write({
    #                     'origin_model_id': self.model_id.id,
    #                     'origin_int_id': self.id})
    #     if self.target_ids:
    #         for target in self.target_ids:
    #             if not self.exist_origin('target', target.id):
    #                 target.write({
    #                     'origin_model_id': self.model_id.id,
    #                     'origin_int_id': self.id})

    def action_legal_plan_views(self):

        action_rec = self.env.ref(
            'mgmtsystem_process_integration.show_ac_legal_plan_action').read()[0]
        ids = []
        for each in self:
            for lin in each.line_ids:
                ids.append(lin.realize.id)

        domain = [('id', 'in', ids)]
        print(domain)
        action_rec['domain'] = domain
        return action_rec

    @api.depends('nonconformity_ids')
    def _compute_nonconformities_count(self):
        for each in self:
            if each.nonconformity_ids:
                each.nonconformities_count = len(each.nonconformity_ids)
            else:
                each.nonconformities_count = 0

    @api.depends('target_ids')
    def _compute_indicators_count(self):
        for each in self:
            if each.target_ids:
                each.targets_count = len(self.target_ids)
            else:
                each.targets_count = 0


class Legal(models.Model):
    _name = 'legal.legal'
    _inherit = ['legal.legal', 'model.origin.abstract']

    target_ids = fields.Many2many('mgmtsystem.target', string='Objetivos')
    targets_count = fields.Integer(
        compute='_compute_indicators_count', string='Objetivos')

    nonconformity_ids = fields.Many2many(
        'mgmtsystem.nonconformity', string='No conformidades')
    nonconformities_count = fields.Integer(
        compute='_compute_nonconformities_count', string='No conformidades')

    action_ids = fields.Many2many('mgmtsystem.action', string='Acciones')
    actions_count = fields.Integer(
        compute='_compute_actions_count', string='Acciones')

    comunication_ids = fields.Many2many('comunication.plan.line', string='Planes de comunicación')
    comunications_count = fields.Integer(compute='_compute_comunications_count', string='Planes de comunicación')
    
    @api.depends('comunication_ids')
    def _compute_comunications_count(self):
        for each in self:
            each.comunications_count = len(each.comunication_ids)


    @api.depends('action_ids')
    def _compute_actions_count(self):
        for each in self:
            if each.action_ids:
                each.actions_count = len(self.action_ids)
            else:
                each.actions_count = 0

    # Ayuda a ingresar el modelo de origen, no se guarda en la base de datos

    def compute_model_id(self):
        for record in self:
            record.model_id = self.env['ir.model'].search(
                [('model', '=', self._name)], limit=1)

    model_id = fields.Many2one(
        string='Modelo',
        comodel_name='ir.model',
        ondelete='cascade',
        compute=compute_model_id,
        store=False,
    )

    def write(self, values):
        """if not self.env.user.has_group('mgmtsystem_legal.group_legal_all'):
            if self.env.user.id !='1' :
                if self.partner_id != self.env.user:
                    raise UserError('Error: Sin permisos de Edición!')"""
        result = super(Legal, self).write(values)
        self.verify_origin()
        return result

    @api.depends('nonconformity_ids')
    def _compute_nonconformities_count(self):
        for each in self:
            if each.nonconformity_ids:
                each.nonconformities_count = len(each.nonconformity_ids)
            else:
                each.nonconformities_count = 0

    @api.depends('target_ids')
    def _compute_indicators_count(self):
        for each in self:
            if each.target_ids:
                each.targets_count = len(self.target_ids)
            else:
                each.targets_count = 0


class NCLegal(models.Model):
    _inherit = 'mgmtsystem.nonconformity'

    legal_ids = fields.Many2many('legal.legal', string='Requisitos Legales')
    legals_count = fields.Integer(
        compute='_compute_legals_count', string='Requisitos Legales')

    legal_plan_ids = fields.Many2many('legal.plan', string='Planes legales')
    legal_plans_count = fields.Integer(
        compute='_compute_legal_plans_count', string='Planes Legales')

    @api.depends('legal_plan_ids')
    def _compute_legal_plans_count(self):
        for each in self:
            if each.legal_plan_ids:
                each.legal_plans_count = len(each.legal_plan_ids)
            else:
                each.legal_plans_count = 0

    @api.depends('legal_ids')
    def _compute_legals_count(self):
        for each in self:
            if each.legal_ids:
                each.legals_count = len(each.legal_ids)
            else:
                each.legals_count = 0


class TargetLegal(models.Model):
    _inherit = 'mgmtsystem.target'

    legal_ids = fields.Many2many('legal.legal', string='Requisitos Legales')
    legals_count = fields.Integer(
        compute='_compute_legals_count', string='Requisitos Legales')

    legal_plan_ids = fields.Many2many('legal.plan', string='Planes legales')
    legal_plans_count = fields.Integer(
        compute='_compute_legal_plans_count', string='Planes Legales')

    @api.depends('legal_plan_ids')
    def _compute_legal_plans_count(self):
        for each in self:
            if each.legal_plan_ids:
                each.legal_plans_count = len(each.legal_plan_ids)
            else:
                each.legal_plans_count = 0

    @api.depends('legal_ids')
    def _compute_legals_count(self):
        for each in self:
            if each.legal_ids:
                each.legals_count = len(each.legal_ids)
            else:
                each.legals_count = 0


class ActionLegal(models.Model):
    _inherit = 'mgmtsystem.action'

    legal_ids = fields.Many2many('legal.legal', string='Requisitos Legales')
    legals_count = fields.Integer(
        compute='_compute_legals_count', string='Requisitos Legales')

    legal_plan_ids = fields.Many2many('legal.plan', string='Planes legales')
    legal_plans_count = fields.Integer(
        compute='_compute_legal_plans_count', string='Planes Legales')

    @api.depends('legal_plan_ids')
    def _compute_legal_plans_count(self):
        for each in self:
            if each.legal_plan_ids:
                each.legal_plans_count = len(each.legal_plan_ids)
            else:
                each.legal_plans_count = 0

    @api.depends('legal_ids')
    def _compute_legals_count(self):
        for each in self:
            if each.legal_ids:
                each.legals_count = len(each.legal_ids)
            else:
                each.legals_count = 0


class ComunicationPlan(models.Model):
    _inherit = 'comunication.plan.line'

    legal_ids = fields.Many2many('legal.legal', string='Requisitos legales')
    legals_count = fields.Integer(compute='_compute_legals_count', string='Requisitos legales')
    
    @api.depends('legal_ids')
    def _compute_legals_count(self):
        for each in self:
            each.legals_count = len(each.legal_ids)
