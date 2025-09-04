from odoo import _, api, fields, models


class Document(models.Model):
    _inherit = 'documents.document'

    short_name = fields.Char(string='Short Name')
    is_intranet_folder = fields.Boolean(string='Is Intranet Folder', default=False)

