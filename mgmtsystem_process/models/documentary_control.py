# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class DocumentaryControl(models.Model):
    _name = 'documentary.control'

    name = fields.Char(
        string='Nombre',
        required=True,
    )

    process_id = fields.Many2one(
        string='Procedimiento',
        comodel_name='mgmt.process',
        required=True,
        domain=[('active','=',True)]
    )
    department_id = fields.Many2one(
        string='Área responsable',
        comodel_name='hr.department',
        ondelete='restrict',
    )
    type_storage = fields.Selection(
        string='Tipo de almacenamiento',
        selection=[
            ('physical', 'Físico'),
            ('digital', 'Digital')],
        required=True,
        default='digital',
    )
    diffusion = fields.Boolean(
        string='Difusión',
        default=True,
    )
    type = fields.Selection(
        string='Tipo',
        selection=[
            ('interna', 'Interna'),
            ('externa', 'Externa')],
        required=True,
        default='interna',

    )

    process_code = fields.Char(
        string="Código de proceso",
        related='process_id.code',
        readonly=True,
        store=False
    )

    # process_last_edition = fields.Char(
    #     related='process_id.last_edition',
    #     readonly=True,
    #     store=True
    # )
    process_last_edition = fields.Char(
        compute='_compute_process_last_edition', string='Edición', readonly=True)
    process_approval_date = fields.Char(
        compute='_compute_process_approval_date', string='Fecha de aprobación', readonly=True)

    @api.depends('process_id')
    def _compute_process_last_edition(self):
        for each in self:
            edition_id = self.env['process.edition'].search(
                [('process_id', '=', each.process_id.id), ('state', '=', 'validate_ok'), ('active', '=', True)], limit=1)
            each.process_last_edition = edition_id.numero[-4:
                                                          ] if edition_id and edition_id.numero else ''

    @api.depends('process_id')
    def _compute_process_approval_date(self):
        for each in self:
            edition_id = self.env['process.edition'].search(
                [('process_id', '=', each.process_id.id), ('state', '=', 'validate_ok'), ('active','=', True)], limit=1)
            each.process_approval_date = edition_id.date_validate

    code = fields.Char(
        string='Código',
        copy=False,
    )

    @api.onchange('process_id')
    def _onchange_process_id(self):
        if not self.process_id:
            return
        next_number = len(self.env['documentary.control'].search(
            [('process_id', '=', self.process_id.id)]))
        self.code = ("%s-%s") % (self.process_id.code, str(next_number+1))

    @api.depends('action_id')
    def _compute_records_count(self):
        for record in self:
            if not record.action_id:
                record.records_count = 0
            else:
                action = record.action_id.read()[0] if record.action_id else ''
                domain = action['domain'] or []
                res = list(eval(str(domain)))
                number_record = len(
                    self.env[str(action['res_model'])].search(res))
                record.records_count = number_record

    _sql_constraints = [
        ('code_uniq', 'unique(code)', "¡Ya existe un registro con este código!"),
    ]

    # para filtrar
    module_id = fields.Many2one(
        string='App',
        comodel_name='ir.module.module',
        
    )

    @api.onchange('module_id')
    def _onchange_module_id(self):
        if not self.module_id:
            return
        module_name = self.module_id.name
        ids = []
        models = self.env['ir.model'].search([])
        for model in models:
            if module_name in model.modules:
                ids.append(model.id)
        self.model_id = False
        return {'domain': {'model_id': [('id', 'in', ids)]}}

    model_id = fields.Many2one(
        string='Modelo',
        comodel_name='ir.model',
        default=lambda self: self.model_id.model,
    )
    action_id = fields.Many2one(
        string='Acción',
        comodel_name='ir.actions.act_window',
        ondelete='restrict',
    )
    records_count = fields.Integer(
        string='# de registros',
        default=0,
        compute='_compute_records_count'
    )

    @api.onchange('model_id')
    def _onchange_model_id(self):
        if not self.model_id:
            return
        self.action_id = False
        return {'domain': {'action_id': [('res_model', '=', self.model_id.model)]}}

    def button_go(self):
        for record in self:
            if record.action_id:
                action = record.action_id.read()[0]
                return action


class DocumentPage(models.Model):
    _name = 'document.page' 
    _inherit = ['document.page', 'mgmtsystem.validation']

    def create_action(self, vuser_id):
        action = self.env.ref('hola_calidad.p_mail_activity_action').read()[0]
        self.env.cr.execute("""SELECT id FROM ir_model 
                          WHERE model = %s""", (str(self._name),))
        info = self.env.cr.dictfetchall()
        if info:
            model_id = info[0]['id']
        action['context'] = {
            'default_res_id': self.ids[0],
            'default_res_model': self._name,
            'default_res_model_id': model_id,
            'default_user_id': vuser_id,
        }
        return action
    
    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'document_page_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'document_page_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'document_page_validation_id', string='Validación')
    
class AuditPlanValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    document_page_elaboration_id = fields.Many2one(
        'document.page', string='Padre')
    document_page_review_id = fields.Many2one(
        'document.page', string='Padre')
    document_page_validation_id = fields.Many2one(
        'document.page', string='Padre')


class AttachmentClasification(models.Model):
    _name = 'ir.attachment.clasification'

    name = fields.Char(string='Nombre')
    description = fields.Text(string='Descripción')
    parent_id = fields.Many2one('ir.attachment.clasification', string='Padre')


class AttachmenteExtra(models.Model):
    _inherit = 'ir.attachment'

    author_id = fields.Many2one(comodel_name='res.users', string='Autor')
    language = fields.Char(string='Idioma')
    date = fields.Date(string='Fecha')
    version = fields.Char(string='Versión')
    clasification = fields.Many2one(
        comodel_name='ir.attachment.clasification', string='Clasificación')
