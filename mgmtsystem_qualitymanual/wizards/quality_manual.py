from odoo import api, fields, models

class QualityManualReportWizard(models.TransientModel):
    _name = 'mgmt.quality_manual.report.wizard'
    
    
    quality_manual_id = fields.Many2one('mgmtsystem.qualitymanual', string='Manual de calidad', domain="[('state', '=', 'validate_ok')]", required=True)
    
    
    def action_print(self):
        data = self.read()[0]
        datas = {
            'data': data,
            'ids': self._ids,
            'model': 'mgmt.quality_manual.report.wizard',
            'res_model': 'mgmt.quality_manual.report.wizard',
            'qlty': self.quality_manual_id.id,
            'is_wizard': True,
        }
        return self.env.ref('mgmtsystem_qualitymanual.action_report_qualitymanual').report_action(self, data=datas)
    
