import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class TYTDistributionList(models.Model):
    _name = 'tyt.distribution.list'
    _description = 'TYT Distribution List'
    _rec_name = 'distributed_to'

    edition_id = fields.Many2one(
        comodel_name='process.edition',
        string='Edition',
        required=True
    )
    
    number_of_copy= fields.Integer(
        string='Number of copy',
    )
    distributed_to = fields.Many2one(
        comodel_name='hr.employee',
        string='Distributed to'
    )
    job_id = fields.Many2one(
        comodel_name='hr.job',
        string='Job',
        related="distributed_to.job_id"
    )
    distribution_date = fields.Date(
        string='Distribution Date',
        default=fields.Date.today
    )
    place = fields.Char(
        string='Place',
    )
    
class TYTDocumentRecord(models.Model):
    _name = 'tyt.document.record'
    _description = 'TYT Document Record'
    
    edition_id = fields.Many2one(
        comodel_name='process.edition',
        string='Edition',
        required=True
    )
    
    prefix = fields.Char(
        string='Prefix',
    )
    name = fields.Char(
        string='Name',
    )
    responsible = fields.Char(
        string='Responsible',
    )
    location = fields.Char(
        string='Location',
    )
    

class ProcedureEdition(models.Model):
    _inherit = 'process.edition'
    
    tyt_distribution_list_ids = fields.One2many(
        comodel_name='tyt.distribution.list',
        inverse_name='edition_id',
        string='Distribution Lists',
        copy=True
    )
    
    tyt_objective_scope_users = fields.Html(
        string='Objective, Scope and Users',
    )
    tyt_reference_documents = fields.Html(
        string='Reference Documents',
    )
    tyt_procedure_description = fields.Html(
        string='Procedure Description',
    )
    tyt_document_record_ids = fields.One2many(
        'tyt.document.record',
        'edition_id',
        string='Management of Records Kept Based on This Document',
    )
    tyt_appendices = fields.Html(
        string='Appendices',
    )

    #### Change String : Edición to Versión #####

    @api.depends('version')
    def _compute_version_as_string(self):
        for record in self:
            record.version_as_string = 'Versión N° {}'.format(str(record.version).rjust(3, '0'))
