# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class MgmtCategType(models.Model):
    _name = 'mgmt.categ.type'
    _description = 'Tipo de proceso'
    _order = 'sequence asc, weight asc'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string='Nombre')
    code = fields.Char(string='Código')
    description = fields.Text(string='Descripción')
    sequence = fields.Integer('Secuencia', default=1,
                              help="Se usa para ordenar.")
    weight = fields.Integer(
        string='Peso', help='Se ordenará de mayor a menor', default=1, required=True)


class MgmtCateg(models.Model):
    _name = 'mgmt.categ'
    _inherit = ['mgmtsystem.validation.mail']
    _description = "Proceso"
    _order = 'sequence asc, type, name'

    name = fields.Char(
        string=u'Nombre',
        required=True
    )
    active = fields.Boolean('Active', default=True, tracking=True)
    type = fields.Many2one(
        'mgmt.categ.type', string='Tipo de proceso', group_expand='_read_group_type', required=True)
    code = fields.Char(
        string=u'Código',
    )
    sequence = fields.Integer('Secuencia', default=1,
                              help="Se usa para ordenar.")
    description = fields.Text(
        string=u'Descripción',
    )
    comments = fields.Text(string='Comentarios')
    process_ids = fields.One2many(
        string=u'Procedimientos asociados',
        comodel_name='mgmt.process',
        inverse_name='categ_id',
        domain=[('active','=',True)]
    )

    color = fields.Integer('Color')

    reference = fields.Text(compute='_compute_reference', string='Referencia')

    attachment_ids = fields.Many2many('ir.attachment', string='Archivos')

    attachments_count = fields.Integer(
        compute='_compute_attachments_count', string='Archivos')

    @api.depends('attachment_ids')
    def _compute_attachments_count(self):
        for each in self:
            count = len(each.attachment_ids)
            each.attachments_count = count

    @api.model
    def _read_group_type(self, stages, domain, order):
        type_ids = self.env['mgmt.categ.type'].search([], order='weight asc')
        return type_ids

    @api.depends('process_ids')
    def _compute_reference(self):
        reference = ''
        for p in self.process_ids:
            document = self.env['process.edition'].search([
                ('process_id', '=', p.id),
                ('state', '=', 'validate_ok'),
                ('active', '=', True)
            ], order='numero desc', limit=1)
            if document and document.references:
                references = ', '.join([x.name for x in document.references])
                reference += references + '\n'
        self.reference = reference

    def write(self, values):
        message = ""

        if values.get('name', False):
            message = message + _("<li>Se cambió el nombre: %s &rarr; %s</li>") % (self.name,
                                                                                   values.get('name', ''))
        if values.get('type', False):
            type_ = self.env['mgmt.categ.type']
            # dict(self._fields['type'].selection).get(self.type)
            vtype1 = self.type.name
            # dict(self._fields['type'].selection).get(values.get('type'))
            vtype2 = type_.browse(values.get('type')).name
            message = message + \
                _("<li>Se cambió el tipo: %s &rarr; %s</li>") % (vtype1, vtype2)
        if values.get('code', False):
            message = message + \
                _("<li>Se cambió el código: %s &rarr; %s</li>") % (self.code,
                                                                   values.get('code', ''))

        result = super(MgmtCateg, self).write(values)

        if message != "":
            self.message_post(body=message)

        return result

    def open_form_view(self):
        view_id = self.env.ref('mgmtsystem_process.mgmt_categ_form').id
        context = self._context.copy()
        active_id = self.env.context.get('active_id')
        print(active_id)
        return {
            'name': 'Conclusiones y recomendaciones',
            'view_type': 'form',
            'view_mode': 'tree',
            'views': [(view_id, 'form')],
            'res_model': 'mgmt.categ',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'res_id': active_id,
            'target': 'current',
            'context': context,
        }

    def open_attachment_ids(self):
        """Método para abrir la lista de documentos
        """
        result = self.env.ref(
            'knowledge.knowledge_action_documents').read()[0]
        result['domain'] = [('id', 'in', self.attachment_ids.ids)]
        return result

    def print_report(self):
        return self.env.ref('mgmtsystem_process.report_mgmt_categ').report_action(self)


