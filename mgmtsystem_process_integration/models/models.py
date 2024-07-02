from odoo import api, fields, models


class InternalIssue(models.Model):
    _name = 'mgmtsystem.context.internal_issue'
    _inherit = ['mgmtsystem.context.internal_issue', 'model.origin.abstract']

    nonconformity_ids = fields.Many2many(
        'mgmtsystem.nonconformity', string='No conformidades', relation='internal_issue_nc')
    nonconformities_count = fields.Integer(
        compute='_compute_nonconformities_count', string='No conformidades')
    target_ids = fields.Many2many('mgmtsystem.target', string='Objetivos')
    targets_count = fields.Integer(
        compute='_compute_indicators_count', string='Objetivos')

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
        result = super(InternalIssue, self).write(values)
        self.verify_origin()
        return result

    @api.depends('target_ids')
    def _compute_indicators_count(self):
        for each in self:
            if each.target_ids:
                each.targets_count = len(self.target_ids)
            else:
                each.targets_count = 0

    @api.depends('nonconformity_ids')
    def _compute_nonconformities_count(self):
        for each in self:
            if each.nonconformity_ids:
                each.nonconformities_count = len(each.nonconformity_ids)
            else:
                each.nonconformities_count = 0


class ExternalIssue(models.Model):
    _name = 'mgmtsystem.context.external_issue'
    _inherit = ['mgmtsystem.context.external_issue', 'model.origin.abstract']

    nonconformity_ids = fields.Many2many(
        'mgmtsystem.nonconformity', string='No conformidades', relation='external_issue_nc')
    nonconformities_count = fields.Integer(
        compute='_compute_nonconformities_count', string='No conformidades')
    target_ids = fields.Many2many('mgmtsystem.target', string='Objetivos')
    targets_count = fields.Integer(
        compute='_compute_indicators_count', string='Objetivos')

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
        result = super(ExternalIssue, self).write(values)
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

    @api.depends('target_ids')
    def _compute_indicators_count(self):
        for each in self:
            if each.target_ids:
                each.targets_count = len(self.target_ids)
            else:
                each.targets_count = 0

    @api.depends('nonconformity_ids')
    def _compute_nonconformities_count(self):
        for each in self:
            if each.nonconformity_ids:
                each.nonconformities_count = len(each.nonconformity_ids)
            else:
                each.nonconformities_count = 0


