from odoo import api, fields, models


class mgmtsystemMof(models.Model):
    _name = 'mgmtsystem.mof'
    _inherit = ['mgmtsystem.validation.mail', 'mgmtsystem.code']
    _description = 'Manual de organización y funciones'

    name = fields.Char('Nombre', required=True)
    orgchart = fields.Html('Organigrama')
    importance = fields.Text('Importancia')
    target = fields.Html('Objetivo')
    legal_ids = fields.Many2many(
        'legal.legal', string='Base legal y normativa', relation='mof_legal_rel')
    validity = fields.Char('Vigencia')
    definition_ids = fields.Many2many(
        string='Definiciones y siglas', comodel_name='edition.abbreviation',)
    job_ids = fields.Many2many('hr.job', string='Puestos')

    resolution = fields.Boolean('Resolución')
    resolution_attachment_id = fields.Many2one(
        'ir.attachment', string='Adjuntar resolución')

    # Validation

    process_id = fields.Many2one('process.edition', string='Proceso')

    # Extras

    target_ids = fields.Many2many('mgmtsystem.target', string='Objetivos', relation='mof_target_rel')
    action_ids = fields.Many2many('mgmtsystem.action', string='Acciones', relation='mof_action_rel')
    nc_ids = fields.Many2many(
        'mgmtsystem.nonconformity', string='No conformidades', relation='mof_nc_rel')
    risk_ids = fields.Many2many(
        'matrix.block.line', string='Riesgos', domain="[('type','=','risk')]", relation='risk_mof_rel')
    opp_ids = fields.Many2many(
        'matrix.block.line', string='Oportunidades', domain="[('type','=','opportunity')]", relation='opp_mof_rel')
    change_request_ids = fields.Many2many(
        'soycalidad.change_request', string='Solicitudes de cambio', relation='mof_change_request_rel')

    # Computed

    target_count = fields.Integer(
        compute='_compute_extras_count', string='Cantidad de objetivos')
    action_count = fields.Integer(
        compute='_compute_extras_count', string='Cantidad de acciones')
    nc_count = fields.Integer(
        compute='_compute_extras_count', string='Cantidad de no conformidades')
    risk_count = fields.Integer(
        compute='_compute_extras_count', string='Cantidad de riesgos')
    opp_count = fields.Integer(
        compute='_compute_extras_count', string='Cantidad de oportunidades')
    change_request_count = fields.Integer(
        compute='_compute_extras_count', string='Solicitudes de cambio')

    @api.depends('change_request_ids')
    def _compute_change_requests_count(self):
        for each in self:
            each.change_requests_count = len(each.change_request_ids)

    @api.depends('target_ids', 'action_ids', 'nc_ids', 'risk_ids', 'opp_ids')
    def _compute_target_count(self):
        for record in self:
            record.target_count = len(record.target_ids)
            record.action_count = len(record.action_ids)
            record.nc_count = len(record.nc_ids)
            record.risk_count = len(record.risk_ids)
            record.opp_count = len(record.opp_ids)
            record.change_request_count = len(record.change_request_ids)

    # DMS

    dms_document_ids = fields.Many2many('dms.file', string='Documentos')
    documents_count = fields.Integer(
        compute='_compute_documents_count', string='# Documentos')

    def set_root_directory(self):
        directory = 'soycalidad_dms.directory_pro'
        return directory

    @api.depends('dms_document_ids')
    def _compute_documents_count(self):
        for each in self:
            each.documents_count = len(each.dms_document_ids)

    # Validación
    
    parent_edition = fields.Many2one(
        comodel_name='mgmtsystem.mof', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='mgmtsystem.mof', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'mgmtsystem_mof_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'mgmtsystem_mof_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'mgmtsystem_mof_validation_id', string='Validación')

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_employees.mgmtsystem_mof_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result


class MOFValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    mgmtsystem_mof_elaboration_id = fields.Many2one(
        'mgmtsystem.mof', string='Padre (Elaboración)')
    mgmtsystem_mof_review_id = fields.Many2one(
        'mgmtsystem.mof', string='Padre (Revisión)')
    mgmtsystem_mof_validation_id = fields.Many2one(
        'mgmtsystem.mof', string='Padre (Validación)')
