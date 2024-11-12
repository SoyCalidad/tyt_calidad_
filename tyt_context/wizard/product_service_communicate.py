from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class ProductServiceCommunicate(models.Model):
    _name = 'tyt.product_service.communicate'
    _description = 'Product Service Communicate'

    name = fields.Char(string='Nombre')
    attachment_ids = fields.Many2many('ir.attachment', string='Adjuntos', copy=False)
    company_id = fields.Many2one('res.company', string='Compañía', default=lambda self: self.env.company)

    @api.constrains('attachment_ids')
    def _check_single_attachment(self):
        for record in self:
            if len(record.attachment_ids) > 1:
                raise ValidationError('Sólo puede adjuntar un archivo.')

    def action_communicate(self):
        self.ensure_one()
        template = self.env.ref('tyt_context.tyt_product_service_communicate_mail_template', raise_if_not_found=False)
        lang = self.env.context.get('lang')
        ctx = {
            'default_model': self._name,
            'default_res_id': self.ids[0],
            'default_use_template': bool(template),
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': 'mail.mail_notification_light',
            'force_email': True,
            'model_description': self.with_context(lang=lang).name,
        }
        if self.attachment_ids:
            ctx['default_attachment_ids'] = [(6, 0, self.attachment_ids.ids)]

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }
