from odoo import fields,models,api, _
from ast import literal_eval

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    comunication_process_id = fields.Many2one('mgmt.process', string = 'Procedimiento para comunicación',related='company_id.comunication_process_id', domain=[('active','=',True)])
    record_meeting_line_approval = fields.Boolean(string='Recordar aprobación de lineas de reunión')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            record_meeting_line_approval=self.env['ir.config_parameter'].sudo().get_param('mgmtsystem_comunication.record_meeting_line_approval'),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('mgmtsystem_comunication.record_meeting_line_approval', self.record_meeting_line_approval)


class Company(models.Model):
    _inherit = 'res.company'

    comunication_process_id = fields.Many2one('mgmt.process', string = 'Procedimiento para comunicación', domain=[('active','=',True)])