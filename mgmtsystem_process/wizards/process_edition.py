from odoo import api, fields, models

class ProcessEditionReportWizard(models.TransientModel):
    _name = 'mgmt.process_edition.report.wizard'
    
    
    process_edition_id = fields.Many2one('process.edition', string='Edición de proceso', required=True)
    
    
    def action_print(self):
        id = self.process_edition_id.id
        data = self.read()[0]
        datas = {
            'data': data,
            'ids': self._ids,
            'model': 'mgmt.process_edition.report.wizard',
            'res_model': 'mgmt.process_edition.report.wizard',
            'id': id,
        }
        return self.env.ref('mgmtsystem_process.report_process_edition').report_action(self, data=datas)
    
