from odoo import api, fields, models


class ComplaintTarget(models.Model):
    _name = 'complaint.complaint'
    _inherit = ['complaint.complaint', 'model.origin.abstract']

    target_ids = fields.Many2many('mgmtsystem.target', string='Objetivos')
    targets_count = fields.Integer(
        compute='_compute_targets_count', string='Objetivos')

    nonconformities_count = fields.Integer(
        compute='_compute_nonconformities_count', string='No conformidades')

    actions_count = fields.Integer(
        compute='_compute_actions_count', string='Acciones')

    risk_ids = fields.Many2many('matrix.block.line', relation='complaint_risk_rel', string='Riesgos', domain=[('type', '=', 'risk')])
    risks_count = fields.Integer(compute='_compute_risks_count', string='Riesgos')

    opp_ids = fields.Many2many('matrix.block.line', relation='complaint_op_rel', string='Oportunidades', domain=[('type', '=', 'opportunity')])
    opps_count = fields.Integer(compute='_compute_opps_count', string='Oportunidades')

    
    #Ayuda a ingresar el modelo de origen, no se guarda en la base de datos
    def compute_model_id(self):
        for record in self:
            record.model_id = self.env['ir.model'].search([('model','=',self._name)], limit=1)

    model_id = fields.Many2one(
        string='Modelo',
        comodel_name='ir.model',
        ondelete='cascade',
        compute=compute_model_id,
        store=False,
    )

    def write(self, values):
        result = super(ComplaintTarget, self).write(values)
        self.verify_origin()
        return result

    # def exist_origin(self, type, type_id):
    #     sql=""
    #     if type == 'action':
    #         sql = "select count(*) from mgmtsystem_action m join mgmtsystem_action_origin as o on o.action_id = m.id "
    #     if type == 'nc':
    #         sql = "select count(*) from mgmtsystem_nonconformity m join mgmtsystem_nonconformity_origin as o on o.nc_id = m.id "
    #     if type == 'target':
    #         sql = "select count(*) from mgmtsystem_target m join mgmtsystem_target_origin as o on o.target_id = m.id "
    #     if type == 'opp':
    #         sql = "select count(*) from matrix_block_line m join matrix_block_line_origin as o on o.line_id = m.id "
    #     sql = ("%s where m.id = %s and o.origin_model_id = %s and o.origin_int_id = %s") % (sql, type_id, self.model_id.id, self.id)
    #     print('-> sql',sql)
    #     self.env.cr.execute(sql)
    #     res_all = self.env.cr.fetchall()
    #     if res_all[0][0] == 0:
    #         return False
    #     return True

    #Verifica que los origenes tengan de origen el presente
    # def verify_origin(self):
    #     if self.target_ids:
    #         for record in self.target_ids:
    #             if not self.exist_origin('target', record.id):
    #                 record.write({
    #                     'origin_model_id': self.model_id.id,
    #                     'origin_int_id': self.id})
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

    complaint_ids = fields.Many2many(
        'complaint.complaint', 
        string='Reclamos',
        relation='target_complaint_rel')
    complaints_count = fields.Integer(
        compute='_compute_complaints_count', string='Reclamos')

    @api.depends('complaint_ids')
    def _compute_complaints_count(self):
        for each in self:
            if each.complaint_ids:
                each.complaints_count = len(each.complaint_ids)
            else:
                each.complaints_count = 0


class NonconformityComplaint(models.Model):
    _inherit = 'mgmtsystem.nonconformity'

    complaint_ids = fields.Many2many(
        'complaint.complaint',
        string='Reclamos',
        relation='nonconformity_complaint_rel',
        column1='complaint_id',
        column2='nonconformity_id',)
    complaints_count = fields.Integer(
        compute='_compute_complaints_count', string='Reclamos')

    @api.depends('complaint_ids')
    def _compute_complaints_count(self):
        for each in self:
            if each.complaint_ids:
                each.complaints_count = len(each.complaint_ids)
            else:
                each.complaints_count = 0


class ActionComplaint(models.Model):
    _inherit = 'mgmtsystem.action'

    complaint_ids = fields.Many2many(
        'complaint.complaint',
        relation='action_complaint_rel',
        column1='complaint_id',
        column2='action_id',)
    complaints_count = fields.Integer(
        compute='_compute_complaints_count', string='Reclamos')

    @api.depends('complaint_ids')
    def _compute_complaints_count(self):
        for each in self:
            if each.complaint_ids:
                each.complaints_count = len(each.complaint_ids)
            else:
                each.complaints_count = 0


class RiskOppComplaint(models.Model):
    _inherit = 'matrix.block.line'

    complaint_ids = fields.Many2many(
        'complaint.complaint',
        relation='riskopp_complaint_rel',
        column1='complaint_id',
        column2='action_id',)
    complaints_count = fields.Integer(
        compute='_compute_complaints_count', string='Reclamos')

    @api.depends('complaint_ids')
    def _compute_complaints_count(self):
        for each in self:
            if each.complaint_ids:
                each.complaints_count = len(each.complaint_ids)
            else:
                each.complaints_count = 0