class Process(models.Model):
    _name = 'mgmt.process'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Procedimiento"
    _order = 'type'

    name = fields.Char(
        string=u'Nombre del procedimiento',
        required=True,
    )
    active = fields.Boolean('Active', default=True, tracking=True)
    type = fields.Many2one(
        'mgmt.categ.type', string='Tipo de proceso', group_expand='_read_group_type', required=True,)
    type_id = fields.Integer(
        related='type.id'
    )
    categ_id = fields.Many2one(
        string=u'Proceso',
        comodel_name='mgmt.categ',
        required=True,
        ondelete='restrict',
        domain="[('type.id','=',type_id)]"
    )
    responsible_id = fields.Many2many(
        'hr.job',
        string='Responsable',
        relation='job_responsible_process_rel'
    )
    related_employees_ids = fields.Many2many(
        'hr.job', string='Puestos relacionados', relation='job_related_process_rel')

    documentarycontrol_ids = fields.One2many(
        string='Registro Lista maestra',
        comodel_name='documentary.control',
        inverse_name='process_id',
    )

    @api.model
    def _read_group_type(self, stages, domain, order):
        type_ids = self.env['mgmt.categ.type'].search([])
        return type_ids

    @api.onchange('categ_id')
    def _onchange_categ_id(self):
        if not self.categ_id:
            return None
        self.type = self.categ_id.type
        if self.type and self.categ_id:
            # type = dict(self._fields['type'].selection).get(self.type)
            type = self.type.code
            code = self.categ_id.code if self.categ_id.code else self.categ_id.name[:2]
            qty = len(self.categ_id.process_ids) + 1
            self.code = _("%s-%s-%s") % (type, code, '0' + str(qty))

    sequence_id = fields.Many2one(
        string=u'Secuencia de ediciones',
        comodel_name='ir.sequence',
        ondelete='restrict',
    )
    code = fields.Char(
        string=u'Código',
    )

    _sql_constraints = [
        ('code_uniq', 'unique(code)', "¡Ya existe un registro con este código!"),
    ]

    last_edition = fields.Html(
        string=u'Edición vigente',
        compute='_compute_last_edition',
    )

    real_last_edition = fields.Many2one(
        comodel_name='process.edition',
        string='Última edición',
        compute='_compute_last_edition',
    )
    validate_date = fields.Date(
        compute='_compute_last_edition', string='Fecha de vigencia')

    @api.depends('name')
    def _compute_last_edition(self):
        for record in self:
            document = self.env['process.edition'].search([
                ('process_id', '=', record.id),
                ('active', '=', True)
            ], order='numero desc', limit=1)
            if document:
                if str(document.id).isdigit():
                    record.real_last_edition = document.id
                record.last_edition = _("<a data-oe-id=%s data-oe-model='process.edition' href=#id=%s&model=process.edition>%s</a>") % (
                    document.id, document.id, document.numero,)
                record.validate_date = document.date_validate
            else:
                record.last_edition = 'No existe edición vigente'
                record.real_last_edition = None
                record.validate_date = None

    def action_view_editions(self):
        for record in self:
            action = self.env.ref(
                'document_page_procedure.action_procedures').read()[0]
            documents = self.env['process.edition'].search(
                [('process_id', '=', record.id)])
            if len(documents) > 1:
                action['domain'] = [('id', 'in', documents.ids)]
            elif documents:
                action['views'] = [
                    (self.env.ref('document_page.view_wiki_form').id, 'form')]
                action['res_id'] = documents.id
            return action

    @api.model
    def create(self, values):
        sequence = self.env['ir.sequence'].create({
            'name': 'Secuencia de '+values.get('name'),
            'active': True,
            'prefix': 'Edición-nro.',
            'padding': 4,
            'number_next': 1,
            'number_increment': 1,
        })
        values['sequence_id'] = sequence.id
        result = super(Process, self).create(values)
        return result

    @api.onchange('type')
    def _onchange_type(self):
        if not self.type:
            return
        if self.categ_id.type != self.type:
            self.categ_id = False
        return {
            'domain': {
                'categ_id': [('type', '=', self.type.id)]
            }
        }

    def write(self, values):
        message = ""
        if values.get('name', False):
            message = message + \
                _("<li>Se cambió el nombre: %s &rarr; %s</li>") % (self.name,
                                                                   values.get('name', ''))
        if values.get('type', False):
            type_ = self.env['mgmt.categ.type']
            vtype1 = self.type.name
            vtype2 = type_.browse(values.get('type')).name
            message = message + \
                _("<li>Se cambió el tipo: %s &rarr; %s</li>") % (vtype1, vtype2)
        if values.get('categ_id', False):
            categ = self.env['mgmt.categ'].browse(values.get('categ_id'))
            message = message + \
                _("<li>Se cambió la categoría: %s &rarr; %s</li>") % (self.categ_id.name, categ.name)
        if values.get('code', False):
            message = message + \
                _("<li>Se cambió el código: %s &rarr; %s</li>") % (self.code,
                                                                   values.get('code', ''))

        result = super(Process, self).write(values)

        if message != "":
            self.message_post(body=message)

        return result

    def show_process_editions(self):
        result = self.env.ref(
            'mgmtsystem_process.action_mgmt_process_edition').read()[0]
        result['context'] = {'default_process_id': self.id,
                             'search_default_process_id': self.id}
        return result


class Purchase(models.Model):
    _inherit = 'purchase.order'

    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])


class Employee(models.Model):
    _inherit = 'hr.employee'

    related_process_ids = fields.Many2many(
        'mgmt.process', string='Asignados', relation='emp_related_process_rel')
    responsible_process_ids = fields.Many2many(
        'mgmt.process', string='Responsables', relation='responsible_process_rel')


class Job(models.Model):
    _inherit = 'hr.job'

    related_process_ids = fields.Many2many(
        'mgmt.process', string='Asignados', relation='job_related_process_rel')
    responsible_process_ids = fields.Many2many(
        'mgmt.process', string='Responsables', relation='job_responsible_process_rel')
