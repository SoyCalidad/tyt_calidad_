from odoo import fields, models, api


class StakeholderReq(models.Model):
    _inherit = 'mgmtsystem.stakeholder.req'


    target_req = fields.Char(string='Objetivo')
    #name = fields.Char(string='Descripción') # Existe en el modelo original
    #legal_req = fields.Many2one(comodel_name='legal.legal', string='Requisito Legal') #"legal_id" Existe en el modelo original

    job_req = fields.Many2one(
        comodel_name='hr.job', string='Puesto Responsable')
    
    limit_date_req = fields.Char(string='Fecha límite')
    

class Stakeholder(models.Model):
    _inherit = 'mgmtsystem.stakeholder'

    mgmt_process = fields.Many2one('mgmt.process', string="Procedimiento/Proceso/Actividad Relacionado")