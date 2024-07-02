# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class MgmtsystemAction(models.Model):
    _inherit = "mgmtsystem.action"

    nonconformity_ids = fields.Many2many(
        'mgmtsystem.nonconformity',
        'mgmtsystem_nonconformity_action_rel',
        'action_id',
        'nonconformity_id',
        'No conformidades',
        readonly=True,
    )

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

    approving_authority_id = fields.Many2one('res.users', string='Autoridad aprobatoria')


class ReportLine(models.Model):
    _inherit = "report.line"

    nc = fields.Selection(
        string=u'Tipo',
        selection=[
            ('na', 'NA'),
            ('mayor', 'Mayor'),
            ('menor', 'Menor'),
        ],
        default='na',
    )

    nc_id = fields.Many2one('mgmtsystem.nonconformity.type',
                            string='Tipo de hallazgo')


class AuditReport(models.Model):
    _inherit = "audit.report"

    nonconformity_ids = fields.One2many(
        string=u'No conformidades',
        comodel_name='mgmtsystem.nonconformity',
        inverse_name='report_id',
    )

    nonconformity_count = fields.Integer(
        string=u'No conformidades',
        compute='_compute_nonconformity_count',
        store=False,
    )

    @api.depends('nonconformity_ids')
    def _compute_nonconformity_count(self):
        for record in self:
            record.nonconformity_count = len(record.nonconformity_ids) or 0
