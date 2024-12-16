from odoo import api, fields, models

class ProcessEditionReportWizard(models.TransientModel):
    _name = 'mgmt.process_edition.report.wizard'
    
    
    process_edition_id = fields.Many2one('process.edition', string='Versión de proceso', required=True)