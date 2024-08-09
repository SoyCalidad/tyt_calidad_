from odoo import fields, models, api


class PlanLinePlace(models.Model):
    _name = "comunication.plan.line.place"
    _description = "Lugares de Plan de Comunicación"

    name = fields.Char(string='Nombre')

class PlanLineMedia(models.Model):
    _name = "comunication.plan.line.media"
    _description = "Medios de Comunicación de Planes de Comunicación"

    name = fields.Char(string='Nombre')

class PlanLine(models.Model):
    _inherit = "comunication.plan.line"

    user_id = fields.Many2many(
        string=u'Quién',
        comodel_name='res.users',
        #required=True,
    )
    
    frequency_text = fields.Char(string="Frecuencia")
    
    communication_target = fields.Char(string="Objetivo")
    communication_format = fields.Char(string="Formato")
    communication_place = fields.Many2one('comunication.plan.line.place', string='Lugar')
    communication_media = fields.Many2one('comunication.plan.line.media', string='Medio de Comunicación')
    responsible_in_id = fields.Many2one('hr.job', string='Responsable')


