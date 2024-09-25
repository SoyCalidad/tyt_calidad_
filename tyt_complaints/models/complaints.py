from odoo import fields, models, api


class StakeholderReq(models.Model):
    _inherit = 'complaint.complaint'


    claim_number = fields.Char(string='Número de reclamo')
    claim_reviewed_by = fields.Many2one(
        comodel_name='hr.employee', string='Reclamo revisado por:')
    claim_state = fields.Selection([
        ('reasonable', 'Razonable'),
        ('not_reasonable', 'No razonable'),
    ], string='Estado del reclamo')


    '''
    #name = fields.Char(string='Descripción') # Existe en el modelo original
    #legal_req = fields.Many2one(comodel_name='legal.legal', string='Requisito Legal') #"legal_id" Existe en el modelo original

    job_req = fields.Many2one(
        comodel_name='hr.job', string='Puesto Responsable')
    
    limit_date_req = fields.Char(string='Fecha límite')
    '''