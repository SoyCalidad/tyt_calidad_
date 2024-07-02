from odoo import api, fields, models


class PolicyWizard(models.TransientModel):
    _name = 'wizard.policy.report'
    
    policy_id = fields.Many2one('mgmtsystem.context.policy', string='Política de calidad')
    
    def action_print(self):
        data = self.read()[0]
        datas = {
            'ids': self._ids,
            'policies': self.policy_id.id,
            'is_wizard': True,
            'model': 'wizard.policy.report',
            'res_model': 'wizard.policy.report',
        }
        return self.env.ref('mgmtsystem_context.action_context_policy_report_2').report_action(self, data=datas)