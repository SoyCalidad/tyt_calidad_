from odoo import api, fields, models


class MgmtsystemContextInternalIssue(models.Model):
    _inherit = 'mgmtsystem.context.internal_issue'

    quality_scope = fields.Text(
        string='Alcance del sistema de gestión de calidad')

    @api.onchange('quality_scope')
    def _onchange_quality_scope(self):
        for each in self:
            each.scope = each.quality_scope


class MgmtsystemTarget(models.Model):
    _inherit = 'mgmtsystem.target'

    policy_id = fields.Many2one('mgmtsystem.context.policy', string='Política')


class MgmtsystemContextPolicy(models.Model):
    _inherit = 'mgmtsystem.context.policy'

    target_ids = fields.One2many(
        'mgmtsystem.target', 'policy_id', string='Objetivos')

    def get_content_by_type(self):
        super().get_content_by_type()
        if self.system_id.name == 'Calidad':
            final_content = ''
            fields = ['introduction', 'organization_context', 'direction_help', 'customer_satisfaction', 'legal_req', 'standar_commitment',
                      'staff_participation', 'continous_improvement', 'quality_goal_pre', 'target_ids', 'communication']
            css = """h1 { font-weight: 300; font-size: 38px; margin: 0px 0px 0px 0px; line-height: 120%; font-family: 'Open sans', sans-serif; }
p { text-align: justify;text-justify: inter-word; }"""
            final_content += '<style type="text/css">{}</style>'.format(css)
            for field in fields:
                if field != 'target_ids':
                    content = getattr(self, field)
                else:
                    content = '<ul>'
                    for target in self.target_ids:
                        content += '<li>{}</li>'.format(target.name)
                    content += '</ul>'
                field_string = self._fields[field].string
                if field != 'introduction':
                    final_content += '<h5>{}</h5><p>{}</p>'.format(
                        field_string, content) if content else ''
                else:
                    final_content += '<p>{}</p>'.format(
                        content) if content else ''
            return final_content
