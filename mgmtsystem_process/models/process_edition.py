# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError
import difflib


class EconomicActiviy(models.Model):
    _name = 'res.economy.activity'

    name = fields.Char(string='Nombre')
    description = fields.Text(string='Descripción')


class Company(models.Model):
    _inherit = 'res.company'

    economic_activity_id = fields.Many2one(
        comodel_name='res.economy.activity', string='Actividad económica')
    economic_activity_name = fields.Char(
        related='economic_activity_id.name', string="Actividad económica")


class LineResponsable(models.Model):
    _name = 'edition.responsable.line'
    _description = 'Linea de responsable y descripción'

    name = fields.Char(
        string='Nombre',
    )
    job_id = fields.Many2one(
        string='Puesto de empleado',
        comodel_name='hr.job',
        ondelete='cascade',
    )
    description = fields.Text(
        string='Descripción',
    )


class ProcessEditionResponsible(models.Model):
    _name = 'process.edition.responsible'
    _description = 'Responsable del procedimiento'

    name = fields.Char(string='Nombre')
    description = fields.Text(string='Descripción')
    edition_id = fields.Many2one(
        'process.edition', string='Edición del procedimiento', domain=[('active','=',True)])


class Abbreviation(models.Model):
    _name = 'edition.abbreviation'
    _description = "Definición o abreviaturas"

    abbre = fields.Char(string='Abreviatura')
    name = fields.Char(
        string='Nombre',
        required=True,
    )
    description = fields.Text(
        string='Descripción',
        required=True,
    )


class EditionTemplate(models.Model):
    _name = 'process.edition.template'
    _description = "Plantillas de edición de procedimiento"

    name = fields.Char(
        string=u'Nombre',
        required=True
    )
    purpose = fields.Html(
        string='Objeto',
    )
    scope = fields.Html(
        string='Alcance',
    )
    references = fields.Html(
        string='Referencias',
    )
    body = fields.Html(
        string=u'Desarrollo',
        required=True,
    )
    flowchart = fields.Html(
        string='Flujograma',
    )
    custom = fields.Boolean(string='Es personalizado')
    custom_body = fields.Text(string='Contenido')

    def _default_company(self):
        return self.env.user.company_id

    company_id = fields.Many2one(
        'res.company',
        'Compañia',
        default=_default_company,
    )

    def _default_economic_activity(self):
        if self.company_id:
            return self.company_id.economic_activity_id
        else:
            return None

    economic_activity_id = fields.Many2one(
        comodel_name='res.economy.activity', string='Actividad económica', default=_default_economic_activity)
    economic_activity_name = fields.Char(
        related='economic_activity_id.name', string="Actividad económica")


