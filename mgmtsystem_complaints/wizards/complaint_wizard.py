from odoo import api, fields, models


class ComplaintWizard(models.TransientModel):
    _name = 'complaint.wizard.report'
    _inherit = 'mgmtsystem.code'
    _description = 'Lista de reclamos'

    date_init = fields.Datetime(string='Fecha inicial')
    date_end = fields.Datetime(string='Fecha final')

    def action_print(self):
        complaint_ids = self.env['complaint.complaint'].search(
            [('date_incident', '>=', self.date_init), ('date_incident', '<=', self.date_end)])
        return self.env.ref('mgmtsystem_complaints.action_report_complaints').report_action(complaint_ids)



    
