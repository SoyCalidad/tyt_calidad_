# -*- coding: utf-8 -*-


from datetime import datetime

from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError, UserError

class AuditReport(models.Model):
    _inherit = "audit.report"

    scope = fields.Text('Alcance', required=False)    

    tyt_line_ids = fields.One2many( 
        comodel_name='audit.audit.planning',
        inverse_name='audit_report_id', #inverse_name='audit_report_id'
        string='Líneas')


    site_id = fields.Many2one(
        'tyt_studio.sites',
        string='Sitios'
    )

    site_manager_id = fields.Many2one(
        string='Gerente de sitio',
        comodel_name='hr.employee',
        ondelete='restrict',
    )

    site_manager_email = fields.Char(
        string='Correo electrónico',
        related='site_manager_id.work_email',
        store=True,
        readonly=True,
    )

    training_manager_id = fields.Many2one(
        string='Responsable de Capacitación y Calidad',
        comodel_name='hr.employee',
        ondelete='restrict',
    )

    audited_ids = fields.Many2many(
        string='Auditados',
        comodel_name='hr.employee',
        ondelete='restrict',
    )

    next_audit = fields.Date(
        string='Próxima Fecha',
    )



    tyt_procedure_description_id = fields.Many2one(
        string='Procedimiento',
        comodel_name='audit.plan.schedule.descriptions',
    )  

    tyt_procedure_activity_id = fields.Many2one(
        string='Actividad',
        comodel_name='audit.plan.schedule.activities',
        domain="[('description_id', '=', tyt_procedure_description_id)]",
    )  

    audit_duration = fields.Integer(
        string='Duración de la Auditoría',
        default=0,
    )

    post_audit_action = fields.Html(string="Post Audit Action", sanitize=True)
    conclusions = fields.Html(string="Conclusions", sanitize=True)


    @api.onchange('audit_id')
    def _onchange_audit_id(self):
        self.name = 'Informe de '+self.audit_id.name if self.audit_id else ""
        self.location = self.audit_id.location
        self.auditor_id = self.audit_id.auditor_id
        self.team_id = self.audit_id.team_id
        self.scope = self.audit_id.observations
        self.golds = self.audit_id.golds
        self.scope = self.audit_id.observations

        self.site_id = self.audit_id.tyt_sites_related_id
        self.tyt_procedure_description_id = self.audit_id.tyt_procedure_description_id
        self.tyt_procedure_activity_id = self.audit_id.tyt_procedure_activity_id
        self.audited_ids = self.audit_id.employee_ids
        self.tyt_line_ids = self.audit_id.planning_ids


        datas = [(5, 0, 0)]
        for line in self.audit_id.line_ids:
            data = {
                'report_id': self.id,
                'name': line.name,
                'employee_id': line.employee_id.id,
                'date_audit': line.datetime,
                # 'nc_id': line.type_id.id,
            }
            datas.append((0, 0, data))
        self.line_ids = datas

    def send_final(self):
        self.write({'state': 'close'})

    # Manejar el porcentaje de good_practices por medio de tyt_line_ids
    good_practices_percentage = fields.Float(
        string="Promedio General de Buenas Prácticas",
        compute="_compute_good_practices_percentage",
        store=True,
    )

    @api.depends('tyt_line_ids.finding')
    def _compute_good_practices_percentage(self):
        for record in self:
            # Contar ocurrencias de "non_conformity" y "good_practices"
            non_conformity_count = len(record.tyt_line_ids.filtered(lambda p: p.finding == 'non_conformity'))
            good_practices_count = len(record.tyt_line_ids.filtered(lambda p: p.finding == 'good_practices'))

            # Calcular el porcentaje de Buenas Prácticas
            total = non_conformity_count + good_practices_count
            record.good_practices_percentage = (good_practices_count / total * 100) if total > 0 else 0