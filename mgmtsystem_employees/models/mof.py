from odoo import _, api, fields, models
from odoo.exceptions import UserError


class Abbreviation(models.Model):
    _name = 'mof.abbreviation'
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


class MOF(models.Model):
    _name = 'mgmtsystem.mof'
    _inherit = ['mgmtsystem.validation.mail',
                'mgmtsystem.version', 'mail.thread', 'mail.activity.mixin']
    _description = 'MOF'

    # Datos generales

    name = fields.Char(string='Nombre')
    process_id = fields.Many2one(
        comodel_name='mgmt.process', string='Procedimiento', domain=[('active','=',True)])

    is_template = fields.Boolean(string='Es plantilla')
    is_custom = fields.Boolean(string='Es personalizado')

    # Validación y versión

    elaborate_ids = fields.Many2many(
        string=u'Elaborado',
        comodel_name='res.users',
        relation='elaborate_mof_rel',
        default=lambda self: self.env.user
    )
    review_ids = fields.Many2many(
        string=u'Revisado',
        relation='review_mof_rel',
        comodel_name='res.users',
    )
    validate_ids = fields.Many2many(
        string=u'Validado',
        relation='validate_mof_rel',
        comodel_name='res.users',
    )

    parent_edition = fields.Many2one(
        comodel_name='mgmtsystem.mof', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='mgmtsystem.mof', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_employees.mof_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result

    # Body

    custom_body = fields.Html(string='Contenido')

    # Capitulo 1

    introduction = fields.Html(string='Introducción')
    target = fields.Html(string='Objetivo del manual')
    scope = fields.Html(string='Alcance')
    references = fields.Html(string='Referencias normativas')
    menanings = fields.Html(string='Términos y definiciones')

    references = fields.Many2many(
        string='Referencias normativas',
        comodel_name='legal.legal',
        relation='references_mof_rel',
    )

    menanings = fields.Many2many(
        string='Terminos y definiciones',
        comodel_name='edition.abbreviation',
        relation='menanings_mof_rel',
    )

    # Capitulo 2

    structure = fields.Html(string='Estructura orgánica')
    org_chart = fields.Many2one(
        comodel_name='mgmtsystem.context.organization_chart', string='Organigrama')
    org_bin = fields.Binary(string='Organigrama')

    jobs_structure = fields.Html(string='Estructura de puestos')
    job_ids = fields.Many2many(comodel_name='hr.job', string='Puestos',
                               relation='job_mof1_rel', domain="[('state','=','validate_ok')]")

    functions = fields.Html(string='Funciones específicas')
    job_2_ids = fields.Many2many(comodel_name='hr.job', string='Puestos',
                                 relation='job_mof2_rel', domain="[('state','=','validate_ok')]")
