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
        'x_sitios',
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


    ## OLD VERSION SETTINGS

    parent_edition = fields.Many2one(
        comodel_name='audit.plan.tyt.auditor', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='audit.plan.tyt.auditor', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    def action_open_older_versions(self):
        result = self.env.ref(
            'tyt_audit.audit_plan_tyt_auditor_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result