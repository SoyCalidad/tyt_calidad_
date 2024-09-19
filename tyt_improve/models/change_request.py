from odoo import fields, models, api
from odoo.exceptions import RedirectWarning, UserError, ValidationError
'''
class TrainingPlace(models.Model):
    _name = "soycalidad.change_request.clause"
    _description = "Cláusulas"

    name = fields.Char(string='Nombre')
'''

class ChangeRequest(models.Model):
    _inherit = 'soycalidad.change_request'

    hr_job_related_employee = fields.Many2one('hr.job', string='Puesto', related='employee_id.job_id', readonly=True, store=True)
    site_related_employee = fields.Many2one('hr.department', string='Sitio', related='employee_id.department_id', readonly=True, store=True)

    clause_narrative = fields.Char(string='Narrativa oficial de Cláusula')
    procedures_char = fields.Char(string='Procedimiento')
    clause_id = fields.Many2many('iso_9001.requirement', string='Cláusulas') ### change
    

    hr_job_related_user = fields.Many2one('hr.job', string='Puesto')
    site_related_user = fields.Many2one('hr.department', string='Departamento')

    '''
    @api.onchange('responsible_id')
    def _onchange_responsible(self):
        if self.responsible_id:
            employee = self.responsible_id.employee_ids[:1]
            if employee:
                self.hr_job_related_user = employee.job_id.id
                self.site_related_user = employee.department_id.id
            else:
                self.hr_job_related_user= False
                self.site_related_user = False
        else:
            self.hr_job_related_user = False
            self.site_related_user = False
    '''