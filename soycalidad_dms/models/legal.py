from odoo import api, fields, models


class LegalPlan(models.Model):
    _inherit = 'legal.plan'

    def set_root_directory(self):
        directory = 'soycalidad_dms.directory_legal'
        return directory


class LegalLegal(models.Model):
    _inherit = 'legal.legal'

    dms_document_ids = fields.Many2many('dms.file', string='Documentos')
    documents_count = fields.Integer(
        compute='_compute_documents_count', string='Documentos')

    def set_root_directory(self):
        directory = 'soycalidad_dms.directory_legal'
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
        result['context'] = {
            'default_directory_id': self.env.ref(directory).id}
        return result
