from odoo import models, fields, api 


class User(models.Model):
    _inherit = "res.users"

    process_ids = fields.Many2many(
        comodel_name='tyt.business.process',
        string="Acceso a Processos",
        
    )