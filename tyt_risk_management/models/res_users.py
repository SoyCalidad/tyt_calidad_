from odoo import models, fields, api 


class User(models.Model):
    _inherit = "res.users"

    process_ids = fields.Many2many(
        comodel_name='tyt.business.process',
        string="Acceso a Processos",
        
    )
    
    tyt_rm_user_type = fields.Selection(
        selection=[
            ('internal', 'Interno'),
            ('portal', 'Portal'),
            ('public', 'Público'),
        ],
        string='Tipo de Usuario',
        compute='_compute_user_type',
        store=True,  # permite filtrar/ordenar por esta columna en listas
    )
 
    @api.depends('groups_id')
    def _compute_user_type(self):
        for user in self:
            if user.has_group('base.group_user'):
                user.tyt_rm_user_type = 'internal'
            elif user.has_group('base.group_portal'):
                user.tyt_rm_user_type = 'portal'
            else:
                user.tyt_rm_user_type = 'public'
