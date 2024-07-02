from odoo import api, models, fields


class ProcessReportWizard2(models.TransientModel):
    _name = 'mgmt.process_2.report.wizard'
    _description = 'Wizard to print process report'

    categ_id = fields.Many2one('mgmt.categ', string='Proceso', required=True)

    def action_print(self):
        return self.env.ref('mgmtsystem_process_integration.action_report_general_process_xls').report_action(self.categ_id)
        
