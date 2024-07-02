from odoo import api, fields, models


class ManagementReview(models.Model):
    _name = 'management.review'
    _inherit = ['management.review', 'model.origin.abstract']

    target_ids = fields.Many2many('mgmtsystem.target', string='Objetivos')
    targets_count = fields.Integer(
        compute='_compute_targets_count', string='Objetivos')

    nonconformity_ids = fields.Many2many(
        'mgmtsystem.nonconformity', string='No conformidades')
    nonconformities_count = fields.Integer(
        compute='_compute_nonconformities_count', string='No conformidades')

    action_ids = fields.Many2many('mgmtsystem.action', string='Acciones')
    actions_count = fields.Integer(
        compute='_compute_actions_count', string='Acciones')

    risk_ids = fields.Many2many('matrix.block.line',
                                relation='managementreview_risk_rel',
                                column1='risk_id',
                                column2='managementreview_id',
                                string='Riesgos',
                                domain=[('type', '=', 'risk')])
    risks_count = fields.Integer(
        compute='_compute_risks_count', string='Riesgos')

    opp_ids = fields.Many2many('matrix.block.line',
                               relation='managementreview_op_rel',
                               column1='opp_id',
                               column2='managementreview_id',
                               string='Oportunidades',
                               domain=[('type', '=', 'opportunity')])
    opps_count = fields.Integer(
        compute='_compute_opps_count', string='Oportunidades')

    @api.depends('action_ids')
    def _compute_actions_count(self):
        for each in self:
            if each.action_ids:
                each.actions_count = len(self.action_ids)
            else:
                each.actions_count = 0

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
        result = super(ManagementReview, self).write(values)
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
    #     if type == 'opp':
    #         sql = "select count(*) from matrix_block_line m join matrix_block_line_origin as o on o.line_id = m.id "
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
    #     if self.risk_ids:
    #         for record in self.risk_ids:
    #             if not self.exist_origin('opp', record.id):
    #                 record.write({
    #                     'origin_model_id': self.model_id.id,
    #                     'origin_int_id': self.id})
    #     if self.opp_ids:
    #         for record in self.opp_ids:
    #             if not self.exist_origin('opp', record.id):
    #                 record.write({
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
    def _compute_targets_count(self):
        for each in self:
            if each.target_ids:
                each.targets_count = len(self.target_ids)
            else:
                each.targets_count = 0


class TargetComplaint(models.Model):
    _inherit = 'mgmtsystem.target'

    managementreview_ids = fields.Many2many(
        'management.review',
        string='Revisión por la dirección',
        relation='target_managementreview_rel',
        column1='managementreview_id',
        column2='target_id',)
    managementreviews_count = fields.Integer(
        compute='_compute_managementreviews_count', string='Revisión por la dirección')

    @api.depends('managementreview_ids')
    def _compute_managementreviews_count(self):
        for each in self:
            if each.managementreview_ids:
                each.managementreviews_count = len(each.managementreview_ids)
            else:
                each.managementreviews_count = 0


class NonconformityComplaint(models.Model):
    _inherit = 'mgmtsystem.nonconformity'

    managementreview_ids = fields.Many2many(
        'management.review',
        string='Revisión por la dirección',
        relation='nonconformity_managementreview_rel',
        column1='managementreview_id',
        column2='nonconformity_id',)
    managementreviews_count = fields.Integer(
        compute='_compute_managementreviews_count', string='Revisión por la dirección')

    @api.depends('managementreview_ids')
    def _compute_managementreviews_count(self):
        for each in self:
            if each.managementreview_ids:
                each.managementreviews_count = len(each.managementreview_ids)
            else:
                each.managementreviews_count = 0


class ActionComplaint(models.Model):
    _inherit = 'mgmtsystem.action'

    managementreview_ids = fields.Many2many(
        'management.review',
        relation='action_managementreview_rel',
        column1='managementreview_id',
        column2='action_id',)
    managementreviews_count = fields.Integer(
        compute='_compute_managementreviews_count', string='Revisión por la dirección')

    @api.depends('managementreview_ids')
    def _compute_managementreviews_count(self):
        for each in self:
            if each.managementreview_ids:
                each.managementreviews_count = len(each.managementreview_ids)
            else:
                each.managementreviews_count = 0


class ManagementReviewPlan(models.Model):
    _name = 'management.review.plan'
    _inherit = ['management.review.plan', 'model.origin.abstract']

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

    revisiones = fields.Many2many('management.review', string='Revisiones')
    revisiones_count = fields.Integer(
        compute='_compute_reviews_count', string='Revisiones')

    @api.depends('line_ids')
    def _compute_reviews_count(self):
        for each in self:
            total = len(each.line_ids)
            each.revisiones_count = total

    @api.depends('line_ids')
    def _compute_actions_count(self):
        for each in self:
            total = 0
            for line in each.line_ids:
                total += len(line.action_ids)
            total += len(each.action_ids)
            each.actions_count = total

    @api.depends('line_ids')
    def _compute_nonconformities_count(self):
        for each in self:
            total = 0
            for line in each.line_ids:
                total += len(line.nonconformity_ids)
            total += len(each.nonconformity_ids)
            each.nonconformities_count = total

    @api.depends('line_ids')
    def _compute_indicators_count(self):
        for each in self:
            total = 0
            for line in each.line_ids:
                total += len(line.target_ids)
            total += len(each.target_ids)
            each.targets_count = total

    def action_mgmtreviewplan_views(self):
        type_action = self._context.get('type_action', '')
        if type_action == '':
            return
        ids = []

        if type_action == 'target':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.action_mgmtreview_plan_target').read()[0]
            for each in self:
                for lin in each.line_ids:
                    ids.extend(lin.target_ids.ids)
            domain = [('id', 'in', ids)]
            action_rec['domain'] = domain

        elif type_action == 'nc':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.action_mgmtreview_plan_nc').read()[0]
            for each in self:
                for lin in each.line_ids:
                    ids.extend(lin.nonconformity_ids.ids)
            domain = [('id', 'in', ids)]
            action_rec['domain'] = domain

        elif type_action == 'action':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.action_mgmtreview_plan_action').read()[0]
            for each in self:
                for lin in each.line_ids:
                    ids.extend(lin.action_ids.ids)
            domain = [('id', 'in', ids)]
            action_rec['domain'] = domain
            print("----->", domain)
        elif type_action == 'revi':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.action_mgmtreview_revisiones').read()[0]

            domain = [('id', 'in', self.lines_ids.ids)]
            action_rec['domain'] = domain
            print("----->", domain)

        return action_rec
