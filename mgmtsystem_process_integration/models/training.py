from odoo import api, fields, models


class TrainingPlan(models.Model):
    _name = 'mgmtsystem.plan'
    _inherit = ['mgmtsystem.plan', 'model.origin.abstract']

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
            total = 0
            total += len(each.action_ids)
            for line in each.training_ids:
                if line.action_ids:
                    total += len(line.action_ids)
            each.actions_count = total

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
        result = super(TrainingPlan, self).write(values)
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
    #     print('-> sql', sql)
    #     self.env.cr.execute(sql)
    #     res_all = self.env.cr.fetchall()
    #     if res_all[0][0] == 0:
    #         return False
    #     return True

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

    @api.depends('nonconformity_ids')
    def _compute_nonconformities_count(self):
        for each in self:
            total = 0
            for line in each.training_ids:
                total += len(line.nonconformity_ids)
            each.nonconformities_count = total

    @api.depends('target_ids')
    def _compute_indicators_count(self):
        for each in self:
            total = 0
            for line in each.training_ids:
                total += len(line.target_ids)
            each.targets_count = total

    def action_training_views(self):
        action_rec = self.env.ref(
            'mgmtsystem_process_integration.show_ac_plan_training_action').read()[0]
        ids = []
        for each in self:
            for lin in each.training_ids:
                ids.extend(lin.action_ids.ids)
            ids.extend(each.action_ids.ids)
        domain = [('id', 'in', ids)]
        action_rec['domain'] = domain
        return action_rec

    def nc_training_views(self):
        action_rec = self.env.ref(
            'mgmtsystem_process_integration.show_nc_plan_training_action').read()[0]
        ids = []
        for each in self:
            for lin in each.training_ids:
                ids.extend(lin.nonconformity_ids.ids)

        domain = [('id', 'in', ids)]
        print(domain)
        action_rec['domain'] = domain
        return action_rec

    def target_training_views(self):
        action_rec = self.env.ref(
            'mgmtsystem_process_integration.show_target_plan_training_action').read()[0]
        ids = []
        for each in self:
            for lin in each.training_ids:
                ids.extend(lin.target_ids.ids)

        domain = [('id', 'in', ids)]
        print(domain)
        action_rec['domain'] = domain
        return action_rec


class Training(models.Model):
    _name = 'mgmtsystem.plan.training'
    _inherit = ['mgmtsystem.plan.training', 'model.origin.abstract']

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
        result = super(Training, self).write(values)
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
    #     print('-> sql', sql)
    #     self.env.cr.execute(sql)
    #     res_all = self.env.cr.fetchall()
    #     if res_all[0][0] == 0:
    #         return False
    #     return True

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


class NCTraining(models.Model):
    _inherit = 'mgmtsystem.nonconformity'

    training_ids = fields.Many2many(
        'mgmtsystem.plan.training', string='Capacitaciones')
    trainings_count = fields.Integer(
        compute='_compute_trainings_count', string='Capacitaciones')

    @api.depends('training_ids')
    def _compute_trainings_count(self):
        for each in self:
            if each.training_ids:
                each.trainings_count = len(each.training_ids)
            else:
                each.trainings_count = 0


class TargetTraining(models.Model):
    _inherit = 'mgmtsystem.target'

    training_ids = fields.Many2many(
        'mgmtsystem.plan.training', string='Capacitaciones')
    trainings_count = fields.Integer(
        compute='_compute_trainings_count', string='Capacitaciones')

    @api.depends('training_ids')
    def _compute_trainings_count(self):
        for each in self:
            if each.training_ids:
                each.trainings_count = len(each.training_ids)
            else:
                each.trainings_count = 0


class ActionTraining(models.Model):
    _inherit = 'mgmtsystem.action'

    training_ids = fields.Many2many(
        'mgmtsystem.plan.training', string='Capacitaciones')
    trainings_count = fields.Integer(
        compute='_compute_trainings_count', string='Capacitaciones')

    @api.depends('training_ids')
    def _compute_trainings_count(self):
        for each in self:
            if each.training_ids:
                each.trainings_count = len(each.training_ids)
            else:
                each.trainings_count = 0
