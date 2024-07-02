from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class DocumentaryControl(models.Model):
    _inherit = 'documentary.control'

    process_id = fields.Many2one(
        string='Procedimiento',
        comodel_name='mgmt.process',
        required=False,
        domain=[('active','=',True)])
    config_type = fields.Selection([
        ('model', 'Modelo'),
        ('document', 'Documento'),
    ], string='Tipo', default='model')
    #document_id = fields.Many2one('dms.file', string='Documento')

    def update_codes_from_documentary_control(self):
        for each in self:
            if not each.model_id:
                raise ValidationError(
                    _('No se puede actualizar los códigos de los documentos sin un modelo'))
            if not each.code:
                raise ValidationError(
                    _('No se puede actualizar los códigos de los documentos sin un código'))
            try:
                records = each.env[each.model_id.model].search([])
                for record in records:
                    record.old_code = record.code or ''
                    record.code = each.code
            except:
                pass

    @api.onchange('process_id')
    def _onchange_process_id(self):
        if not self.process_id:
            return
        next_number = len(self.env['documentary.control'].search(
            [('process_id', '=', self.process_id.id)]))
        self.code = ("%s-%s") % (self.process_id.code, str(next_number+1))
