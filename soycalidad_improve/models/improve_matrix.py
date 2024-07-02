from odoo import api, fields, models


class ImprovePlanMatrix(models.Model):
    _name = 'soycalidad.improve_plan.matrix'
    _inherit = ['mgmtsystem.validation.mail', 'mgmtsystem.code']
    _description = 'Matriz de Planificación de cambios'

    name = fields.Char(string='Nombre')
    improve_plan_ids = fields.Many2many(
        'soycalidad.change_request', string='Planificación de cambios', copy=True)

    target_ids = fields.Many2many('mgmtsystem.target', string='Objetivos',
                                  relation='target_improve_matrix_rel', column1='target_id', column2='improve_id')
    targets_count = fields.Integer(
        compute='_compute_targets_count', string='Objetivos')

    nonconformity_ids = fields.Many2many(
        'mgmtsystem.nonconformity', string='No conformidades', relation='nonconformity_improve_matrix_rel', column1='nonconformity_id', column2='improve_id')
    nonconformities_count = fields.Integer(
        compute='_compute_nonconformities_count', string='No conformidades')

    action_ids = fields.Many2many(
        'mgmtsystem.action', string='Acciones', relation='action_improve_matrix_rel', column1='action_id', column2='improve_id')
    actions_count = fields.Integer(
        compute='_compute_actions_count', string='Acciones')

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
        result = super().write(values)
        self.verify_origin()
        return result

    def exist_origin(self, type, type_id):
        sql = ""
        if type == 'action':
            sql = "select count(*) from mgmtsystem_action m join mgmtsystem_action_origin as o on o.action_id = m.id "
        if type == 'nc':
            sql = "select count(*) from mgmtsystem_nonconformity m join mgmtsystem_nonconformity_origin as o on o.nc_id = m.id "
        if type == 'target':
            sql = "select count(*) from mgmtsystem_target m join mgmtsystem_target_origin as o on o.target_id = m.id "
        sql = ("%s where m.id = %s and o.origin_model_id = %s and o.origin_int_id = %s") % (
            sql, type_id, self.model_id.id, self.id)
        print('-> sql', sql)
        self.env.cr.execute(sql)
        res_all = self.env.cr.fetchall()
        if res_all[0][0] == 0:
            return False
        return True

    # Verifica que los origenes tengan de origen el presente
    def verify_origin(self):
        if self.action_ids:
            for action in self.action_ids:
                if not self.exist_origin('action', action.id):
                    action.write({
                        'origin_model_id': self.model_id.id,
                        'origin_int_id': self.id})
        if self.nonconformity_ids:
            for nonconformity in self.nonconformity_ids:
                if not self.exist_origin('nc', nonconformity.id):
                    nonconformity.write({
                        'origin_model_id': self.model_id.id,
                        'origin_int_id': self.id})
        if self.target_ids:
            for target in self.target_ids:
                if not self.exist_origin('target', target.id):
                    target.write({
                        'origin_model_id': self.model_id.id,
                        'origin_int_id': self.id})

    @api.depends('action_ids')
    def _compute_actions_count(self):
        for each in self:
            if each.action_ids:
                each.actions_count = len(self.action_ids)
            else:
                each.actions_count = 0

    @api.depends('nonconformity_ids')
    def _compute_nonconformities_count(self):
        for each in self:
            if each.nonconformity_ids:
                each.nonconformities_count = len(each.nonconformity_ids)
            else:
                each.nonconformities_count = 0

    @api.depends('target_ids')
    def _compute_targets_count(self):
        for each in self:
            if each.target_ids:
                each.targets_count = len(self.target_ids)
            else:
                each.targets_count = 0

    #Adding to update to Odoo v15
    def action_improve_views(self):
        type_action = self._context.get('type_action', '')
        if type_action == '':
            return
        ids = []
        if type_action == 'target':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.action_maintenance_plan_target').read()[0]
            for each in self:
                for lin in each.maintenance_ids:
                    ids.extend(lin.target_ids.ids)
                ids.extend(each.target_ids.ids)
            domain = [('id', 'in', ids)]
            action_rec['domain'] = domain

        elif type_action == 'nc':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.action_maintenance_plan_nc').read()[0]
            for each in self:
                for lin in each.maintenance_ids:
                    ids.extend(lin.nonconformity_ids.ids)
                ids.extend(each.nonconformity_ids.ids)
            domain = [('id', 'in', ids)]
            action_rec['domain'] = domain

        elif type_action == 'action':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.action_maintenance_plan_action').read()[0]
            for each in self:
                for lin in each.maintenance_ids:
                    ids.extend(lin.action_ids.ids)
                ids.extend(each.action_ids.ids)
            domain = [('id', 'in', ids)]
            action_rec['domain'] = domain

        return action_rec