class ProcessEdition(models.Model):
    _name = 'process.edition'
    _inherit = 'mgmtsystem.validation.mail'
    _description = 'Edición de procedimiento'
    _order = 'numero desc'

    parent_edition = fields.Many2one(
        comodel_name='process.edition', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='process.edition', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    name = fields.Char(
        string=u'Nombre',
        compute='_compute_name_code',
        default='Sin nombre',
        search='_search_name',
    )
    active = fields.Boolean('Active', default=True, tracking=True)
    categ_id = fields.Many2one(
        related='process_id.categ_id', string='Proceso', store='True')
    type_id = fields.Many2one(
        related='process_id.type', string='Tipo de proceso')

    def _default_company(self):
        return self.env.user.company_id

    company_id = fields.Many2one(
        'res.company',
        'Compañia',
        default=_default_company,
    )

    def _default_economic_activity(self):
        if self.company_id:
            return self.company_id.economic_activity_id
        else:
            return None

    economic_activity_id = fields.Many2one(
        comodel_name='res.economy.activity', string='Actividad económica', default=_default_economic_activity)
    economic_activity_name = fields.Char(
        related='economic_activity_id.name', string="Actividad económica")

    @api.depends('process_id', 'numero')
    def _compute_name_code(self):
        for record in self:
            if not record.process_id:
                record.name = ''
                record.code = ''
            record.name = record.process_id.name
            record.code = record.process_id.code

    code = fields.Char(
        string='Referencia',
        default='Nuevo',
        compute='_compute_name_code',
        search='_search_code',
    )

    numero = fields.Char(
        string="Numero de secuencia",
        readonly=True,
        required=True,
        default='Sin definir',
        copy=False,
    )

    version_as_string = fields.Char(
        string='Version',
        compute='_compute_version_as_string',
    )
    
    @api.depends('version')
    def _compute_version_as_string(self):
        for record in self:
            record.version_as_string = 'Edición N° {}'.format(str(record.version).rjust(3, '0'))

    process_id = fields.Many2one(
        string=u'Procedimiento',
        comodel_name='mgmt.process',
        required=True,
        ondelete='restrict',
        domain=[('active','=',True)]
    )
    documentarycontrol_ids = fields.One2many(
        related='process_id.documentarycontrol_ids',
    )

    sequence_id = fields.Many2one(
        string=u'Secuencia de ediciones',
        comodel_name='ir.sequence',
        related='process_id.sequence_id',
    )

    purpose = fields.Text(
        string='Objeto',
        tracking=True,
    )
    scope = fields.Text(
        string='Alcance',
        tracking=True,
    )
    references = fields.Text(
        string='Referencias',
        tracking=True,
    )
    body = fields.Text(
        string='Desarrollo',
        tracking=True,
    )
    responsable_ids = fields.Many2many(
        string='Responsables',
        comodel_name='edition.responsable.line',
        relation='edition_responsable_line_rel_',
        column1='edition_id',
        column2='responsable_line_id',
        tracking=True,
    )
    responsible_ids = fields.One2many(
        'process.edition.responsible', 'edition_id', string='Responsables', tracking=True,)
    abbreviation_ids = fields.Many2many(
        string='Definición o abreviaturas',
        comodel_name='edition.abbreviation',
        relation='edition_page_abbreviation_rel_',
        column1='edition_id',
        column2='abbreviation_id',
        tracking=True,
    )
    flowchart = fields.Text(
        string='Flujograma',
        tracking=True,
    )

    template_id = fields.Many2one(
        string=u'Plantilla',
        comodel_name='process.edition.template',
    )
    custom_template_id = fields.Many2one(
        string=u'Plantilla',
        comodel_name='process.edition.template',
        domain="[('custom', '=', True), ('economic_activity_name','=',economic_activity_name)]"
    )
    change_history = fields.One2many(
        'process.edition.history', 'process_edition_id', string='Historial de cambios', copy=True)

    custom = fields.Boolean(string='Es personalizado')
    custom_body = fields.Text(string='Contenido')
    
    def _search_name(self, operator, value):
        if operator == 'like':
            operator = 'ilike'
        return [('name', operator, value)]
    
    def _search_code(self, operator, value):
        if operator == 'like':
            operator = 'ilike'
        return [('name', operator, value)]

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

    def cancel_other_versions(self):
        """Cancela las versiones anteriores"""
        for each in self:
            for version in each.old_versions:
                version.write({
                    'state': 'cancel'
                })

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_process.action_mgmt_process_edition').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result

    @api.onchange('template_id')
    def _onchange_template_id(self):
        if not self.template_id:
            return
        else:
            self.purpose = self.template_id.purpose
            self.scope = self.template_id.scope
            self.references = self.template_id.references
            self.body = self.template_id.body
            self.flowchart = self.template_id.flowchart

    @api.onchange('custom_template_id')
    def _onchange_custom_template_id(self):
        if not self.custom_template_id:
            return
        else:
            self.custom_body = self.custom_template_id.custom_body

    def write(self, values):
        if values.get('numero', 'Sin definir') == 'Sin definir' and values.get('state', False) == 'validate_ok':
            values['numero'] = self.sequence_id.next_by_id() or 'Sin definir'
            values['name'] = self.process_id.name + ' ' + values.get('version_as_string', 'Sin definir')

        result = super(ProcessEdition, self).write(values)

        message = self.check_changes(values, "")
        if message != "":
            self.message_post(body=message)

        return result

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

    def create_action(self, vuser_id):
        action = self.env.ref('hola_calidad.p_mail_activity_action').read()[0]
        self.env.cr.execute("""SELECT id FROM ir_model 
                          WHERE model = %s""", (str(self._name),))
        info = self.env.cr.dictfetchall()
        if info:
            model_id = info[0]['id']
        else:
            model_id = None
        action['context'] = {
            'default_res_id': self.ids[0],
            'default_res_model': self._name,
            'default_res_model_id': model_id,
            'default_user_id': vuser_id,
        }
        return action
    
    def send_edition_by_email(self):
        """Envía un correo electrónico a todos los empleados de la empresa
        notificando sobre la existencia de la edición del procedimiento"""
        template = 'mgmtsystem_process.email_template_process_edition'
        return self.notify_users_by_email(template)

    def get_send_to_emails(self):
        """Retorna los correos de trabajo de todos los trabajadores activos
        de la empresa"""
        employee_ids = self.env['hr.employee'].search(
            [('active', '=', True), ('company_id', '=', self.company_id.id)])
        work_emails = ','.join(
            [x.work_email for x in employee_ids if x.work_email])

        return work_emails


class ProcessEditionHistory(models.Model):
    _name = 'process.edition.history'

    process_edition_id = fields.Many2one('process.edition', string='Edición')
    numero = fields.Char(string='Número')
    publish_date = fields.Date(string='Fecha de publicación')
    name = fields.Text(string='Contenido')
