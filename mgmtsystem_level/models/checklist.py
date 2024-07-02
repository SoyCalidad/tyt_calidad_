# Copyright 2019 Fenix Engineering Solutions
# @author Jose F. Fernandez
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _

import logging

_logger = logging.getLogger(__name__)


class ChecklistItem(models.Model):
    _name = 'checklist.item'
    _description = 'Task Checklist Item'
    _order = 'sequence, id'

    sequence = fields.Integer(default=10)
    level_id = fields.Many2one('mgmtsystem.level', string='Task', index=True)
    # company_id = fields.Many2one(related='level_id.company_id', string='Company', store=True, readonly=True)
    name = fields.Char(string='Nombre', required=True)

    action_id = fields.Many2one('mgmtsystem.action', string='Acción')
    action_date_open = fields.Datetime(related='action_id.date_open', string='Fecha de apertura')
    action_date_deadline = fields.Date(related='action_id.date_deadline', string='Fecha límite')
    action_state = fields.Selection(related='action_id.state', string='Estado')
    
    internal_issue_id1 = fields.Many2one(
        'mgmtsystem.context.internal_issue', string='Factores internos', index=True)
    internal_issue_id2 = fields.Many2one(
        'mgmtsystem.context.internal_issue', string='Factores internos', index=True)
    internal_issue_id3 = fields.Many2one(
        'mgmtsystem.context.internal_issue', string='Factores internos', index=True)

    policy_id1 = fields.Many2one(
        'mgmtsystem.context.policy', string='Política', index=True)
    policy_id2 = fields.Many2one(
        'mgmtsystem.context.policy', string='Política', index=True)
    policy_id3 = fields.Many2one(
        'mgmtsystem.context.policy', string='Política', index=True)
    
    checked = fields.Boolean(compute='_compute_checked', string='Cumplido', default=False)
    
    @api.depends('action_id')
    def _compute_checked(self):
        for each in self:
            if each.action_id:
                if each.action_id.state == 'done':
                    each.checked = True