from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ContextScopeHistory(models.Model):
    _inherit = 'process.edition.history'

    scope_id = fields.Many2one('tyt.context.scope', string='Alcance')


class ContextScope(models.Model):
    _name = 'tyt.context.scope'
    _inherit = ['mgmtsystem.validation.mail', 'mgmtsystem.code']
    _description = 'Alcance'
    _order = 'numero desc'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(
        string=u'Nombre',
        compute='_compute_name_code',
        search='_search_name',
        store=True
    )
    code = fields.Char(
        string='Referencia',
        default='Nuevo',
        compute='_compute_name_code',
        search='_search_code',
        store=True
    )

    def _search_name(self, operator, value):
        if operator == 'like':
            operator = 'ilike'
        return [('name', operator, value)]

    def _search_code(self, operator, value):
        if operator == 'like':
            operator = 'ilike'
        return [('code', operator, value)]

    sequence = fields.Integer('Secuencia', default=1, help='Se usa para ordenar.')
    process_id = fields.Many2one('mgmt.process', string='Proceso', domain=[('active', '=', True)])
    attachment_ids = fields.Many2many('ir.attachment', string='Archivos')
    attachments_count = fields.Integer(compute='_compute_attachments_count', string='Archivos')
    parent_edition = fields.Many2one(comodel_name='tyt.context.scope', string='Padre', copy=False)
    old_versions = fields.One2many(comodel_name='tyt.context.scope', string='Versiones antiguas',
                                   inverse_name='parent_edition', context={'active_version': False})
    version_as_string = fields.Char(string='Version', compute='_compute_version_as_string', store=True)
    change_history = fields.One2many('process.edition.history', 'scope_id',
                                     string='Historial de cambios', copy=True)

    tyt_objective_scope_users = fields.Html(string='Objectivo, alcance and usuarios')
    tyt_reference_documents = fields.Html(string='Documentos de referencia')
    tyt_procedure_scope_definition = fields.Html(string='Definicición de alcance del SGC')

    tyt_processes_activities = fields.Html(string='Procesos y actividades')
    tyt_products_services = fields.Html(string='Productos y servicios')
    tyt_organizational_units_and_functions = fields.Html(string='Unidades organizativas y funciones')
    tyt_locations = fields.Html(string='Ubicaciones')
    tyt_scope_exclusions = fields.Html(string='Exclusiones del alcance')
    tyt_iso_requirements_exclusions = fields.Html(string='Exclusiones de los requisitos de ISO 9001:2015')

    numero = fields.Char(
        string="Numero de secuencia",
        readonly=True,
        default='Sin definir',
        copy=False,
        store=True
    )

    sequence_id = fields.Many2one(
        string=u'Secuencia de ediciones',
        comodel_name='ir.sequence',
        related='process_id.sequence_id',
    )

    def _copy_edition(self):
        new_edition = self.copy({
            'version': self.version,
            'state': 'validate_ok',
            'deactivate_date': fields.Date.today(),
            'parent_edition': self.id,
        })
        return new_edition

    def button_new_version(self):
        self.ensure_one()
        self._copy_edition()
        revno = self.version
        self.write({
            'numero': 'Sin definir',
            'version': revno + 1,
            'state': 'elaborate',
            'name': self.name,
        })

    @api.depends('process_id', 'numero')
    def _compute_name_code(self):
        for record in self:
            if not record.process_id:
                record.name = ''
                record.code = ''
            record.name = record.process_id.name
            record.code = record.process_id.code

    def write(self, values):
        if values.get('numero', 'Sin definir') == 'Sin definir' and values.get('state', False) == 'validate_ok':
            values['numero'] = self.sequence_id.next_by_id() or 'Sin definir'
            values['name'] = self.process_id.name + ' ' + values.get('version_as_string', 'Sin definir')

        result = super().write(values)

        message = self.check_changes(values, "")
        if message != "":
            self.message_post(body=message)

        return result

    @api.depends('attachment_ids')
    def _compute_attachments_count(self):
        for each in self:
            count = len(each.attachment_ids)
            each.attachments_count = count

    def action_open_older_versions(self):
        result = self.env.ref(
            'tyt_context.tyt_context_scope_cancel_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result

    @api.depends('version')
    def _compute_version_as_string(self):
        for record in self:
            record.version_as_string = 'Versión N° {}'.format(str(record.version).rjust(3, '0'))

    def send_validate_ok(self):
        if not self.validation_users_check:
            raise ValidationError(
                'La validación no ha sido aprobada por los usuarios asignados')
        self.cancel_other_versions()
        self.write({
            'state': 'validate_ok',
        })
        validate_activity = self.activity_ids.filtered(
            lambda r: r.summary == 'Validación de documento')
        for validate in validate_activity:
            validate.action_done()
        self.write({})
        change_message = ''
        diff = ''
        related_fields = ['purpose', 'scope', 'references', 'body', 'flowchart',
                          'abbreviation_ids', 'responsable_ids', 'documentarycontrol_ids']
        if not self.old_versions:
            change_message += 'Versión Inicial'
            self.env['process.edition.history'].create({
                'name': change_message,
                'numero': self.numero,
                'scope_id': self.id,
                'publish_date': fields.Date.today(),
            })
        else:
            prev = self.old_versions[-1] if self.old_versions else None
            for other in self.old_versions:
                other.send_cancel()
            for field in related_fields:
                if prev:
                    diff = self.getDiff(prev.id, self.id, field)
                else:
                    diff = self.getDiff(False, self.id, field)
                change_message += diff
            self.env['process.edition.history'].create({
                'name': change_message,
                'numero': self.numero,
                'scope_id': self.id,
                'publish_date': self.date_validate,
            })

    @api.model
    def getDiff(self, v1, v2, field):
        text1 = v1 and getattr(self.browse(v1), field) or ''
        text2 = v2 and getattr(self.browse(v2), field) or ''
        if text1 == text2:
            return ''
        else:
            return 'Campo %s actualizado\n' % self._fields[field].string


    def check_changes(self, values, message):
        if values.get('state', False):
            state1 = dict(self._fields['state'].selection).get(
                self.state)
            state2 = dict(self._fields['state'].selection).get(
                values.get('state'))
            message = message + \
                _("<li>Estado: %s &rarr; %s</li>") % (state1, state2)

        if values.get('purpose', False):
            message = message + \
                _("<li><b>Objeto editado:</b></li> %s") % (values.get('purpose', ''))
        if values.get('scope', False):
            message = message + \
                _("<li><b>Alcance editado:</b></li> %s") % (values.get('scope', ''))
        if values.get('references', False):
            message = message + \
                _("<li><b>Referencia editado:</b></li> %s") % (values.get('references', ''))

        return message

    def send_context_scope_by_email(self):
        template = 'tyt_context.tyt_context_scope_mail_template'
        return self.notify_users_by_email(template)

