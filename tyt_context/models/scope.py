from odoo import fields, models, api


class ContextScope(models.Model):
    _name = 'tyt.context.scope'
    _inherit = ['mgmtsystem.validation.mail', 'mgmtsystem.code']
    _description = 'Alcance'
    _order = 'sequence asc'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string='Nombre')
    code = fields.Char(string='Código')
    sequence = fields.Integer('Secuencia', default=1, help='Se usa para ordenar.')
    process_id = fields.Many2one(
        'mgmt.process', string='Proceso', domain=[('active', '=', True)])

    attachment_ids = fields.Many2many('ir.attachment', string='Archivos')
    attachments_count = fields.Integer(compute='_compute_attachments_count', string='Archivos')

    parent_edition = fields.Many2one(comodel_name='tyt.context.scope', string='Padre', copy=False)
    old_versions = fields.One2many(
        omodel_name='tyt.context.scope', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    @api.depends('attachment_ids')
    def _compute_attachments_count(self):
        for each in self:
            count = len(each.attachment_ids)
            each.attachments_count = count


    def action_open_older_versions(self):
        result = self.env.ref(
            'tyt_context.tyt_context_scope_cancel_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result
