from odoo import api, fields, models

class MgmtsystemContextPolicy(models.Model):
    _inherit = 'mgmtsystem.context.policy'
    
    action_ids = fields.Many2many('mgmtsystem.action', string='Acciones')
    action_count = fields.Char(compute='_compute_action_count', string='Acciones')
    
    @api.depends('action_ids')
    def _compute_action_count(self):
        for each in self:
            each.action_count = len(each.action_ids)

    def open_action_ids(self):
        """
        """
        result = self.env.ref(
            'mgmtsystem_action.open_mgmtsystem_action_list').read()[0]
        result['domain'] = [('id', 'in', self.action_ids.ids)]
        return result
    