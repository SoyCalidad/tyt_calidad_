from odoo import models, fields


class DocumentsDocument(models.Model):
    _inherit = 'documents.document'

    # Inverse links used only by the record rules (security/ir_rule.xml) to
    # know whether a document belongs to a risk control or process the user
    # can access. They are not shown in any view.
    tyt_rm_mo_file_ids = fields.One2many(
        comodel_name='tyt.risk.mo_file',
        inverse_name='file_id',
        string="Archivos de riesgos",
        copy=False,
    )
