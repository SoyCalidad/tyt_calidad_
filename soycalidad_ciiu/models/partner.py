from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    fundation_date = fields.Date(string='Fecha de fundación')
    activity = fields.Char(string='Actividad')
    ciiu = fields.Char(string='Descripción CIUU')
    sector = fields.Selection([
        ('public', 'Público'),
        ('private', 'Privado'),
    ], string='Sector')
    employees_number = fields.Integer(string='N° de trabajadores')
    commercial_name = fields.Char(string='Nombre comercial')
