from odoo import models, api, fields

class MaintanancePlanWizard(models.TransientModel):
    _name = 'maintance.plan.wizard'
    
    maintenance_plan_id = fields.Many2one('mgmtsystem.maintenance.plan', string='Programa de mantenimientos')
    
    def action_print(self):
        id = self.maintenance_plan_id.id
        data = self.read()[0]
        datas = {
            'data': data,
            'ids': self._ids,
            'model': 'maintance.plan.wizard',
            'res_model': 'maintance.plan.wizard',
            'is_wizard': True,
            'id': id,
        }
        return self.env.ref('mgmtsystem_infrastructure.reporte_plan_infrastructure').report_action(self, data=datas)
    
    
class MaintanancePlanReport(models.AbstractModel):
    _name = 'report.mgmtsystem_infrastructure.maintance_plan_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data and data.get('is_wizard'):
            maintenance_plan_id = self.env['mgmtsystem.maintenance.plan'].browse(data['id'])
        else:
            maintenance_plan_id = self.env['mgmtsystem.maintenance.plan'].browse(docids)

        company = self.env.user.company_id
        return {
            'doc_ids': self.ids,
            'company': company,
            'docs': maintenance_plan_id,
        }
