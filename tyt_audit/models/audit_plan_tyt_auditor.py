# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class AuditPlanTytAuditorSchedule(models.Model):
    _name = "audit.plan.tyt.auditor.schedule"
    _description = "Cronograma de Auditoría - Auditor / Cronograma"

    audit_plan_tyt_auditor_id = fields.Many2one(
        'audit.plan.tyt.auditor',string='Sitio'
    )    

    tyt_sites_id = fields.Many2one(
        comodel_name='x_sitios',#'tyt_studio.sites',
        string='Sitios'
    )    
    responsible_auditors_id = fields.Many2many('res.partner', string='Auditores Responsables')
    


    human_resources = fields.Integer(
        string='Recursos Humanos',
        default=0,
    )

    quality = fields.Integer(
        string='Calidad',
        default=0,
    )

    systems = fields.Integer(
        string='Sistemas',
        default=0,
    )

    internal_regulations = fields.Integer(
        string='Reglamento Interno',
        default=0,
    )

    operations = fields.Integer(
        string='Operaciones',
        default=0,
    )

    additionals = fields.Integer(
        string='Adicionales',
        default=0,
    )

    total_sum = fields.Integer(
        string='Totales',
        compute='_compute_total_sum',
        store=True,
    )

    @api.depends('human_resources', 'quality', 'systems', 'internal_regulations', 'operations', 'additionals')
    def _compute_total_sum(self):
        for record in self:
            record.total_sum = (
                record.human_resources +
                record.quality +
                record.systems +
                record.internal_regulations +
                record.operations +
                record.additionals
            )


    @api.constrains('human_resources', 'quality', 'systems', 'internal_regulations', 'operations', 'additionals')
    def _check_positive_values(self):
        for record in self:
            fields_to_check = ['human_resources', 'quality', 'systems', 'internal_regulations', 'operations', 'additionals']
            for field in fields_to_check:
                if getattr(record, field) < 0:
                    raise ValidationError(
                        _("El campo %s no puede ser negativo.") % field.replace('_', ' ').capitalize()
                    )


class AuditPlanTytAuditor(models.Model):
    _name = "audit.plan.tyt.auditor"
    _inherit = ['mgmtsystem.validation.mail', 'mgmtsystem.code']
    _description = "Cronograma de Auditoría - Auditor"

    name = fields.Char(
        string='Nombre',
        required=True,
    )

    active = fields.Boolean('Activo', default=True)
    schedule_ids = fields.One2many( 
        comodel_name='audit.plan.tyt.auditor.schedule',
        inverse_name='audit_plan_tyt_auditor_id',
        string='Cronograma')

    ## Cada vez que se cree un registro en el modelo audit.plan.tyt.auditor se generen automáticamente 8 registros vinculados en el modelo audit.plan.tyt.auditor.schedule con los IDs de sitio específicos [1, 2, 10, 9, 8, 7, 5, 3]

    # @api.model
    # def create(self, vals):
    #     # Crear el registro principal
    #     record = super(AuditPlanTytAuditor, self).create(vals)

    #     # IDs de los sitios
    #     SITE_GUADALAJARA_ID = 1
    #     SITE_HERMOSILLO_ID = 2
    #     SITE_PUEBLA_CAT_ID = 10
    #     SITE_PUEBLA_ID = 9
    #     SITE_QUERETARO_ID = 8
    #     SITE_M_TAPIA_ID = 7
    #     SITE_M_ARTEAGA_ID = 5
    #     SITE_MERIDA_ID = 3

    #     # Usar las variables en lugar de los números directamente
    #     site_ids = [
    #         SITE_GUADALAJARA_ID,
    #         SITE_HERMOSILLO_ID,
    #         SITE_PUEBLA_CAT_ID,
    #         SITE_PUEBLA_ID,
    #         SITE_QUERETARO_ID,
    #         SITE_M_TAPIA_ID,
    #         SITE_M_ARTEAGA_ID,
    #         SITE_MERIDA_ID,
    #     ]
        

    @api.model_create_multi
    def create(self, vals_list):
        # Crear todos los registros principales de AuditPlanTytAuditor de una sola vez
        records = super(AuditPlanTytAuditor, self).create(vals_list)

        # Lista de IDs de sitios
        site_ids = [1, 2, 10, 9, 8, 7, 5, 3]

        # Preparar los valores para los registros de audit.plan.tyt.auditor.schedule
        schedule_vals = []
        for record in records:
            for site_id in site_ids:
                schedule_vals.append({
                    'audit_plan_tyt_auditor_id': record.id,
                    'tyt_sites_id': site_id,
                })

        # Crear todos los registros en audit.plan.tyt.auditor.schedule de una sola vez
        if schedule_vals:
            self.env['audit.plan.tyt.auditor.schedule'].create(schedule_vals)

        return records


    ## OLD VERSION BUTTON + SETTINGS

    parent_edition = fields.Many2one(
        comodel_name='audit.plan.tyt.auditor', copy=False)
    old_versions = fields.One2many(
        comodel_name='audit.plan.tyt.auditor', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    def action_open_older_versions(self):
        result = self.env.ref(
            'tyt_audit.audit_plan_tyt_auditor_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result
    
