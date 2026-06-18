from odoo import models, fields, api
from odoo.exceptions import UserError

from dateutil.relativedelta import relativedelta
import logging 

_logger = logging.getLogger(__name__)


def _get_index_period(period, month):
    if period == 12:
        return month
    if period == 6:
        return int((month // (12/period)) + (month % (12/period)))
    if period == 4:
        if month <=3:
            return 1 
        elif month <=6:
            return 2
        elif month <= 9:
            return 3
        else:
            return 4 
    if period == 3:
        if month <= 4:
            return 1 
        elif month <= 8:
            return 2 
        else:
            return 3
    if period == 2:
        if month <= 6:
            return 1 
        else:
            return 2
    if period == 1:
        return 1
    return 0

class RiskMitigation(models.Model):
    _name = "tyt.risk.mitigation"
    _description = "Mitigación del riesgo"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(string="Activo", default=True)
    risk_id = fields.Many2one(
        comodel_name="tyt.risk.management",
        string="Riesgo",

    )
    risk_id_id = fields.Integer(
        related='risk_id.id',
        string="ID Riesgo",

    )
    risk_id_name = fields.Text(
        related="risk_id.name",
    )
    risk_id_control_objective = fields.Text(string="Objetivo de control", related="risk_id.control_objective", store=True)
    risk_id_control_activity = fields.Text(string="Actividad de control", related='risk_id.control_activity', store=True)
    risk_id_department_id = fields.Many2one(
        related='risk_id.department_id',
    )
    risk_id_goal_coso_ids = fields.Many2many(
        related='risk_id.goal_coso_ids',
        string="Objetivo COSO",

    )
    risk_id_assertion_ids = fields.Many2many(
        related='risk_id.assertion_ids',
        string="Aseveraciones"
    )
    risk_id_frequency_id = fields.Many2one(
        related='risk_id.frequency_id',
        string="Frecuencia"
    )
    risk_id_fsc_id = fields.Many2one(
        related='risk_id.fsc_id',
        string="Categoría del estado financiero",
    )
    risk_id_quadrant = fields.Integer(
        related='risk_id.quadrant',
    )
    risk_id_quantification = fields.Float(string="Cuantificación", related="risk_id.quantification")
    risk_id_type_ma = fields.Selection(related="risk_id.type_ma", string="Manual o Automático")
    risk_id_system_control = fields.Char(string="Sistema de control", related="risk_id.system_control")
    risk_id_type_pd = fields.Selection(related="risk_id.type_pd", string="Preventivo o Detectivo")
    risk_id_impact = fields.Selection(
        related="risk_id.impact",
        string="Impacto"
    )
    risk_id_occurrence = fields.Selection(
        related="risk_id.occurrence",
        string="Ocurrencia"
    )
    risk_id_type_cf = fields.Selection(related="risk_id.type_cf", string="Control de fraude")

    risk_id_domain_id = fields.Many2one(
        related="risk_id.domain_id"
    )
    risk_id_pdomain_id = fields.Many2one(
        related="risk_id.pdomain_id"
    )
    risk_id_subprocess_id = fields.Many2one(
        related="risk_id.subprocess_id",
        store=True
    )
    risk_id_process_id = fields.Many2one(
        related="risk_id.process_id",
        string="Proceso",
        store=True,
    )
    risk_id_owner_id = fields.Many2one(
        related="risk_id.owner_id",
        store=True,
    )
    risk_id_reviewer_id = fields.Many2one(
        related="risk_id.reviewer_id",
        store=True,
    )
    risk_id_auditor_id = fields.Many2one(
        related="risk_id.auditor_id",
        store=True,
    )
    assigned_to = fields.Many2one(
        comodel_name='res.users',
        string="Asignado a",
        compute="_compute_assigned_to",
        store=True,
    )

    @api.depends('status', 'mr_status_mitigation', 'mr_action_plan_ids', 'mr_action_plan_ids.status')
    def _compute_assigned_to(self):
        for rec in self:
            if rec.status == 'unmitigated' and not rec.mr_status_mitigation == 'mitigated':
                rec.assigned_to = rec.risk_id_owner_id
            elif rec.mr_status_mitigation == 'mitigated':
                rec.assigned_to = rec.risk_id_auditor_id
            elif len(rec.mr_action_plan_ids)>0:
                if len(rec.mr_action_plan_ids.filtered(lambda plan: plan.status == 'pending'))>0:
                    rec.assigned_to = rec.risk_id_owner_id
                else: 
                    rec.assigned_to = rec.risk_id_reviewer_id
            else:
                rec.assigned_to = rec.risk_id_reviewer_id 



    status = fields.Selection(
        selection=[
            ('unmitigated', 'No Mitigado'), # create a mitigation
            ('mitigated', 'Mitigado'), # owner notify reviewer
            ('partially_mitigated', 'Parcialmente Mitigado'),
            ('under_review', 'En revisión'), #amarillo

            ('pending', 'Pendiente'), # when existe some plan action pendient 
            ('complete', 'Completado'),
        ],
        string="Estatus",
        default="unmitigated",
        tracking=True,
    )

    status_audit = fields.Selection(
        selection=[
            ('unmitigated', 'No Mitigado'), # create a mitigation
            ('mitigated', 'Mitigado'), # owner notify reviewer
            ('partially_mitigated', 'Parcialmente Mitigado'),
        ],
        string="Estatus de auditoria",
        default="unmitigated",
        tracking=True,
    )

    initial_date = fields.Date(string='Fecha Inicial')
    mitigation_date = fields.Datetime(string='Fecha de Mitigación (Límite)')
    audit_date = fields.Datetime(string='Fecha de Auditoría')
    finish_mitigation = fields.Datetime(string='Finalización Real Mitigación')
    finish_audit = fields.Datetime(string='Finalización Real Auditoría')

    year = fields.Integer(string="Año")


    month = fields.Selection([
        ('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'), ('4', 'Abril'),
        ('5', 'Mayo'), ('6', 'Junio'), ('7', 'Julio'), ('8', 'Agosto'),
        ('9', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre')
    ], string='Mes', tracking=True)
    period_str = fields.Char(string="Periodo", compute="_compute_period_str", store=True)

    @api.depends('year', 'month')
    def _compute_period_str(self):
        for record in self:
            if record.year and record.month:
                # Obtenemos el nombre (label) del mes desde la definición del Selection
                # record.month devuelve la clave (1, 2, 3...), dict(...).get() devuelve 'Enero', 'Febrero'...
                month_name = dict(self._fields['month'].selection).get(record.month)
                record.period_str = f"{record.year}-{month_name}"
            else:
                record.period_str = "Sin Periodo"

    cuadrante = fields.Integer(string='Cuadrante') # algo computado en el grafico
    mr_maturity_level  = fields.Selection(
        selection=[
            ('limited', 'Limitado'),#amarillo 50%
            ('defined', 'Definido'),#amarillo 75%
            ('initial', 'Inicial'),#amarillo 25%
            ('none', 'No existe'),#rojo 0%
            ('optimize', 'Optimizado'),#verde 100   %

        ],
        string="Nivel de madurez",
        default="none",
    )
    residual_risk = fields.Float(string="Riesgo residual", compute="_compute_residual_risk")
    residual_risk_audit = fields.Float(string="Riesgo residual", compute="_compute_residual_risk")
    degree_mitigation = fields.Selection(
        selection=[
            ('0', '0%'),
            ('25', '25%'),
            ('50', '50%'),
            ('75', '75%'),
            ('100', '100%'),
        ],
        string="Grado de mitigación"
    )

    risk_id_quantification = fields.Float(
        related="risk_id.quantification",
    )

    @api.depends('risk_id.quantification', 'degree_mitigation')
    def _compute_residual_risk(self):
        for record in self:
            if record.risk_id and record.risk_id.quantification and record.degree_mitigation:
                record.residual_risk = ((100 - int(record.degree_mitigation)) * record.risk_id.quantification) / 100
            else:
                record.residual_risk = 0

    status_mitigation = fields.Selection(
        selection=[
            ('unmitigated', 'No Mitigado'),
            ('partialmitigated', 'Parcialmente Mitigado'),
            ('mitigated', 'Mitigado'),
        ],
        string="Estatus de mitigación",
        tracking=True,
    )



    def open_reviewer_guide(self):
        return {
            "type": "ir.actions.client",
            "tag": "tyt_risk_management.reviewer_guide",
            'name': 'Guía del revisor',
            
            "target": "new",  
        }

    mo_period_str = fields.Char(string="Periodo calc", compute="_compute_mo_period_str")


    @api.depends('month', 'year')
    def _compute_mo_period_str(self):
        for record in self:
            if record.month and record.year:
                mes = record.month.zfill(2)
                anio = str(record.year)

                if record.risk_id.cr_peoriod == 'fortnightly':
                    record.mo_period_str = f"01-{mes}-{anio} al 09-{mes}-{anio}"
                else:
                    record.mo_period_str = f"01-{mes}-{anio} al 11-{mes}-{anio}"
            else:
                record.mo_period_str = False

    mo_document_ids = fields.One2many(
        comodel_name='tyt.risk.mo_file',
        inverse_name='mitigation_id',
        string="Documentación soporte",
        domain=[('origin', '=', 'mitigation_owner')],
    )
    mo_link_ids = fields.One2many(
        comodel_name='tyt.risk.mo_link',
        inverse_name='mitigation_id',
        string="Enlaces relacionados",
        domain=[('origin', '=', 'mitigation_owner')]
    )
    mo_comment_ids = fields.One2many(
        comodel_name='tyt.risk.mo_comment',
        inverse_name='mitigation_id',
        string="Comentarios"
    )

    def action_notify_revision(self,):
        #open wizard to write coment and send email
        self.write({})
        if not self.mo_document_ids and not self.mo_link_ids:
            raise UserError(
                "Debe cargar al menos algun documento o enlace",
            )

        return {
            'type': 'ir.actions.act_window',
            'name': 'Notificar',
            'res_model': 'tyt.risk.notification.revision',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_mitigation_id': self.id,
            }
        }

    mo_comment_ids_count = fields.Integer(string="N° comentarios", compute="_compute_mo_comment_ids_count")

    @api.depends('mo_comment_ids')
    def _compute_mo_comment_ids_count(self):
        for record in self:
            record.mo_comment_ids_count = len(record.mo_comment_ids)

    #mitigation reviewer
    mr_period_str = fields.Char(string="Periodo revision", compute="_compute_mr_period_str")
    @api.depends('month', 'year')
    def _compute_mr_period_str(self):
        for record in self:
            if record.month and record.year:
                mes = record.month.zfill(2)
                anio = str(record.year)
                if record.risk_id.cr_peoriod == 'fortnightly':
                    record.mr_period_str = f"09-{mes}-{anio} al 14-{mes}-{anio}"
                else:
                    record.mr_period_str = f"11-{mes}-{anio} al 20-{mes}-{anio}"
            else:
                record.mr_period_str = False
    mr_status_mitigation = fields.Selection(
        selection=[
            ('unmitigated', 'No Mitigado'),
            ('partialmitigated', 'Parcialmente Mitigado'),
            ('mitigated', 'Mitigado'),
        ],
        string="Estatus de mitigación",
    )
    # mr_degree_mitigation = fields.Selection(
    #     selection=[
    #         ('0', '0%'),
    #         ('25', '25%'),
    #         ('50', '50%'),
    #         ('75', '75%'),
    #         ('100', '100%'),
    #     ],
    #     string="Grado de mitigación",
    #     default="0",
    # )
    def _default_mr_degree_mitigation(self):
        return self.env.ref('tyt_risk_management.unmitigated_0').id 
    mr_degree_mitigation = fields.Many2one(
        comodel_name='tyt.risk.degree.mitigation',
        string="Grado de mitigación",
        default="_default_mr_degree_mitigation"
    )
    mr_residual_risk = fields.Float(string="Riesgo residual", compute="_compute_mr_residual_risk")

    @api.depends('risk_id_quantification', 'mr_degree_mitigation')
    def _compute_mr_residual_risk(self):
        for record in self:
            if record.risk_id_quantification and record.mr_degree_mitigation:
                record.mr_residual_risk = ((100 - int(record.mr_degree_mitigation.value)) * record.risk_id_quantification) / 100
            else:
                record.mr_residual_risk = 0



    # @api.onchange('mr_status_mitigation')
    # def _onchange_mr_status_mitigation(self):
    #     if self.mr_status_mitigation:
    #         if self.mr_status_mitigation == 'unmitigated':
    #             self.mr_degree_mitigation = '0'
    #         if self.mr_status_mitigation == 'partialmitigated':
    #             self.mr_degree_mitigation = '25'
    #         if self.mr_status_mitigation == 'mitigated':
    #             self.mr_degree_mitigation = '100'
    #     else:
    #         self.mr_degree_mitigation = False

    maturity_level  = fields.Selection(
        selection=[
            ('limited', 'Limitado'),#amarillo 50%
            ('defined', 'Definido'),#amarillo 75%
            ('initial', 'Inicial'),#amarillo 25%
            ('none', 'No existe'),#rojo 0%
            ('optimize', 'Optimizado'),#verde 100   %

        ],
        string="Nivel de madurez"
    )

    mr_mitigation_date = fields.Date(string="Fecha de mitigación")
    mr_level_compliance = fields.Selection(
        selection=[
            ('programmed', 'Programado'),
            ('unaccepted', 'No Atendido'),
            ('ontime', 'A Tiempo') # TODO: Check one use, is compute with mitigation date
        ],
        string="Grado de cumplimiento", default="programmed")
    mr_action_plan_ids = fields.One2many(
        comodel_name='tyt.risk.action.plan',
        inverse_name='mitigation_id',
        string="Plan de acción",
        domain=[('origin', '=', 'review')]

    )
    mr_action_plan_ids_count = fields.Integer(string="N° plan de acción", compute="_compute_mr_action_plan_ids_count")

    @api.depends('mr_action_plan_ids')
    def _compute_mr_action_plan_ids_count(self):
        for rec in self:
            rec.mr_action_plan_ids_count = len(rec.mr_action_plan_ids)
    mr_all_action_plans_complete = fields.Boolean(
        string="MR planes completos?",
        compute='_compute_mr_all_action_plans_complete',

    )

    @api.depends('mr_action_plan_ids', 'mr_action_plan_ids.status')
    def _compute_mr_all_action_plans_complete(self):
        for record in self:
            if len(record.mr_action_plan_ids)>0:
                record.mr_all_action_plans_complete = all(p.status=='complete' for p in record.mr_action_plan_ids)
            else:
                record.mr_all_action_plans_complete = False

    @api.onchange('mr_degree_mitigation')
    def _onchange_mr_degree_mitigation(self):
        if self.mr_degree_mitigation.id == self.env.ref('tyt_risk_management.unmitigated_0').id:
            self.maturity_level = 'none'
        if self.mr_degree_mitigation.id == self.env.ref('tyt_risk_management.pmitigated_25').id:
            self.maturity_level = 'initial'
        if self.mr_degree_mitigation.id == self.env.ref('tyt_risk_management.pmitigated_50').id:
            self.maturity_level = 'limited'
        if self.mr_degree_mitigation.id == self.env.ref('tyt_risk_management.pmitigated_75').id:
            self.maturity_level = 'defined'
        if self.mr_degree_mitigation.id == self.env.ref('tyt_risk_management.mitigated_100').id:
            self.maturity_level = 'optimize'

    
    #mitigation audit
    ma_period_str = fields.Char(string="Periodo revision", compute="_compute_ma_period_str")
    @api.depends('month', 'year')
    def _compute_ma_period_str(self):
        for record in self:
            if record.month and record.year:
                mes = record.month.zfill(2)
                anio = str(record.year)
                if record.risk_id.cr_peoriod == 'fortnightly':
                    record.ma_period_str = f"14-{mes}-{anio} al 15-{mes}-{anio}"
                else:
                    record.ma_period_str = f"20-{mes}-{anio} al 30-{mes}-{anio}"
            else:
                record.ma_period_str = False
    ma_status_mitigation = fields.Selection(
        selection=[
            ('unmitigated', 'No Mitigado'),
            ('partialmitigated', 'Parcialmente Mitigado'),
            ('mitigated', 'Mitigado'),
        ],
        string="Estatus de auditoria",
    )
    ma_degree_mitigation = fields.Many2one(
        comodel_name='tyt.risk.degree.mitigation',
        string="Grado de mitigación",
        default="_default_mr_degree_mitigation"
    )
    ma_residual_risk = fields.Float(string="Riesgo residual", compute="_compute_ma_residual_risk")
    ma_recommendation = fields.Text(string="Recomendación del auditor")

    @api.depends('risk_id_quantification', 'ma_degree_mitigation')
    def _compute_ma_residual_risk(self):
        for record in self:
            if record.risk_id_quantification and record.ma_degree_mitigation:
                record.ma_residual_risk = ((100 - int(record.ma_degree_mitigation.value)) * record.risk_id_quantification) / 100
            else:
                record.ma_residual_risk = 0





    ma_maturity_level  = fields.Selection(
        selection=[
            ('limited', 'Limitado'),#amarillo 50%
            ('defined', 'Definido'),#amarillo 75%
            ('initial', 'Inicial'),#amarillo 25%
            ('none', 'No existe'),#rojo 0%
            ('optimize', 'Optimizado'),#verde 100   %

        ],
        string="Nivel de madurez"
    )

    ma_mitigation_date = fields.Date(string="Fecha de mitigación")
    ma_level_compliance = fields.Char(string="Grado de cumplimiento", default="Programado")
    ma_action_plan_ids = fields.One2many(
        comodel_name='tyt.risk.action.plan',
        inverse_name='mitigation_id',
        string="Plan de acción",
        domain=[('origin', '=', 'audit')]
    )
    ma_all_action_plans_complete = fields.Boolean(
        string="MA planes completos?",
        compute='_compute_ma_all_action_plans_complete',

    )

    @api.depends('ma_action_plan_ids', 'ma_action_plan_ids.status')
    def _compute_ma_all_action_plans_complete(self):
        for record in self:
            if len(record.ma_action_plan_ids)>0:
                record.ma_all_action_plans_complete = all(p.status=='complete' for p in record.ma_action_plan_ids)
            else:
                record.ma_all_action_plans_complete = False

    @api.onchange('ma_degree_mitigation')
    def _onchange_ma_degree_mitigation(self):
        if self.ma_degree_mitigation.id == self.env.ref('tyt_risk_management.unmitigated_0').id:
            self.ma_maturity_level = 'none'
        if self.ma_degree_mitigation.id == self.env.ref('tyt_risk_management.pmitigated_25').id:
            self.ma_maturity_level = 'initial'
        if self.ma_degree_mitigation.id == self.env.ref('tyt_risk_management.pmitigated_50').id:
            self.ma_maturity_level = 'limited'
        if self.ma_degree_mitigation.id == self.env.ref('tyt_risk_management.pmitigated_75').id:
            self.ma_maturity_level = 'defined'
        if self.ma_degree_mitigation.id == self.env.ref('tyt_risk_management.mitigated_100').id:
            self.ma_maturity_level = 'optimize'


    def action_create_action_plan(self,):
        self.ensure_one()
        self.write({
            'risk_activity_state': 'action_plan',
        })
        view_id = self.env.ref('tyt_risk_management.view_risk_action_plan_form').id

        return {
            'type': 'ir.actions.act_window',
            'name': 'Plan de acción',
            'res_model': 'tyt.risk.action.plan',
            'view_mode': 'form',
            'views': [(view_id, 'form')], 
            'target': 'new',
            'context': {
                'default_risk_id': self.risk_id.id,
                'default_mitigation_id': self.id,
                'default_user_id': self.risk_id_owner_id.id,
                'default_origin': 'review',
            }
        }

    risk_activity_state = fields.Selection(
        selection=[
            ('mitigation', 'Mitigación'),
            ('action_plan', 'Plan de acción'),
            ('unmitigated', 'No mitigado'),
            ('monitoring', 'Monitoreo'),

        ],
        default='mitigation',
        string="Actividad",
        tracking=True,
    )

    def action_create_action_plan_audit(self,):
        self.ensure_one()
        self.write({
            'risk_activity_state': 'action_plan',
        })
        view_id = self.env.ref('tyt_risk_management.view_risk_action_plan_form').id

        return {
            'type': 'ir.actions.act_window',
            'name': 'Plan de acción',
            'res_model': 'tyt.risk.action.plan',
            'view_mode': 'form',
            'views': [(view_id, 'form')], 
            'target': 'new',
            'context': {
                'default_risk_id': self.risk_id.id,
                'default_mitigation_id': self.id,
                'default_user_id': self.risk_id_reviewer_id.id,
                'default_origin': 'audit',
            }
        }

    @api.depends('year', 'risk_id')
    def _compute_display_name(self):
        for record in self:
            #year_str = str(record.year) if record.year else "S/A"
            
            risk_id = record.risk_id_id 
            
            record.display_name = f"{self.period_str} - R{risk_id or ''}"

    #controls
    before_control = fields.Selection(
        selection=[
            ('insignificant', 'Insignificate'),
            ('minor', 'Menor'),
            ('higher', 'Mayor'),
            ('significant', 'Significativo'),
            ('severe', 'Severo'),
        ],
        string="Antes de controles",
        compute="_compute_before_control",
        store=True,
    )
    before_control_audit = fields.Selection(
        selection=[
            ('minor', 'Menor'),
            ('higher', 'Mayor'),

            ('significant', 'Significativo'),
            ('insignificant', 'Insignificante'),
            ('severe', 'Severo'),
        ],
        string="Antes de controles (auditoria)",
    )
    after_control = fields.Selection(
        selection=[
            ('minor', 'Menor'),
            ('significant', 'Significativo'),
            ('severe', 'Severo'),
            ('higher', 'Mayor'),
            ('insignificant', 'Insignificante'),


        ],
        string="Después de controles",
        compute="_compute_after_control",
        store=True,
    )
    after_control_audit = fields.Selection(
        selection=[
            ('minor', 'Menor'),
        ],
        string="Después de controles"
    )

    @api.depends('risk_id_impact', 'risk_id_occurrence')
    def _compute_after_control(self):
        for rec in self:
            if rec.mr_status_mitigation == 'mitigated':
                if rec.risk_id_impact == 'high' and rec.risk_id_impact == 'medium':
                    rec.after_control = 'minor'
                else:
                    rec.after_control = 'insignificant'  
            elif rec.mr_status_mitigation == 'partialmitigated': 
                if rec.risk_id_impact == 'high':
                    rec.after_control = 'significant'
                elif (rec.risk_id_impact ==  'medium' and rec.risk_id_occurrence == 'high'):
                    rec.after_control = 'significant'
                else:
                    rec.after_control = 'minor' 
            else:
                if rec.risk_id_impact == 'high' and rec.risk_id_occurrence == 'high':
                    rec.after_control = 'higher'
                elif (rec.risk_id_impact ==  'high' and not rec.risk_id_occurrence == 'high') or (rec.risk_id_impact == 'medium' and  rec.risk_id_occurrence == 'high'):
                    rec.after_control = 'significant'
                else:
                    rec.after_control = 'minor'

    @api.depends('risk_id_impact', 'risk_id_occurrence')
    def _compute_before_control(self):
        for rec in self:
            if rec.risk_id_impact == 'high':
                rec.before_control = 'severe'
            elif rec.risk_id_impact == 'medium':
                rec.before_control = 'higher'
            else: # rec.risk_id_impact == 'low':
                rec.before_control = 'significant'

    @api.model
    def _cron_update_compliance_status(self):
        
        today = fields.Date.context_today(self)
        current_year = today.year
        current_month = today.month # Entero 1-12

        mitigations = self.search([])

        for rec in mitigations:
            if not rec.year or not rec.month:
                continue
                
            # Convertimos el mes de la selección (string) a entero para comparar
            rec_month_int = int(rec.month)
            
            # Verificamos si el periodo ya venció
            if (rec.year < current_year) or (rec.year == current_year and rec_month_int < current_month):
                if rec.mr_level_compliance != 'unaccepted':
                    rec.mr_level_compliance = 'unaccepted'
            else:
                if rec.mr_level_compliance != 'ontime':
                    rec.mr_level_compliance = 'ontime'

    can_create_documents = fields.Boolean(compute="_compute_can_create")

    def _compute_can_create(self):
        for rec in self:
            rec.can_create_documents = rec.risk_id_owner_id.id == self.env.uid

    is_reviewer = fields.Boolean(compute="_compute_is_reviewer")

    def _compute_is_reviewer(self):
        for rec in self:
            rec.is_reviewer = rec.risk_id_reviewer_id.id == self.env.uid

    is_auditor = fields.Boolean(compute="_compute_is_auditor")

    def _compute_is_auditor(self):
        for rec in self:
            rec.is_auditor = rec.risk_id_auditor_id.id == self.env.uid


    def write(self, vals):
        if 'mr_status_mitigation' in vals and vals['mr_status_mitigation'] == 'partialmitigated':
            vals['status'] = 'partially_mitigated'
        
        if 'mr_status_mitigation' in vals and vals['mr_status_mitigation'] == 'mitigated':
            vals['mr_mitigation_date'] = fields.Datetime.now().date()
            vals['mr_level_compliance'] = 'ontime'
            vals['status'] = 'mitigated' # en revision por el auditor 
            vals['risk_activity_state'] = 'monitoring'

        if 'ma_status_mitigation' in vals and vals['ma_status_mitigation'] == 'mitigated':
            vals['ma_mitigation_date'] = fields.Datetime.now().date()
            vals['ma_level_compliance'] = 'A tiempo' # tambien hay fuera de periodo
            vals['status'] = 'complete' 
        return super().write(vals)

    @api.model
    def get_available_years(self):
        # Usamos f-string para inyectar dinámicamente el nombre de la tabla
        # Odoo guarda el nombre real de la tabla en el atributo privado _table
        query = f"""
            SELECT DISTINCT year 
            FROM {self._table} 
            WHERE year IS NOT NULL 
            ORDER BY year DESC
        """
        
        self.env.cr.execute(query)
        
        # Obtenemos solo el primer elemento de cada tupla en el resultado
        return [r[0] for r in self.env.cr.fetchall()]
        

    def get_form_action_id(self):
        action = self.env.ref("tyt_risk_management.action_risk_my_activity")
        return action.id 

    def _data_mitigation_for_consolidated(self, mitigation):
        return {
            'id': mitigation.id,
            'risk_activity_state': mitigation.risk_activity_state,
            'risk_id_quadrant': mitigation.risk_id_quadrant,
            'risk_id_id': mitigation.risk_id_id,
            'status': mitigation.status,
            'mr_status_mitigation': mitigation.mr_status_mitigation,
        }

    def _load_data_processes(self, mitigations):
        process_dict = dict()
        for m in mitigations:
            if not m.risk_id_process_id:
                continue
            n_unmitigation = 0
            n_partialmitigated = 0
            n_mitigation = 0
            if m.mr_status_mitigation == 'unmitigated':
                n_unmitigation += 1
            elif m.mr_status_mitigation=='partialmitigated':
                n_partialmitigated += 1
            else:
                n_mitigation += 1
            if m.risk_id_process_id.id not in process_dict:
                process_dict[m.risk_id_process_id.id] = {
                    'id': m.risk_id_process_id.id,
                    'name': m.risk_id_process_id.name,
                    'short_name': m.risk_id_process_id.short_name,
                    'quantification': m.risk_id_quantification,
                    'residual': m.mr_residual_risk,
                    'n_unmitigation': n_unmitigation,
                    'n_partialmitigated': n_partialmitigated,
                    'n_mitigation': 0,

                    'subprocesses': [{
                        'id': m.risk_id_subprocess_id.id,
                        'name': m.risk_id_subprocess_id.name,
                        'short_name': m.risk_id_subprocess_id.short_name,
                        'quantification': m.risk_id_quantification,
                        'residual': m.mr_residual_risk,
                        'n_unmitigation': n_unmitigation,
                        'n_partialmitigated': n_partialmitigated,
                        'n_mitigation': n_mitigation,
                    }]
                } 
            else:
                process_dict[m.risk_id_process_id.id]["quantification"] += m.risk_id_quantification
                process_dict[m.risk_id_process_id.id]["residual"] += m.mr_residual_risk
                process_dict[m.risk_id_process_id.id]["n_unmitigation"] += n_unmitigation
                process_dict[m.risk_id_process_id.id]["n_partialmitigated"] += n_partialmitigated
                process_dict[m.risk_id_process_id.id]["n_mitigation"] += n_mitigation
                exist_subprocess = False 
                for index, subp in enumerate(process_dict[m.risk_id_process_id.id]["subprocesses"]):
                    if subp["id"] == m.risk_id_subprocess_id.id:
                        exist_subprocess = index 
                        break 

                if exist_subprocess:
                    process_dict[m.risk_id_process_id.id]["subprocesses"][exist_subprocess]["quantification"] += m.risk_id_quantification
                    process_dict[m.risk_id_process_id.id]["subprocesses"][exist_subprocess]["residual"] += m.mr_residual_risk
                    process_dict[m.risk_id_process_id.id]["subprocesses"][exist_subprocess]["n_unmitigation"] += n_unmitigation
                    process_dict[m.risk_id_process_id.id]["subprocesses"][exist_subprocess]["n_partialmitigated"] += n_partialmitigated
                    process_dict[m.risk_id_process_id.id]["subprocesses"][exist_subprocess]["n_mitigation"] += n_mitigation

        return list(process_dict.values())



    @api.model 
    def report_consolidated(self, department_id, pdomain_id, process_id, anio, month):
        domain_mitigation = [
            ('risk_activity_state', 'in', [ 'mitigation', 'monitoring' ]),
            ('mitigation_date', '<=', (fields.Datetime.today() + relativedelta(months=1, day=1)))
        ] 
        if department_id and int(department_id):
            domain_mitigation.append(('risk_id_department_id', '=', department_id))
        if pdomain_id and int(pdomain_id):
            domain_mitigation.append(('risk_id_pdomain_id', '=', pdomain_id))
        if process_id and int(process_id):
            domain_mitigation.append(('risk_id_process_id', '=', process_id))
        if anio and int(anio):
            domain_mitigation.append(('year', '=', int(anio)))
        if month and int(month):
            domain_mitigation.append(('month', '=', str(int(month))))

        mitigations = self.env['tyt.risk.mitigation'].search(
            domain_mitigation,  
        )
        m_mitigation = mitigations.filtered(lambda m: m.risk_activity_state=='mitigation')
        m_monitoring = mitigations.filtered(lambda m: m.risk_activity_state=='monitoring')

        return {
            "lista": [self._data_mitigation_for_consolidated(m) for m in mitigations],
            "listaResumen": [],
            "resumenProcesos": {
                "mitigado": [self._data_mitigation_for_consolidated(m) for m in m_mitigation],
                "monitoring": [self._data_mitigation_for_consolidated(m) for m in m_monitoring],
            },
            "processes_mitigated": self._load_data_processes(m_mitigation),
            "processes_monitoring": self._load_data_processes(m_monitoring),
            "mitigated_riesgo_asegurado": sum(m_mitigation.mapped('risk_id_quantification')),
            "mitigated_riesgo_residual": sum(m_mitigation.mapped('residual_risk')),
            "monitoring_riesgo_asegurado": sum(m_monitoring.mapped('risk_id_quantification')),
            "monitoring_riesgo_residual": sum(m_monitoring.mapped('residual_risk')),
            "barchart_mitigated":  [
                len(m_mitigation.filtered(lambda m: m.mr_status_mitigation=='unmitigated')),
                len(m_mitigation.filtered(lambda m: m.mr_status_mitigation=='partialmitigated')),
                len(m_mitigation.filtered(lambda m: m.mr_status_mitigation=='mitigated')),
            ],
            "barchart_monitoring":  [
                len(m_monitoring.filtered(lambda m: m.ma_status_mitigation=='unmitigated')),
                len(m_monitoring.filtered(lambda m: m.ma_status_mitigation=='partialmitigated')),
                len(m_monitoring.filtered(lambda m: m.ma_status_mitigation=='mitigated')),
            ],
            "maturity_mitigated": [
                len(m_mitigation.filtered(lambda m: m.mr_maturity_level=='none')),
                len(m_mitigation.filtered(lambda m: m.mr_maturity_level=='initial')),
                len(m_mitigation.filtered(lambda m: m.mr_maturity_level=='limited')),
                len(m_mitigation.filtered(lambda m: m.mr_maturity_level=='defined')),
                len(m_mitigation.filtered(lambda m: m.mr_maturity_level=='optimize')),
            ],
            "maturity_monitoring": [
                len(m_mitigation.filtered(lambda m: m.ma_maturity_level=='none')),
                len(m_mitigation.filtered(lambda m: m.ma_maturity_level=='initial')),
                len(m_mitigation.filtered(lambda m: m.ma_maturity_level=='limited')),
                len(m_mitigation.filtered(lambda m: m.ma_maturity_level=='defined')),
                len(m_mitigation.filtered(lambda m: m.ma_maturity_level=='optimize')),
            ],
            
        }
        

    @api.model
    def report_executive(self, department_id, pdomain_id, process_id, anio, month):
        domain_mitigation = [
            ('mitigation_date', '<=', (fields.Datetime.today() + relativedelta(months=1, day=1)))
        ] 
        if department_id and int(department_id):
            domain_mitigation.append(('risk_id_department_id', '=', department_id))
        if pdomain_id and int(pdomain_id):
            domain_mitigation.append(('risk_id_pdomain_id', '=', pdomain_id))
        if process_id and int(process_id):
            domain_mitigation.append(('risk_id_process_id', '=', process_id))
        if anio and int(anio):
            domain_mitigation.append(('year', '=', int(anio)))
        if month and int(month):
            domain_mitigation.append(('month', '=', str(int(month))))

        mitigations = self.env['tyt.risk.mitigation'].search(
            domain_mitigation,  
        )

        maturity_level = "No existe" #TODO: this is a compute 
        target_dic = dict() #key is target a values [asegurado, no_asegurado]
        degree_of_compliance_company_dict = dict() #key departmentname , value is [n_asegurado, total, residual]
        degree_of_compliance_company = []
        targets = []
        nivel_madurez=[]
        for m in mitigations:
            target_name = ",".join([g.display_name for g in m.risk_id.goal_coso_ids])
            asegurado = 0
            no_asegurado = 0
            if m.mr_status_mitigation=='mitigated':
                asegurado = 1
            else:
                no_asegurado = 1
            if target_name in target_dic:
                target_dic[target_name][0] = asegurado
                target_dic[target_name][1] = no_asegurado
            else:
                target_dic[target_name] = [asegurado, no_asegurado]

        
            if m.risk_id_department_id.name in degree_of_compliance_company_dict:
                degree_of_compliance_company_dict[m.risk_id_department_id.name][0] += asegurado
                degree_of_compliance_company_dict[m.risk_id_department_id.name][1] += 1
                degree_of_compliance_company_dict[m.risk_id_department_id.name][2] += m.mr_residual_risk 
            else:
                degree_of_compliance_company_dict[m.risk_id_department_id.name] = [
                    asegurado,
                    1,
                    m.mr_residual_risk,
                ]

            find_level=False 
            for index, item in enumerate(nivel_madurez):
                if item["nivel"] == m.mr_maturity_level:
                    find_level = index 

            if find_level:
                nivel_madurez[find_level]["count"] += 1
            else:
                nivel_madurez.append({
                    "nivel": m.mr_maturity_level,
                    "count": 1,
                    "name": dict(self._fields['mr_maturity_level'].selection).get(m.mr_maturity_level),
                })


        for name, values in target_dic.items():
            targets.append({
                "objetivo": name,
                "asegurados": values[0],
                "no_asegurados": values[1]
            })
        for name, values in degree_of_compliance_company_dict.items():
            degree_of_compliance_company.append({
                "department_name": name,
                "grado_cumplimiento": round((values[0] / values[1])*100),
                "grado_cumplimiento_residual": values[2],
            })

        len_mitigations = len(mitigations)
        
        return {
            "lista": [],
            "report": {
                "lista": [ self._data_mitigation_for_consolidated(m) for m in mitigations],
                "num_mitigation_total": len_mitigations,
                "per_mitigation_safe": (round((len(mitigations.filtered(lambda m: m.mr_status_mitigation=='mitigated')) / len_mitigations) * 100)) if len_mitigations>0 else 0,
                "riesgos_no_asegurados_impacto": sum(mitigations.filtered(lambda m: m.mr_status_mitigation!='mitigated').mapped('risk_id_quantification')),
                "nivel_de_madurez": maturity_level,

                "objetivos": targets,
                "degree_of_compliance_company": degree_of_compliance_company,
                "nivel_madurez":  nivel_madurez,

            },
        }

    @api.model
    def mitigation_detail(self, mitigation_id=None):
        if not mitigation_id:
            return {}
        m = self.browse(mitigation_id)

        return {
            "id": m.id, 
            "risk_name": m.risk_id_name,
            "risk_process": m.risk_id_process_id.display_name,
            "risk_subprocess": m.risk_id_subprocess_id.display_name,
            "anio": m.year,
            "month": dict(self._fields['month'].selection).get(m.month),
            "risk_id": m.risk_id_id,
            "risk_pdomain": m.risk_id_pdomain_id.display_name,
            "risk_low_scenery": m.risk_id.low_scenery, 
            "risk_middle_scenery": m.risk_id.middle_scenery, 
            "risk_high_scenery": m.risk_id.high_scenery, 
            "risk_impact": dict(self.env['tyt.risk.management']._fields['impact'].selection).get(m.risk_id_impact),
            "risk_occurrence": dict(self.env['tyt.risk.management']._fields['occurrence'].selection).get(m.risk_id_occurrence),
            "risk_control_objective": m.risk_id.control_objective,
            "risk_goal_coso_names": "\n".join([g.name for g in m.risk_id.goal_coso_ids]),
            "risk_control_activity": m.risk_id.control_activity,
            "risk_assertion_names": ",".join([a.name for a in m.risk_id.assertion_ids]),
            "risk_type_ma": dict(self.env['tyt.risk.management']._fields['type_ma'].selection).get(m.risk_id.type_ma),
            'risk_system_control': m.risk_id.system_control,
            'risk_frequency_name': m.risk_id.frequency_id.name,
            "risk_type_pd": dict(self.env['tyt.risk.management']._fields['type_pd'].selection).get(m.risk_id.type_pd),
            "risk_type_cf": dict(self.env['tyt.risk.management']._fields['type_cf'].selection).get(m.risk_id.type_cf),

            "residual_risk": m.residual_risk,
            "risk_quantification": m.risk_id_quantification,
            "before_control": dict(self._fields['before_control'].selection).get(m.before_control),
            "after_control": dict(self._fields['after_control'].selection).get(m.after_control),
            "mr_degree_mitigation": m.mr_degree_mitigation.name ,
            "mr_level_compliance": dict(self._fields['mr_level_compliance'].selection).get(m.mr_level_compliance),
            "mr_maturity_level": dict(self._fields['mr_maturity_level'].selection).get(m.mr_maturity_level),
            "mr_status_mitigation": dict(self._fields['mr_status_mitigation'].selection).get(m.mr_status_mitigation)
        }

    @api.model
    def calc_num_periods(self, years, months):
        return 0

    @api.model
    def customized_report(self, department_ids, pdomain_ids, process_ids, years, months):
        num_period = 0
        data_list = []
        label_time = []
        if department_ids or pdomain_ids or process_ids or years or months:
            domain_m = []
            domain_domain = [('level', '=', 1)]
            domain_process = [('level', '=', 2)]
            domain_depts = [('x_studio_npp', '=', 1)]
            if department_ids and isinstance(department_ids, list):
                domain_m.append(('risk_id.department_id', 'in', department_ids))
                domain_depts.append(('id', 'in', department_ids))
            if pdomain_ids and isinstance(pdomain_ids, list):
                domain_m.append(('risk_id.pdomain_id', 'in', pdomain_ids))
                domain_domain.append(('id', 'in', pdomain_ids))
            if process_ids and isinstance(process_ids, list):
                domain_process.append(('id', 'in', process_ids))
                domain_m.append(('risk_id.process_id', 'in', process_ids))
            if years and isinstance(years, list):
                domain_m.append(('year', 'in', years))
            if months and isinstance(months, list):
                domain_m.append(('month', 'in', months))

            available_years = self.get_available_years()
            iterable_years = sorted(years or available_years)
            _logger.info(f"mes array, {months}")
            iterable_months = months or [1,2,3,4,5,6,7,8,9,10,11,12]
            _logger.info(f"mes array iterable, {iterable_months}")
            num_period = len(iterable_years) * len(iterable_months)

            departments = self.env['hr.department'].search(domain_depts)
            domains = self.env['tyt.business.process'].search(domain_domain)
            process = self.env['tyt.business.process'].search(domain_process)
            sub_process = self.env['tyt.business.process'].search([('parent_id', 'in', process.ids)])
            
            for d in departments:
                for do in domains:
                    for p in process.filtered(lambda pro: pro.parent_id.id==do.id):
                        for sp in sub_process.filtered(lambda subp: subp.parent_id.id==p.id):
                            month_table = []
                            for y_index, y in enumerate(iterable_years):
                                for m_index, m in enumerate(iterable_months):
                                    month_label = dict(self._fields['month'].selection).get(f"{m}")
                                    if f"{month_label} {y}" not in label_time:
                                        label_time.append(f"{month_label} {y}")
                                    mitigations = self.env['tyt.risk.mitigation'].search([
                                        ('risk_id.department_id', '=', d.id),
                                        ('risk_id.process_id', '=', p.id),
                                        ('risk_id.subprocess_id', '=', sp.id),
                                        ('risk_id.pdomain_id', '=', do.id),
                                        ('year', '=', int(y)),
                                        ('month', '<=', str(m)),
                                    ])
                                    mi_month = mitigations.filtered(lambda mi: mi.month == m)
                                    compliances = []
                                    num_100 = 0
                                    for mi in mi_month:
                                        if mi.mr_degree_mitigation.value ==100:
                                            num_100 += 1
                                        compliances.append(mi.mr_degree_mitigation.value)
                                    month_table.append(
                                        {
                                            "month": m,
                                            "month_name": "sys_month_5",
                                            "month_text": month_label,
                                            "year": y,
                                            "cantidad": len(mi_month),
                                            "compliance": round(sum(compliances) / len (compliances) if len(compliances)> 0 else 0),
                                            "complianceAcomulado": round(num_100 / len(compliances) if len(compliances)>0 else 0),
                                            "cantidadAcomulada": len(compliances),
                                            "risks": list(mi_month.mapped('id')),
                                            "risksAcomulado": list(mitigations.mapped('id')),
                                        })

                            data_list.append({
                                "id": f"{d.id}-{p.id}-{sp.id}-{do.id}",
                                "department_name": d.display_name,
                                "process_name": p.display_name,
                                "sub_process_name": sp.display_name,
                                "pdomain_name": do.display_name,
                                "month_table": month_table,
                            })


        return {
            "label_header": ["Riesgos", "Cumplimiento", "Cumplimiento acumulado"] * num_period,
            "label_time": label_time,
            "list": data_list,
        }

    @api.model 
    def rpe_carried_out_report(self, department_id, year, cr_peoriod, revision_type):
        domain_mitigation = [
            ('mitigation_date', '<=', (fields.Datetime.today() + relativedelta(months=1, day=1)))

        ]
        if department_id and int(department_id):
            domain_mitigation.append(('risk_id.department_id', '=', int(department_id)))
        if year and int(year):
            domain_mitigation.append(('year', '=', int(year)))
        num_period = 1
        if cr_peoriod:
            if revision_type == 'sys_only_normal':
                domain_mitigation.append(('risk_id.cr_peoriod', '!=', 'fortnightly'))
            if revision_type == 'sys_only_special':
                domain_mitigation.append(('risk_id.cr_peoriod', '=',  'fortnightly'))

            if cr_peoriod == 'month':
                num_period = 12
            if cr_peoriod == 'bi':
                num_period = 6
            if cr_peoriod == 'tri':
                num_period = 4
            if cr_peoriod == 'cua':
                num_period = 3
            if cr_peoriod == 'se':
                num_period = 2
            if cr_peoriod == 'anual':
                num_period = 1

        _logger.info(f"domain_mitigation {domain_mitigation}")
        mitigations = self.env['tyt.risk.mitigation'].search(domain_mitigation)

        department_dict = dict()
        level_dict = dict() #key is (dep_id, level) and value is num 
        for mitigation in mitigations:
            key = (mitigation.risk_id_department_id.id, mitigation.mr_degree_mitigation.value, mitigation.risk_id_department_id.display_name, mitigation.month)
            if key in department_dict:
                department_dict[(key)] += 1
            else:
                department_dict[(key)] = 1


        data_report = []
        total_obj =  {
            "department_name": "sys_report_sox_1",
            "department_id": "sys_report_sox_1",
            "items": [
                {
                    "titulo": "sys_sox1_nivel_0",
                    "nivel": 0,
                    "periodos": [{"periodo": str(_l), "valor": 0} for _l in range(1, num_period +1)],
                    "total": 0,
                    "porcentaje": 0
                },
                {
                    "titulo": "sys_sox1_nivel_25",
                    "nivel": 25,
                    "periodos": [{"periodo": str(_l), "valor": 0} for _l in range(1, num_period +1)],
                    "total": 0,
                    "porcentaje": 0
                },
                {
                    "titulo": "sys_sox1_nivel_50",
                    "nivel": 50,
                    "periodos": [{"periodo": str(_l), "valor": 0} for _l in range(1, num_period +1)],
                    "total": 0,
                    "porcentaje": 0
                },
                {
                    "titulo": "sys_sox1_nivel_75",
                    "nivel": 75,
                    "periodos": [{"periodo": str(_l), "valor": 0} for _l in range(1, num_period +1)],
                    "total": 0,
                    "porcentaje": 0
                },
                {
                    "titulo": "sys_sox1_nivel_100",
                    "nivel": 100,
                    "periodos": [{"periodo": str(_l), "valor": 0} for _l in range(1, num_period +1)],
                    "total": 0,
                    "porcentaje": 0
                }
            ],
            "totales": {
                "titulo": "sys_sox1_nivel_total",
                "nivel": 0,
                "periodos":  [{"periodo": str(_l), "valor": 0} for _l in range(1, num_period +1)],
                "total": 0,
                "porcentaje": 100
            }
        }
        for dep_id, level, dep_name, month in department_dict.keys():
            index_data = None
            for i, da in enumerate(data_report):
                if dep_name == da["department_name"]:
                    index_data = i
                    break 
            index_pe = _get_index_period(num_period, int(month)) -1
            if index_data is not None:
                if level == 0:
                    data_report[index_data]["items"][0]["periodos"][index_pe]["valor"] +=1
                    data_report[index_data]["items"][0]["total"] +=1
                elif level == 25:
                    data_report[index_data]["items"][1]["total"] +=1
                    data_report[index_data]["items"][1]["periodos"][index_pe]["valor"] +=1
                elif level == 50:
                    data_report[index_data]["items"][2]["total"] +=1
                    data_report[index_data]["items"][2]["periodos"][index_pe]["valor"] +=1
                elif level == 25:
                    data_report[index_data]["items"][3]["total"] +=1
                    data_report[index_data]["items"][3]["periodos"][index_pe]["valor"] +=1
                else:
                    data_report[index_data]["items"][4]["total"] +=1
                    data_report[index_data]["items"][4]["periodos"][index_pe]["valor"] +=1
                data_report[index_data]["totales"]["total"] += 1
                data_report[index_data]["totales"]["periodos"][index_pe]["valor"] += 1
            else:
                data_report.append({
                    "department_name": dep_name,
                    "department_id": dep_id,
                    "items": [
                        {
                            "titulo": "sys_sox1_nivel_0",
                            "nivel": 0,
                            "periodos": [{"periodo": str(_l), "valor": 1 if index_pe == _l and level == 0 else 0} for _l in range(1, num_period +1)],
                            
                            "total":  1 if  level == 0 else 0,
                            "porcentaje": 0
                        },
                        {
                            "titulo": "sys_sox1_nivel_25",
                            "nivel": 25,
                            "periodos": [{"periodo": str(_l), "valor": 1 if index_pe == _l and level == 25 else 0} for _l in range(1, num_period +1)],
                            "total": 1 if level== 25 else 0,
                            "porcentaje": 0
                        },
                        {
                            "titulo": "sys_sox1_nivel_50",
                            "nivel": 50,
                            "periodos": [{"periodo": str(_l), "valor": 1 if index_pe == _l and level == 50 else 0} for _l in range(1, num_period +1)],

                            "total": 1 if level== 50 else 0,
                            "porcentaje": 0
                        },
                        {
                            "titulo": "sys_sox1_nivel_75",
                            "nivel": 75,
                            "periodos": [{"periodo": str(_l), "valor": 1 if index_pe == _l and level == 75 else 0} for _l in range(1, num_period +1)],
                            "total": 1 if level== 75 else 0,
                            "porcentaje": 0
                        },
                        {
                            "titulo": "sys_sox1_nivel_100",
                            "nivel": 100,
                            "periodos": [{"periodo": str(_l), "valor": 1 if index_pe == _l and level == 100 else 0} for _l in range(1, num_period +1)],
                            "total": 1 if level== 100 else 0,
                            "porcentaje": 0
                        }
                    ],
                    "totales": {
                        "titulo": "sys_sox1_nivel_total",
                        "nivel": 0,
                        "periodos": [{
                            "periodo": str(_l), 
                            "valor": 1 if _l==index_pe else 0} for _l in range(1, num_period +1)],
                        "total": 1,
                        "porcentaje": 100
                    }
                })

            if level== 0:
                total_obj['items'][0]["periodos"][index_pe]["valor"] += 1
                total_obj['items'][0]["total"] += 1
                total_obj['totales']["periodos"][index_pe]["valor"] += 1
                total_obj['totales']["total"] += 1
            if level== 25:
                total_obj['items'][1]["periodos"][index_pe]["valor"] += 1
                total_obj['items'][1]["total"] += 1
                total_obj['totales']["periodos"][index_pe]["valor"] += 1
                total_obj['totales']["total"] += 1
            if level== 50:
                total_obj['items'][2]["periodos"][index_pe]["valor"] += 1
                total_obj['items'][2]["total"] += 1
                total_obj['totales']["periodos"][index_pe]["valor"] += 1
                total_obj['totales']["total"] += 1
            if level== 75:
                total_obj['items'][3]["periodos"][index_pe]["valor"] += 1
                total_obj['items'][3]["total"] += 1
                total_obj['totales']["periodos"][index_pe]["valor"] += 1
                total_obj['totales']["total"] += 1
            if level== 100:
                total_obj['items'][4]["periodos"][index_pe]["valor"] += 1
                total_obj['items'][4]["total"] += 1
                total_obj['totales']["periodos"][index_pe]["valor"] += 1
                total_obj['totales']["total"] += 1
        #calculate totals
        for d in data_report:
            #total by periodo
            total_m = d["totales"]["total"] 
            if total_m == 0:
                continue
            for item in d["items"]:
                item["porcentaje"] = round((item["total"] / total_m) * 100, 2)

        if total_obj['totales']["total"]> 0:
            for t_item in total_obj["items"]:
                t_item["porcentaje"] = round((t_item["total"] / total_obj['totales']["total"]) * 100, 2)

        return {
            "periods": list(range(1,num_period+1)),
            "report": data_report,
            "totals": total_obj,
        }

    @api.model 
    def rpe_consolidated_report(self, department_id, year, cr_peoriod, revision_type):
        domain_mitigation = [
            ('mitigation_date', '<=', (fields.Datetime.today() + relativedelta(months=1, day=1)))
        ]
        if department_id and int(department_id):
            domain_mitigation.append(('risk_id.department_id', '=', int(department_id)))
        if year and int(year):
            domain_mitigation.append(('year', '=', int(year)))
        num_period = 1
        if cr_peoriod:
            if revision_type == 'sys_only_normal':
                domain_mitigation.append(('risk_id.cr_peoriod', '!=', 'fortnightly'))
            if revision_type == 'sys_only_special':
                domain_mitigation.append(('risk_id.cr_peoriod', '=',  'fortnightly'))

            if cr_peoriod == 'month':
                num_period = 12
            if cr_peoriod == 'bi':
                num_period = 6
            if cr_peoriod == 'tri':
                num_period = 4
            if cr_peoriod == 'cua':
                num_period = 3
            if cr_peoriod == 'se':
                num_period = 2
            if cr_peoriod == 'anual':
                num_period = 1

        mitigations = self.env['tyt.risk.mitigation'].search(domain_mitigation)

        department_dict = dict()
        level_dict = dict() #key is (dep_id, level) and value is num 
        for mitigation in mitigations:
            key = (mitigation.risk_id_department_id.id, mitigation.mr_status_mitigation, mitigation.risk_id_department_id.display_name, mitigation.month)
            if key in department_dict:
                department_dict[(key)] += 1
            else:
                department_dict[(key)] = 1

       
        data_report = []
        total_obj =  {
            "titulo": "sys_sox1_nivel_total",
            "total": 0  ,
            "porcentaje": 100,
            "periodos":  [{"periodo": str(_l), "mitigado": 0, "parcial": 0, "no": 0, "total": 0} for _l in range(1, num_period +1)],
        }
        for dep_id, status_mitigation, dep_name, month in department_dict.keys():
            _logger.info(f"status_mitigation, {status_mitigation}")
            index_data = None
            for i, da in enumerate(data_report):
                if dep_name == da["department_name"]:
                    index_data = i
                    break 
            index_pe = _get_index_period(num_period, int(month)) - 1
            if index_data is not None:
                data_report[index_data]["total"] += 1
                if status_mitigation == 'mitigated':
                    data_report[index_data]["periodos"][index_pe]["mitigado"] +=1
                    data_report[index_data]["periodos"][index_pe]["total"] +=1
                elif status_mitigation == 'partialmitigated':
                    data_report[index_data]["periodos"][index_pe]["parcial"] +=1
                    data_report[index_data]["periodos"][index_pe]["total"] +=1
                else:
                    data_report[index_data]["periodos"][index_pe]["no"] +=1
                    data_report[index_data]["periodos"][index_pe]["total"] +=1

            else: 
                data_report.append({
                    "department_name": dep_name,
                    "department_id": dep_id,
                    "total": 1,
                    "porcentaje": 0,
                    
                    "periodos": [{
                        "periodo": str(_l), 
                        "mitigado": 1 if status_mitigation == 'mitigated' and _l -1 == index_pe else 0,
                        "parcial":  1 if status_mitigation == 'partialmitigated' and _l -1 == index_pe else 0, 
                        "no":   1 if (status_mitigation == 'unmitigated' or status_mitigation == False) and _l -1 == index_pe else 0, 
                        "total": 1 if  _l -1 == index_pe else 0} for _l in range(1, num_period +1)],
                    
                })

            total_obj["total"] += 1
            if status_mitigation == 'unmitigated' or status_mitigation == False:
                total_obj["periodos"][index_pe]["no"] += 1
            if status_mitigation == 'partialmitigated':
                total_obj["periodos"][index_pe]["parcial"] += 1
            if status_mitigation == 'mitigated':
                total_obj["periodos"][index_pe]["mitigado"] += 1
            total_obj["periodos"][index_pe]["total"] += 1
            _logger.info(f"total_obj periodos, {total_obj['periodos'][index_pe]}")

            

            


        if total_obj['total'] >  0:
            for item in data_report:
                item["porcentaje"] = round((item["total"] / total_obj['total'])*100, 2)

        return {
            "report": data_report,
            "totales": total_obj,
        }

    @api.model 
    def rpe_remedition_action(self, department_id, year, cr_peoriod, revision_type):
        domain_mitigation = [
            ('mitigation_date', '<=', (fields.Datetime.today() + relativedelta(months=1, day=1)))

        ]
        if department_id and int(department_id):
            domain_mitigation.append(('risk_id.department_id', '=', int(department_id)))
        if year and int(year):
            domain_mitigation.append(('year', '=', int(year)))
        num_period = 1
        if cr_peoriod:
            if revision_type == 'sys_only_normal':
                domain_mitigation.append(('risk_id.cr_peoriod', '!=', 'fortnightly'))
            if revision_type == 'sys_only_special':
                domain_mitigation.append(('risk_id.cr_peoriod', '=',  'fortnightly'))

            if cr_peoriod == 'month':
                num_period = 12
            if cr_peoriod == 'bi':
                num_period = 6
            if cr_peoriod == 'tri':
                num_period = 4
            if cr_peoriod == 'cua':
                num_period = 3
            if cr_peoriod == 'se':
                num_period = 2
            if cr_peoriod == 'anual':
                num_period = 1

        mitigations = self.env['tyt.risk.mitigation'].search(domain_mitigation)
        plans = self.env['tyt.risk.action.plan'].search([
            ('mitigation_id', 'in', mitigations.ids)
        ])
        department_dict = dict()
        for plan in plans:
            key = (plan.status, plan.mitigation_id.risk_id_department_id.display_name, plan.mitigation_id.risk_id_department_id.id, plan.mitigation_id_month)
            if key in department_dict:
                department_dict[(key)] += 1
            else:
                department_dict[(key)] = 1

                
        data_report = []
        total_obj =  {
            "department_name": "sys_report_sox_3",
            "department_id": "sys_report_sox_3",
            "items": [
                {
                    "titulo": "sys_sox_reme_open",
                    "periodos": [{"periodo": str(_l), "valor": 0} for _l in range(1, num_period +1)],
                    "total": 0,
                    "porcentaje": 0
                },
                {
                    "titulo": "sys_sox_reme_process",
                    "nivel": 25,
                    "periodos": [{"periodo": str(_l), "valor": 0} for _l in range(1, num_period +1)],
                    "total": 0,
                    "porcentaje": 0
                },
                {
                    "titulo": "sys_sox_reme_complete",
                    "nivel": 50,
                    "periodos": [{"periodo": str(_l), "valor": 0} for _l in range(1, num_period +1)],
                    "total": 0,
                    "porcentaje": 0
                },
            ],
            "totales": {
                "titulo": "sys_sox3_nivel_total",
                "nivel": 0,
                "periodos":  [{"periodo": str(_l), "valor": 0} for _l in range(1, num_period +1)],
                "total": 0,
                "porcentaje": 100
            }
        }
        for status, dep_name, dep_id, month in department_dict.keys():
            index_data = None
            for i, da in enumerate(data_report):
                if dep_name == da["department_name"]:
                    index_data = i
                    break 
            index_pe = _get_index_period(num_period, int(month)) -1
            if index_data is not None:
                if status == 'pending':
                    data_report[index_data]["items"][0]["periodos"][index_pe]["valor"] +=1
                    data_report[index_data]["items"][0]["total"] +=1
                elif status=='under_review':
                    data_report[index_data]["items"][1]["total"] +=1
                    data_report[index_data]["items"][1]["periodos"][index_pe]["valor"] +=1
                else:
                    data_report[index_data]["items"][2]["total"] +=1
                    data_report[index_data]["items"][2]["periodos"][index_pe]["valor"] +=1
                data_report[index_data]["totales"]["total"] += 1
                data_report[index_data]["totales"]["periodos"][index_pe]["valor"] += 1
            else:
                data_report.append({
                    "department_name": dep_name,
                    "department_id": dep_id,
                    "items": [
                        {
                            "titulo": "sys_sox_reme_open",
                            "nivel": 0,
                            "periodos": [{
                                "periodo": str(_l), 
                                "valor": 1 if index_pe == _l and status == 'pending' else 0} for _l in range(1, num_period +1)],
                            
                            "total":  1 if  status == 'pending' else 0,
                            "porcentaje": 0
                        },
                        {
                            "titulo": "sys_sox_reme_process",
                            "periodos": [{
                                "periodo": str(_l), 
                                "valor": 1 if index_pe == _l and status == 'under_review' else 0} for _l in range(1, num_period +1)],
                            "total": 1 if status== 'under_review' else 0,
                            "porcentaje": 0
                        },
                        {
                            "titulo": "sys_sox_reme_complete",
                            "nivel": 50,
                            "periodos": [{"periodo": str(_l), "valor": 1 if index_pe == _l and status == 'complete' else 0} for _l in range(1, num_period +1)],

                            "total": 1 if status== 'complete' else 0,
                            "porcentaje": 0
                        },
                    ],
                    "totales": {
                        "titulo": "sys_sox1_nivel_total",
                        "nivel": 0,
                        "periodos": [{
                            "periodo": str(_l), 
                            "valor": 1 if _l==index_pe else 0} for _l in range(1, num_period +1)],
                        "total": 1,
                        "porcentaje": 100
                    }
                })

            if status== 'pending':
                total_obj['items'][0]["periodos"][index_pe]["valor"] += 1
                total_obj['items'][0]["total"] += 1
                total_obj['totales']["periodos"][index_pe]["valor"] += 1
                total_obj['totales']["total"] += 1
            if status== 'under_review':
                total_obj['items'][1]["periodos"][index_pe]["valor"] += 1
                total_obj['items'][1]["total"] += 1
                total_obj['totales']["periodos"][index_pe]["valor"] += 1
                total_obj['totales']["total"] += 1
            if status== 'complete':
                total_obj['items'][2]["periodos"][index_pe]["valor"] += 1
                total_obj['items'][2]["total"] += 1
                total_obj['totales']["periodos"][index_pe]["valor"] += 1
                total_obj['totales']["total"] += 1
            
        #calculate totals
        for d in data_report:
            #total by periodo
            total_m = d["totales"]["total"] 
            if total_m == 0:
                continue
            for item in d["items"]:
                item["porcentaje"] = round((item["total"] / total_m) * 100, 2)

        if total_obj['totales']["total"]> 0:
            for t_item in total_obj["items"]:
                t_item["porcentaje"] = round((t_item["total"] / total_obj['totales']["total"]) * 100, 2)

        return {
            "periods": list(range(1,num_period+1)),
            "report": data_report,
            "totals": total_obj,
        }

    @api.model 
    def rpe_appetite_level_report(self, department_id, year, cr_peoriod, revision_type):
        domain_mitigation = [
            ('mitigation_date', '<=', (fields.Datetime.today() + relativedelta(months=1, day=1)))
        ]
        if department_id and int(department_id):
            domain_mitigation.append(('risk_id.department_id', '=', int(department_id)))
        if year and int(year):
            domain_mitigation.append(('year', '=', int(year)))
        num_period = 1
        if cr_peoriod:
            if revision_type == 'sys_only_normal':
                domain_mitigation.append(('risk_id.cr_peoriod', '!=', 'fortnightly'))
            if revision_type == 'sys_only_special':
                domain_mitigation.append(('risk_id.cr_peoriod', '=',  'fortnightly'))

            if cr_peoriod == 'month':
                num_period = 12
            if cr_peoriod == 'bi':
                num_period = 6
            if cr_peoriod == 'tri':
                num_period = 4
            if cr_peoriod == 'cua':
                num_period = 3
            if cr_peoriod == 'se':
                num_period = 2
            if cr_peoriod == 'anual':
                num_period = 1

        mitigations = self.env['tyt.risk.mitigation'].search(domain_mitigation)

        department_dict = dict()
        for mitigation in mitigations:
            key = (mitigation.risk_id_department_id.id, mitigation.mr_residual_risk, mitigation.risk_id_quantification, mitigation.risk_id_department_id.display_name, mitigation.month, mitigation.mr_degree_mitigation.value)
            if key in department_dict:
                department_dict[(key)] += 1
            else:
                department_dict[(key)] = 1

                
        data_report = []
        total_obj =  {
            "titulo": "sys_sta_total",
            "periodos":  [{
                "periodo": str(_l), 
                "residual": 0, 
                "asegurado": 0, 
                "apetitos": [],
                "apetito_label": "",
            } for _l in range(1, num_period +1)],
        }
        #apetito
        # bajo: mayoria en 100
        # moderado: queda en 50 
        # alto que en 0
        def _get_apetito_label(apetitos):
            len_100_75 = len([_ for _ in apetitos if _ == 100 or _ == 75])
            len_50 = len([_ for _ in apetitos if _ == 50])
            len_apetitos = len(apetitos)
            if len_apetitos == 0:
                return "Bajo"
            
            if len_apetitos > 0 and len_100_75 / len_apetitos >= 0.5:
                return "Bajo"
            elif len_apetitos > 0 and len_50 / len_apetitos >= 0.5:
                return "Moderado"
            else:
                return "Alto"
        
        for dep_id, residual, quantification, dep_name, month, degree_value in department_dict.keys():
            index_data = None
            insured = quantification - residual 
            for i, da in enumerate(data_report):
                if dep_name == da["department_name"]:
                    index_data = i
                    break 
            index_pe = _get_index_period(num_period, int(month)) - 1
            if index_data is not None:
                data_report[index_data]["periodos"][index_pe]["residual"] += residual
                data_report[index_data]["periodos"][index_pe]["asegurado"] += insured
                data_report[index_data]["periodos"][index_pe]["apetitos"].append(degree_value)

            else: 
                data_report.append({
                    "department_name": dep_name,
                    "department_id": dep_id, 
                    
                    "periodos": [{
                        "periodo": str(_l), 
                        "residual": residual if _l -1 == index_pe else 0,
                        "asegurado": insured if _l -1 == index_pe else 0, 
                        "apetitos": [degree_value],
                        "apetito_label": "", 
                    } for _l in range(1, num_period +1)],
                    
                })

            total_obj["periodos"][index_pe]["residual"] += residual
            total_obj["periodos"][index_pe]["asegurado"] += insured
            total_obj["periodos"][index_pe]["apetitos"].append(degree_value)

            

        for item in data_report:
            for periodo in item["periodos"]:
                periodo["apetito_label"] = _get_apetito_label(periodo["apetitos"])

        for period in total_obj["periodos"]:
            period["apetito_label"] = _get_apetito_label(period["apetitos"])

        return {
            "report": data_report,
            "totales": total_obj,
        }
 

    @api.model 
    def rpe_risk_rating(self, department_id, year, cr_peoriod, revision_type):
        domain_mitigation = [
            ('mitigation_date', '<=', (fields.Datetime.today() + relativedelta(months=1, day=1)))

        ]
        if department_id and int(department_id):
            domain_mitigation.append(('risk_id.department_id', '=', int(department_id)))
        if year and int(year):
            domain_mitigation.append(('year', '=', int(year)))
        num_period = 1
        if cr_peoriod:
            if revision_type == 'sys_only_normal':
                domain_mitigation.append(('risk_id.cr_peoriod', '!=', 'fortnightly'))
            if revision_type == 'sys_only_special':
                domain_mitigation.append(('risk_id.cr_peoriod', '=',  'fortnightly'))

            if cr_peoriod == 'month':
                num_period = 12
            if cr_peoriod == 'bi':
                num_period = 6
            if cr_peoriod == 'tri':
                num_period = 4
            if cr_peoriod == 'cua':
                num_period = 3
            if cr_peoriod == 'se':
                num_period = 2
            if cr_peoriod == 'anual':
                num_period = 1

        mitigations = self.env['tyt.risk.mitigation'].search(domain_mitigation)
         
        department_dict = dict()
        for mitigation in mitigations:
            key = (mitigation.risk_id_department_id.display_name, mitigation.risk_id_department_id.id, mitigation.month, mitigation.before_control, mitigation.after_control)
            if key in department_dict:
                department_dict[(key)] += 1
            else:
                department_dict[(key)] = 1

                
        data_report = []
        INDEX_CONTROL = {
            'severe': 0,
            'higher': 1,
            'significant': 2,
            'minor': 3,
            'insignificant': 4,
        }
        total_obj =  {
            "items": [
                {
                    "titulo": "severe",
                    "title": "Severo",
                    "periodos": [{"periodo": str(_l), "before": 0, "after": 0, "performance": 0} for _l in range(1, num_period +1)],
                },
                {
                    "titulo": "higher",
                    "title": "Mayor",
                    "periodos": [{"periodo": str(_l), "before": 0, "after": 0, "performance": 0} for _l in range(1, num_period +1)],
                },
                {
                    "titulo": "significant",
                    "title": "Significativo",
                    "nivel": 50,
                    "periodos": [{"periodo": str(_l), "before": 0, "after": 0, "performance": 0} for _l in range(1, num_period +1)],
                },
                {
                    "titulo": "minor",
                    "title": "Menor",
                    "periodos": [{"periodo": str(_l), "before": 0, "after": 0, "performance": 0} for _l in range(1, num_period +1)],
                },
                {
                    "titulo": "insignificant",
                    "title": "Insignificate",
                    "periodos": [{"periodo": str(_l), "before": 0, "after": 0, "performance": 0} for _l in range(1, num_period +1)],
                },
            ],
            "totals": [ 0 for _l in range(1, num_period +1)],
        }
        for dep_name, dep_id, month, before_control, after_control in department_dict.keys():
            index_data = None
            _logger.info(f"month {month}")
            for i, da in enumerate(data_report):
                if dep_name == da["department_name"]:
                    index_data = i
                    break 
            index_pe = _get_index_period(num_period, int(month)) -1
            if index_data is not None:
            
                data_report[index_data]["rows"][INDEX_CONTROL.get(before_control)]["periodos"][index_pe]["before"] += 1
                data_report[index_data]["rows"][INDEX_CONTROL.get(after_control)]["periodos"][index_pe]["after"] += 1
                data_report[index_data]["totals"][index_pe] += 1
            else:
                data_report.append({
                    "department_name": dep_name,
                    "department_id": dep_id,
                    "rows": [
                        {
                            "titulo": "severe",
                            "title": "Severo",
                            "periodos": [{
                                "periodo": str(_l), 
                                "before": 1 if before_control== 'severe' and _l-1 == index_pe else 0, 
                                "after": 1 if after_control== 'severe' and _l-1 == index_pe else 0, 
                                "performance": 0} for _l in range(1, num_period +1)],
                        },
                        {
                            "titulo": "higher",
                            "title": "Mayor",
                            "periodos": [{
                                "periodo": str(_l), 
                                "before": 1 if before_control== 'higher' and _l-1 == index_pe else 0, 
                                "after": 1 if after_control== 'higher' and _l-1 == index_pe else 0, 
                                "performance": 0} for _l in range(1, num_period +1)],
                        },
                        {
                            "titulo": "significant",
                            "title": "Significativo",
                            "periodos": [{
                                "periodo": str(_l), 
                                "before": 1 if before_control== 'significant' and _l-1 == index_pe else 0, 
                                "after": 1 if after_control== 'significant' and _l-1 == index_pe else 0,  
                                "performance": 0} for _l in range(1, num_period +1)],

                        },
                        {
                            "titulo": "minor",
                            "title": "Menor",
                            "periodos": [{
                                "periodo": str(_l), 
                                "before": 1 if before_control== 'minor' and _l-1 == index_pe else 0, 
                                "after": 1 if after_control== 'minor' and _l-1 == index_pe else 0, 
                                "performance": 0} for _l in range(1, num_period +1)],
                        },
                        {
                            "titulo": "insignificant",
                            "title": "Insignificate",
                            "periodos": [{
                                "periodo": str(_l), 
                                "before": 1 if before_control== 'insignificant' and _l-1 == index_pe else 0, 
                                "after": 1 if after_control== 'insignificant' and _l-1 == index_pe else 0, 
                                "performance": 0} for _l in range(1, num_period +1)],
                        },
                    ], 
                    "totals": [1 if index_pe == _l -1 else 0 for _l in range(1, num_period +1)],
                })

            total_obj['items'][INDEX_CONTROL.get(before_control)]["periodos"][index_pe]["before"] += 1
            total_obj['items'][INDEX_CONTROL.get(after_control)]["periodos"][index_pe]["after"] += 1
            total_obj['totals'][index_pe] += 1
            
        #calculate totals
        for d in data_report:
            #total by periodo
            for item in d["rows"]:
                for i_p, period in enumerate(item["periodos"]):
                    if d["totals"][i_p] == 0:
                        continue
                    period["performance"] = round((period["after"] / d["totals"][i_p]) * 100, 2)

        for t_item in total_obj["items"]:
            for t_i_p, period in enumerate(t_item["periodos"]):
                if total_obj["totals"][t_i_p]==0:
                    continue
                period["performance"] = round((period["after"] / total_obj["totals"][t_i_p]) * 100, 2)

        return {
            "periods": list(range(1,num_period+1)),
            "report": data_report,
            "totals": total_obj,
        }

