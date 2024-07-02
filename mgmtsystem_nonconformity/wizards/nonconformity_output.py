from odoo import fields, models

class NonconformityOutputWizardReport(models.Model):
    _name = 'nonconformity_output.wizard_report'
    _description = 'Wizard de reporte de salidas no conformes'
    
    nonconformity_ids = fields.Many2many('mgmtsystem.nonconformity', string='No conformidades', domain='[("nc_output", "=", True)]')

    # Print report
    def print_report(self):
        self.ensure_one()
        nonconformity_ids = self.nonconformity_ids if self.nonconformity_ids else self.env['mgmtsystem.nonconformity'].search([("nc_output", "=", True)])
        return self.env.ref('mgmtsystem_nonconformity.action_report_nonconformity_output').report_action(nonconformity_ids)