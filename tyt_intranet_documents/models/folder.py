# -*- coding: utf-8 -*-
from odoo import _, api, Command, fields, models
from odoo.exceptions import ValidationError


class DocumentFolder(models.Model):
    _inherit = 'documents.folder'

    is_intranet_folder = fields.Boolean(string='Is Intranet Folder', default=False)
