from odoo import api, fields, models

class Process(models.Model):
    _inherit = 'process.edition'

    references = fields.Many2many(
        comodel_name='legal.legal', 
        string='Referencias normativas',
        relation="processedition_ref_rel",
    )

class ProcessTemplate(models.Model):
    _inherit = 'process.edition.template'

    references = fields.Many2many(
        comodel_name='legal.legal', 
        string='Referencias normativas',
        relation="editiontemplate_ref_rel",
    )