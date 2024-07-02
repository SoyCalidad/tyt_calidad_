from odoo import _, api, fields, models
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class Target(models.Model):
    _name = 'mgmtsystem.target'
    _inherit = ['mgmtsystem.target', 'model.origin.abstract']

    nonconformity_ids = fields.Many2many(
        'mgmtsystem.nonconformity', string='No conformidades')
    nonconformities_count = fields.Integer(
        compute='_compute_nonconformities_count', string='No conformidades')

    comunication_ids = fields.Many2many(
        comodel_name='comunication.plan.line', relation='complanline_target_rel', string='Comunicaciones')
    comunications_count = fields.Integer(
        compute='_compute_comunications_count', string='Comunicaciones')

    resource_ids = fields.Many2many('mgmt.process.resource', string='Recursos')

    @api.depends('comunication_ids')
    def _compute_comunications_count(self):
        for each in self:
            if each.comunication_ids:
                each.comunications_count = len(each.comunication_ids)
            else:
                each.comunications_count = 0

    @api.depends('nonconformity_ids')
    def _compute_nonconformities_count(self):
        for each in self:
            if each.nonconformity_ids:
                each.nonconformities_count = len(each.nonconformity_ids)
            else:
                each.nonconformities_count = 0

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

        result = super(Target, self).write(values)
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
