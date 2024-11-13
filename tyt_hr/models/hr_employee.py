from odoo import fields, models, api

class HrTytEmployeePrivate(models.Model):
    _name = "hr.employee.tyt_manager"
    _description = "Tipos de Jefe TYT"

    name = fields.Char(string='Nombre')


class HrEmployeePrivate(models.Model):
    _inherit = "hr.employee"

    tyt_manager_id = fields.Many2one('hr.employee.tyt_manager', string='Tipos de Jefe')

