# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class NonConformity(models.Model):
    _inherit = 'mgmtsystem.nonconformity'

    report_id = fields.Many2one(
        string=u'Informe asociado',
        comodel_name='audit.report',
        ondelete='cascade',
    )

    employee_id = fields.Many2one(
        string=u'Responsable',
        comodel_name='hr.employee',
        ondelete='cascade',
    )
    process_id = fields.Many2one(
        string=u'Doc.Ref',
        comodel_name='mgmt.process',
        ondelete='cascade', 
        domain=[('active', '=', True)]
    )
    # auditor_id = fields.Many2one(
    #     string=u'Auditor',
    #     comodel_name='res.partner',
    # )
    auditor_id = fields.Reference(selection=[('res.partner', 'Auditor externo'), (
        'hr.employee', 'Auditor interno'), ], string="Auditor")
    standard = fields.Char(
        string=u'Requisito de la norma',
        required=True,
    )
    team_id = fields.Many2one(
        string=u'Equipo',
        comodel_name='audit.team',
        ondelete='cascade',
    )
    date_found = fields.Date(
        string=u'Fecha de hallazgo',
        default=fields.Date.context_today,
    )
    date_limit = fields.Date(
        string=u'Fecha límite',
        default=fields.Date.context_today,
    )

    action_count = fields.Integer(
        string='Acciones', compute='_compute_action_ids')

    @api.depends('action_ids')
    def _compute_action_ids(self):
        for each in self:
            each.action_count = len(each.action_ids)

    def action_view_actions(self):
        action = self.env.ref('purchase.purchase_form_action').read()[0]
        purchases = self.mapped('purchase_ids')
        if len(purchases) > 1:
            action['domain'] = [('id', 'in', purchases.ids)]
        elif purchases:
            action['views'] = [
                (self.env.ref('purchase.purchase_order_form').id, 'form')]
            action['res_id'] = purchases.id
        return action


class Action(models.Model):
    _inherit = 'mgmtsystem.action'

    nonconformity_id = fields.Many2one(
        string=u'No conformidad',
        comodel_name='mgmtsystem.nonconformity',
        ondelete='cascade',
    )

    nonconformity_count = fields.Integer(
        string='No conformidades', compute='_compute_nonconformity_ids')

    @api.depends('nonconformity_ids')
    def _compute_nonconformity_ids(self):
        for each in self:
            each.nonconformity_count = len(each.nonconformity_ids)

    def action_view_nonconformity(self):
        action = self.env.ref('purchase.purchase_form_action').read()[0]
        purchases = self.mapped('purchase_ids')
        if len(purchases) > 1:
            action['domain'] = [('id', 'in', purchases.ids)]
        elif purchases:
            action['views'] = [
                (self.env.ref('purchase.purchase_order_form').id, 'form')]
            action['res_id'] = purchases.id
        return action
