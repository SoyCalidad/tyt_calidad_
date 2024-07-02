from odoo import api, fields, models


class CRMLead(models.Model):
    _inherit = 'crm.lead'

    document_ids = fields.Many2many('dms.file', string='Documentos')
    documents_count = fields.Integer(
        compute='_compute_documents_count', string='Documentos')

    main_tag_id = fields.Many2one(
        'crm.lead.tag', compute='_compute_main_tag_id', string='Tag principal', store=True)

    commercial_name = fields.Char(
        string='Nombre comercial', related='partner_id.commercial_name')

    state_id = fields.Many2one('res.country.state', 'Departamento',
                                  domain="[('country_id', '=', country_id),('state_id', '=', False),('province_id', '=', False)]")

    @api.depends('tag_ids')
    def _compute_main_tag_id(self):
        for each in self:
            each.main_tag_id = each.tag_ids[0].id if each.tag_ids else None

    @api.depends('document_ids')
    def _compute_documents_count(self):
        for each in self:
            each.documents_count = len(each.document_ids)

    def action_document_ids(self):
        result = self.env.ref(
            'dms.action_dms_file').read()[0]
        result['domain'] = [('id', 'in', self.document_ids.ids)]
        result['context'] = {'default_directory_id': self.env.ref(
            'soycalidad_crm.directory_crm').id}
        return result
