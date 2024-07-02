from odoo import api, fields, models

class DMSFile(models.Model):
    _inherit = 'dms.file'

    language = fields.Char(string='Idioma')
    version = fields.Char(string='Versión')
    clasification = fields.Many2one(
        comodel_name='ir.attachment.clasification', string='Clasificación')
    url = fields.Char(string='URL')

class MailValidation(models.Model):
    _inherit = 'mgmtsystem.validation.mail'

    dms_document_ids = fields.Many2many('dms.file', string='Documentos')
    documents_count = fields.Integer(
        compute='_compute_documents_count', string='Documentos')

    def set_root_directory(self):
        directory = ''
        return directory


    @api.depends('dms_document_ids')
    def _compute_documents_count(self):
        for each in self:
            each.documents_count = len(each.dms_document_ids)

    def action_document_ids(self):
        result = self.env.ref(
            'dms.action_dms_file').read()[0]
        directory = self.set_root_directory()
        result['domain'] = [('id', 'in', self.dms_document_ids.ids)]
        result['context'] = {'default_directory_id': self.env.ref(directory).id}
        return result
