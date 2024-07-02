from odoo import api, fields, models, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class OrganizationChart(models.Model):
    _name = 'mgmtsystem.context.organization_chart'
    _inherit = 'mgmtsystem.validation.mail'

    name = fields.Char(string='Nombre')
    parent_edition = fields.Many2one(
        comodel_name='mgmtsystem.context.organization_chart', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='mgmtsystem.context.organization_chart', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})
    active = fields.Boolean('Active', default=True)
    organization_chart_id = fields.Many2one(
        'org.chart.employee', string='Organigrama')

    

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_context.context_org_chart_cancel_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result
