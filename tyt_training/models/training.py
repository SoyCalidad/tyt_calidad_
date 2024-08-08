from odoo import fields, models, api

class TrainingPlace(models.Model):
    _name = "mgmtsystem.plan.training.place"
    _description = "Lugares de Capacitación"

    name = fields.Char(string='Nombre')

class TrainingMedia(models.Model):
    _name = "mgmtsystem.plan.training.media"
    _description = "Medios de Comunicación de Capacitaciones"

    name = fields.Char(string='Nombre')

'''
# Link "res.partner" with "hr.job", 
    # (necesario para que "exponent_job_id" retorne valores if "exponent_record._name == 'res.partner'")

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    custom_job_id = fields.Many2one('hr.job', string='Custom Job Position')
'''
class Training(models.Model):
    _inherit = "mgmtsystem.plan.training"
    
    responsible_in_id = fields.Many2one('hr.job', string='Responsable')

    exponent_job_id = fields.Many2one(
        comodel_name='hr.job',
        string='Puesto del Expositor',
        compute='_compute_exponent_job_id',
        store=True
    )

    training_frequency = fields.Char(string="Frecuencia")
    date_training = fields.Char(string="Fecha")
    training_target = fields.Text(string="Objetivo")
    training_format = fields.Char(string="Formato")

    training_place = fields.Many2one(
        string="Lugar",
        comodel_name='mgmtsystem.plan.training.place',
    )
    training_media = fields.Many2one(
        string="Medio de Comunicación",
        comodel_name='mgmtsystem.plan.training.media',
    )    

    @api.depends('exponent_id')
    def _compute_exponent_job_id(self):
        for record in self:
            job_id = False
            if record.exponent_id:
                exponent_record = record.exponent_id
                if exponent_record._name == 'hr.employee':
                    job_id = exponent_record.job_id.id
            record.exponent_job_id = job_id

    '''
    # link exponent_id with res.partner.custom_job_id
    @api.depends('exponent_id')
    def _compute_exponent_job_id(self):
        for record in self:
            job_id = False
            if record.exponent_id:
                exponent_record = record.exponent_id
                if exponent_record._name == 'hr.employee':
                    job_id = exponent_record.job_id.id
                # devuelve valores if record.exponent_id._name == 'res.partner'      
                elif exponent_record._name == 'res.partner':
                    job_id = exponent_record.custom_job_id.id
            record.exponent_job_id = job_id
    '''