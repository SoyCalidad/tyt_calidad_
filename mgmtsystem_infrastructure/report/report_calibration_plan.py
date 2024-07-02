from odoo import models, api, fields

class MaintanancePlanWizard(models.TransientModel):
    _name = 'calibration.plan.wizard'
    
    calibration_plan_id = fields.Many2one('mgmtsystem.calibration.plan', string='Programa de calibraciones')
    
    def action_print(self):
        id = self.calibration_plan_id.id
        data = self.read()[0]
        datas = {
            'data': data,
            'ids': self._ids,
            'model': 'calibration.plan.wizard',
            'res_model': 'calibration.plan.wizard',
            'is_wizard': True,
            'id': id,
        }
        return self.env.ref('mgmtsystem_infrastructure.action_calibration_plan_report').report_action(self, data=datas)
    
    
class MaintanancePlanReport(models.AbstractModel):
    _name = 'report.mgmtsystem_infrastructure.calibration_plan_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data and data.get('is_wizard'):
            calibration_plan_id = self.env['mgmtsystem.calibration.plan'].browse(data['id'])
        else:
            calibration_plan_id = self.env['mgmtsystem.calibration.plan'].browse(docids)

        company = self.env.user.company_id
        return {
            'doc_ids': self.ids,
            'company': company,
            'docs': calibration_plan_id,
        }