class SWOT(models.Model):
    _name = 'mgmtsystem.context.swot'
    _inherit = ['mgmtsystem.context.swot', 'model.origin.abstract']

    nonconformity_ids = fields.Many2many(
        'mgmtsystem.nonconformity', string='No conformidades', relation='swot_nc')
    nonconformities_count = fields.Integer(
        compute='_compute_nonconformities_count', string='No conformidades')
    target_ids = fields.Many2many('mgmtsystem.target', string='Objetivos')
    targets_count = fields.Integer(
        compute='_compute_indicators_count', string='Objetivos')

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
        result = super(SWOT, self).write(values)
        self.verify_origin()
        return result

    @api.depends('target_ids')
    def _compute_indicators_count(self):
        for each in self:
            if each.target_ids:
                each.targets_count = len(self.target_ids)
            else:
                each.targets_count = 0

    @api.depends('nonconformity_ids')
    def _compute_nonconformities_count(self):
        for each in self:
            if each.nonconformity_ids:
                each.nonconformities_count = len(each.nonconformity_ids)
            else:
                each.nonconformities_count = 0

    risk_ids = fields.Many2many('matrix.block.line', relation='swot_risk_rel',
                                string='Riesgos', domain=[('type', '=', 'risk')])
    risks_count = fields.Integer(
        compute='_compute_risks_count', string='Riesgos')

    opp_ids = fields.Many2many('matrix.block.line', relation='swot_op_rel',
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

    def action_opp_views(self):
        type_action = self._context.get(
            'type_action', '')
        if type_action == '':
            return
        ids = []
        if type_action == 'risk':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.show_risk_action_action').read()[0]
            ids = self.risk_ids.ids
        elif type_action == 'opp':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.show_opp_action_action').read()[0]
            ids = self.opp_ids.ids
        domain = [('id', 'in', ids)]
        action_rec['domain'] = domain
        return action_rec


class CrossSWOT(models.Model):
    _name = 'mgmtsystem.context.cross.swot'
    _inherit = ['mgmtsystem.context.cross.swot', 'model.origin.abstract']

    nonconformity_ids = fields.Many2many(
        'mgmtsystem.nonconformity', string='No conformidades', relation='cross_swot_nc')
    nonconformities_count = fields.Integer(
        compute='_compute_nonconformities_count', string='No conformidades')
    target_ids = fields.Many2many('mgmtsystem.target', string='Objetivos')
    targets_count = fields.Integer(
        compute='_compute_indicators_count', string='Objetivos')

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
        result = super(CrossSWOT, self).write(values)
        self.verify_origin()
        return result

    @api.depends('target_ids')
    def _compute_indicators_count(self):
        for each in self:
            if each.target_ids:
                each.targets_count = len(self.target_ids)
            else:
                each.targets_count = 0

    @api.depends('nonconformity_ids')
    def _compute_nonconformities_count(self):
        for each in self:
            if each.nonconformity_ids:
                each.nonconformities_count = len(each.nonconformity_ids)
            else:
                each.nonconformities_count = 0


class Stakeholders(models.Model):
    _name = 'mgmtsystem.stakeholders'
    _inherit = ['mgmtsystem.stakeholders', 'model.origin.abstract']

    nonconformity_ids = fields.Many2many(
        'mgmtsystem.nonconformity', string='No conformidades', relation="stak_nc_rel")
    nonconformities_count = fields.Integer(
        compute='_compute_nonconformities_count', string='No conformidades')
    target_ids = fields.Many2many(
        'mgmtsystem.target', string='Objetivos', relation="stak_target_rel")
    targets_count = fields.Integer(
        compute='_compute_indicators_count', string='Objetivos')

    action_ids = fields.Many2many(
        'mgmtsystem.action', string='Acciones', relation="stak_action_rel")
    actions_count = fields.Integer(
        compute='_compute_actions_count', string='Acciones')

    risks_count = fields.Integer(
        compute='_compute_risks_count', string='Riesgos')
    opps_count = fields.Integer(
        compute='_compute_risks_count', string='Oportunidades')

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
        result = super(Stakeholders, self).write(values)
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

    @api.depends('stakeholder_in_ids', 'stakeholder_out_ids')
    def _compute_risks_count(self):
        for each in self:
            risks_count = 0
            opps_count = 0
            for factor in self.stakeholder_in_ids + self.stakeholder_out_ids:
                opps_count += len(factor.opportunity_ids)
                risks_count += len(factor.risk_ids)
            each.risks_count = risks_count
            each.opps_count = opps_count

    def action_opp_views(self):
        type_action = self._context.get(
            'type_action', '')
        if type_action == '':
            return
        ids = []
        if type_action == 'risk':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.show_risk_action_action').read()[0]
            for each in self:
                for factor in each.stakeholder_in_ids + each.stakeholder_out_ids:
                    ids.extend(factor.risk_ids.ids)
        elif type_action == 'opp':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.show_opp_action_action').read()[0]
            for each in self:
                for factor in each.stakeholder_in_ids + each.stakeholder_out_ids:
                    ids.extend(factor.opportunity_ids.ids)
        domain = [('id', 'in', ids)]
        action_rec['domain'] = domain
        return action_rec

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
    def _compute_indicators_count(self):
        for each in self:
            if each.target_ids:
                each.targets_count = len(self.target_ids)
            else:
                each.targets_count = 0


class Stakeholder(models.Model):
    _name = 'mgmtsystem.stakeholder'
    _inherit = ['mgmtsystem.stakeholder', 'model.origin.abstract']

    action_ids = fields.Many2many('mgmtsystem.action', string='Acciones')

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

    # def exist_origin(self, type, type_id):
    #     sql = ""
    #     if type == 'action':
    #         sql = "select count(*) from mgmtsystem_action m join mgmtsystem_action_origin as o on o.action_id = m.id "
    #     sql = ("%s where m.id = %s and o.origin_model_id = %s and o.origin_int_id = %s") % (
    #         sql, type_id, self.model_id.id, self.id)
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


class StakeholderReq(models.Model):
    _inherit = 'mgmtsystem.stakeholder.req'

    is_legal = fields.Boolean(string='Es requisito legal')
    legal_id = fields.Many2one('legal.legal', string='Requisito legal')


class PEST(models.Model):
    _name = 'mgmtsystem.context.pest'
    _inherit = ['mgmtsystem.context.pest', 'model.origin.abstract']

    nonconformity_ids = fields.Many2many(
        'mgmtsystem.nonconformity', string='No conformidades', relation="nc_pest_rel")
    nonconformities_count = fields.Integer(
        compute='_compute_nonconformities_count', string='No conformidades')
    target_ids = fields.Many2many(
        'mgmtsystem.target', string='Objetivos', relation='target_pest_rel')
    targets_count = fields.Integer(
        compute='_compute_indicators_count', string='Objetivos')

    action_ids = fields.Many2many(
        'mgmtsystem.action', string='Acciones', relation='action_pest_rel')
    actions_count = fields.Integer(
        compute='_compute_actions_count', string='Acciones')

    risks_count = fields.Integer(
        compute='_compute_opps_count', string='Riesgos')
    opps_count = fields.Integer(
        compute='_compute_opps_count', string='Oportunidades')

    @api.depends('factor_ids', 'politic_factor_ids', 'economic_factor_ids', 'sociocult_factor_ids', 'tech_factor_ids', 'ecologic_factor_ids', 'legal_factor_ids')
    def _compute_opps_count(self):
        for each in self:
            risks_count = 0
            opps_count = 0
            if each.custom_analysis:
                for factor in self.factor_ids:
                    opps_count += len(factor.opportunity_ids)
                    risks_count += len(factor.risk_ids)
            else:
                for factor in each.politic_factor_ids:
                    opps_count += len(factor.opportunity_ids)
                    risks_count += len(factor.risk_ids)
                for factor in each.economic_factor_ids:
                    opps_count += len(factor.opportunity_ids)
                    risks_count += len(factor.risk_ids)
                for factor in each.sociocult_factor_ids:
                    opps_count += len(factor.opportunity_ids)
                    risks_count += len(factor.risk_ids)
                for factor in each.tech_factor_ids:
                    opps_count += len(factor.opportunity_ids)
                    risks_count += len(factor.risk_ids)
                for factor in each.ecologic_factor_ids:
                    opps_count += len(factor.opportunity_ids)
                    risks_count += len(factor.risk_ids)
                for factor in each.legal_factor_ids:
                    opps_count += len(factor.opportunity_ids)
                    risks_count += len(factor.risk_ids)
            each.risks_count = risks_count
            each.opps_count = opps_count

    def action_opp_views(self):
        type_action = self._context.get(
            'type_action', '')
        if type_action == '':
            return
        ids = []

        if self.custom_analysis:
            if type_action == 'risk':
                action_rec = self.env.ref(
                    'mgmtsystem_process_integration.show_risk_action_action').read()[0]
                for each in self:
                    for factor in each.factor_ids:
                        ids.extend(factor.risk_ids.ids)
            elif type_action == 'opp':
                action_rec = self.env.ref(
                    'mgmtsystem_context.show_opp_action_action').read()[0]
                for each in self:
                    for factor in each.factor_ids:
                        ids.extend(factor.opportunity_ids.ids)
        else:
            if type_action == 'risk':
                action_rec = self.env.ref(
                    'mgmtsystem_process_integration.show_risk_action_action').read()[0]
                for each in self:
                    for factor in each.politic_factor_ids:
                        ids.extend(factor.risk_ids.ids)
                    for factor in each.economic_factor_ids:
                        ids.extend(factor.risk_ids.ids)
                    for factor in each.sociocult_factor_ids:
                        ids.extend(factor.risk_ids.ids)
                    for factor in each.tech_factor_ids:
                        ids.extend(factor.risk_ids.ids)
                    for factor in each.ecologic_factor_ids:
                        ids.extend(factor.risk_ids.ids)
                    for factor in each.legal_factor_ids:
                        ids.extend(factor.risk_ids.ids)
            elif type_action == 'opp':
                action_rec = self.env.ref(
                    'mgmtsystem_process_integration.show_opp_action_action').read()[0]
                for each in self:
                    for factor in each.politic_factor_ids:
                        ids.extend(factor.opportunity_ids.ids)
                    for factor in each.economic_factor_ids:
                        ids.extend(factor.opportunity_ids.ids)
                    for factor in each.sociocult_factor_ids:
                        ids.extend(factor.opportunity_ids.ids)
                    for factor in each.tech_factor_ids:
                        ids.extend(factor.opportunity_ids.ids)
                    for factor in each.ecologic_factor_ids:
                        ids.extend(factor.opportunity_ids.ids)
                    for factor in each.legal_factor_ids:
                        ids.extend(factor.opportunity_ids.ids)
        domain = [('id', 'in', ids)]
        action_rec['domain'] = domain
        return action_rec

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
        result = super(PEST, self).write(values)
        self.verify_origin()
        return result

    @api.depends('target_ids')
    def _compute_indicators_count(self):
        for each in self:
            if each.target_ids:
                each.targets_count = len(self.target_ids)
            else:
                each.targets_count = 0

    @api.depends('nonconformity_ids')
    def _compute_nonconformities_count(self):
        for each in self:
            if each.nonconformity_ids:
                each.nonconformities_count = len(each.nonconformity_ids)
            else:
                each.nonconformities_count = 0


class Target(models.Model):
    _inherit = 'mgmtsystem.target'

    internal_issue_ids = fields.Many2many(
        'mgmtsystem.context.internal_issue', string='Contexto organizacional')
    internal_isssues_count = fields.Integer(
        compute='_compute_internal_isssues_count', string='Contexto Organizacional')

    external_issue_ids = fields.Many2many(
        'mgmtsystem.context.external_issue', string='Factores externos')
    external_issues_count = fields.Integer(
        compute='_compute_external_isssues_count', string='Factores externos')

    swot_ids = fields.Many2many('mgmtsystem.context.swot', string='FODA')
    swot_count = fields.Integer(
        compute='_compute_swot_count', string='Contexto Organizacional')

    cross_swot_ids = fields.Many2many(
        'mgmtsystem.context.cross.swot', string='FODA Cruzado')
    cross_swot_count = fields.Integer(
        compute='_compute_cross_swot_count', string='FODA Cruzado')

    pest_ids = fields.Many2many(
        'mgmtsystem.context.pest', relation='target_pest_rel', string='Análisis PESTEL')
    pest_count = fields.Integer(
        compute='_compute_pest_count', string='Análisis PESTEL')

    stakeholders_ids = fields.Many2many(
        'mgmtsystem.stakeholders', string='Interesados', relation="stak_target_rel")
    stakeholders_count = fields.Integer(
        compute='_compute_stakeholders_count', string='Interesados')

    policy_ids = fields.Many2many(
        'mgmtsystem.context.policy', string='Políticas', relation="target_policy_rel")
    policies_count = fields.Integer(
        compute='_compute_policies_count', string='Políticas')

    @api.depends('policy_ids')
    def _compute_policies_count(self):
        for each in self:
            if each.policy_ids:
                each.policies_count = len(self.policy_ids)
            else:
                each.policies_count = 0

    @api.depends('stakeholders_ids')
    def _compute_stakeholders_count(self):
        for each in self:
            if each.stakeholders_ids:
                each.stakeholders_count = len(self.stakeholders_ids)
            else:
                each.stakeholders_count = 0

    @api.depends('pest_ids')
    def _compute_pest_count(self):
        for each in self:
            if each.pest_ids:
                each.pest_count = len(self.pest_ids)
            else:
                each.pest_count = 0

    @api.depends('internal_issue_ids')
    def _compute_internal_isssues_count(self):
        for each in self:
            each.internal_isssues_count = len(each.internal_issue_ids)

    @api.depends('external_issue_ids')
    def _compute_external_isssues_count(self):
        for each in self:
            each.internal_isssues_count = len(each.external_issue_ids)

    @api.depends('swot_ids')
    def _compute_swot_count(self):
        for each in self:
            each.internal_isssues_count = len(each.swot_ids)

    @api.depends('cross_swot_ids')
    def _compute_cross_swot_count(self):
        for each in self:
            each.internal_isssues_count = len(each.cross_swot_ids)


class Action(models.Model):
    _inherit = 'mgmtsystem.action'

    internal_issue_ids = fields.Many2many(
        'mgmtsystem.context.internal_issue', string='Contexto organizacional')
    internal_isssues_count = fields.Integer(
        compute='_compute_internal_isssues_count', string='Contexto Organizacional')

    external_issue_ids = fields.Many2many(
        'mgmtsystem.context.external_issue', string='Factores externos')
    external_issues_count = fields.Integer(
        compute='_compute_internal_isssues_count', string='Contexto Organizacional')

    swot_ids = fields.Many2many('mgmtsystem.context.swot', string='FODA')
    swot_count = fields.Integer(
        compute='_compute_swot_count', string='Contexto Organizacional')

    cross_swot_ids = fields.Many2many(
        'mgmtsystem.context.cross.swot', string='FODA Cruzado')
    cross_swot_count = fields.Integer(
        compute='_compute_cross_swot_count', string='Contexto Organizacional')

    pest_ids = fields.Many2many(
        'mgmtsystem.context.pest', relation='action_pest_rel', string='Análisis PESTEL')
    pest_count = fields.Integer(
        compute='_compute_pest_count', string='Análisis PESTEL')

    stakeholders_ids = fields.Many2many(
        'mgmtsystem.stakeholders', string='Interesados', relation="stak_action_rel")
    stakeholders_count = fields.Integer(
        compute='_compute_stakeholders_count', string='Interesados')

    policy_ids = fields.Many2many(
        'mgmtsystem.context.policy', string='Políticas', relation="action_policy_rel")
    policies_count = fields.Integer(
        compute='_compute_policies_count', string='Políticas')

    @api.depends('policy_ids')
    def _compute_policies_count(self):
        for each in self:
            if each.policy_ids:
                each.policies_count = len(self.policy_ids)
            else:
                each.policies_count = 0

    @api.depends('stakeholders_ids')
    def _compute_stakeholders_count(self):
        for each in self:
            if each.stakeholders_ids:
                each.stakeholders_count = len(self.stakeholders_ids)
            else:
                each.stakeholders_count = 0

    @api.depends('pest_ids')
    def _compute_pest_count(self):
        for each in self:
            if each.pest_ids:
                each.pest_count = len(self.pest_ids)
            else:
                each.pest_count = 0

    @api.depends('internal_issue_ids')
    def _compute_internal_isssues_count(self):
        for each in self:
            each.internal_isssues_count = len(each.internal_issue_ids)

    @api.depends('external_issue_ids')
    def _compute_external_isssues_count(self):
        for each in self:
            each.internal_isssues_count = len(each.external_issue_ids)

    @api.depends('swot_ids')
    def _compute_swot_count(self):
        for each in self:
            each.internal_isssues_count = len(each.swot_ids)

    @api.depends('cross_swot_ids')
    def _compute_cross_swot_count(self):
        for each in self:
            each.internal_isssues_count = len(each.cross_swot_ids)


class Policy(models.Model):
    _name = 'mgmtsystem.context.policy'
    _inherit = ['mgmtsystem.context.policy', 'model.origin.abstract']

    nonconformity_ids = fields.Many2many(
        'mgmtsystem.nonconformity', string='No conformidades', relation="nc_policy_rel")
    nonconformities_count = fields.Integer(
        compute='_compute_nonconformities_count', string='No conformidades')
    target_ids = fields.Many2many(
        'mgmtsystem.target', string='Objetivos', relation='target_policy_rel')
    targets_count = fields.Integer(
        compute='_compute_indicators_count', string='Objetivos')

    action_ids = fields.Many2many(
        'mgmtsystem.action', string='Acciones', relation='action_policy_rel')
    actions_count = fields.Integer(
        compute='_compute_actions_count', string='Acciones')

    risk_ids = fields.Many2many('matrix.block.line', relation='policy_risk_rel',
                                string='Riesgos', domain=[('type', '=', 'risk')])
    risks_count = fields.Integer(
        compute='_compute_risks_count', string='Riesgos')

    opp_ids = fields.Many2many('matrix.block.line', relation='policy_op_rel',
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

    @api.depends('action_ids')
    def _compute_actions_count(self):
        for each in self:
            if each.action_ids:
                each.actions_count = len(self.action_ids)
            else:
                each.actions_count = 0

    @api.depends('target_ids')
    def _compute_indicators_count(self):
        for each in self:
            if each.target_ids:
                each.targets_count = len(self.target_ids)
            else:
                each.targets_count = 0

    @api.depends('nonconformity_ids')
    def _compute_nonconformities_count(self):
        for each in self:
            if each.nonconformity_ids:
                each.nonconformities_count = len(each.nonconformity_ids)
            else:
                each.nonconformities_count = 0

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
        result = super(Policy, self).write(values)
        self.verify_origin()
        return result

    def action_opp_views(self):
        type_action = self._context.get(
            'type_action', '')
        if type_action == '':
            return
        ids = []
        if type_action == 'risk':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.show_risk_action_action').read()[0]
            for each in self:
                ids.extend(each.risk_ids.ids)
        elif type_action == 'opp':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.show_opp_action_action').read()[0]
            for each in self:
                ids.extend(each.opp_ids.ids)
        domain = [('id', 'in', ids)]
        action_rec['domain'] = domain
        return action_rec
