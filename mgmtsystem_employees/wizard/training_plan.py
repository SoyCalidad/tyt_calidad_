from odoo import api, fields, models

class TrainingPlanWizard(models.TransientModel):
    _name = 'training.plan.wizard'
    
    training_plan_id = fields.Many2one('mgmtsystem.plan', string='Programa de capacitaciones')
    
    def action_print(self):
        data = self.read()[0]
        datas = {
            'data': data,
            'is_wizard': True,
            'id': self.training_plan_id.id,
            'ids': self._ids,
            'model': 'training.plan.wizard',
            'res_model': 'training.plan.wizard',
        }
        return self.env.ref('mgmtsystem_employees.report_trainings').report_action(self, data=datas)
    

class TrainingPlanReport(models.AbstractModel):
    _name = 'report.mgmtsystem_employees.training_plan_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        
        if data and data.get('is_wizard'):
            training_plan_id = self.env['mgmtsystem.plan'].browse(data['id'])
        else:
            training_plan_id = self.env['mgmtsystem.plan'].browse(docids)

        company = self.env.user.company_id
        return {
            'doc_ids': self.ids,
            'company': company,
            'docs': training_plan_id,
        }
    
    