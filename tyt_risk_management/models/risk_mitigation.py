from odoo import models, fields, api
from odoo.exceptions import UserError


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
        string="Asignado a"
    )
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
            ('under_review', 'En revisión'), #amarillo

            ('pending', 'Pendiente'), # when existe some plan action pendient
            ('complete', 'Completado'),
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
        msg = "Enviado a {0} para su revisión".format(self.assigned_to.display_name if self.assigned_to else '')
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
    mr_degree_mitigation = fields.Many2one(
        comodel_name='tyt.risk.degree.mitigation',
        string="Grado de mitigación",
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
            ('ontime', 'A Tiempo') # TODO: Check one use
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
        string="Estatus de mitigación",
    )
    ma_degree_mitigation = fields.Many2one(
        comodel_name='tyt.risk.degree.mitigation',
        string="Grado de mitigación"
    )
    ma_residual_risk = fields.Float(string="Riesgo residual", compute="_compute_ma_residual_risk")

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
        inverse_name='risk_id',
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
                'default_user_id': self.risk_id_owner_id.id,
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

        # Buscamos solo los que no están mitigados aún para ahorrar recursos
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
        if 'status' in vals and vals['status'] == 'mitigated':
            vals['mr_mitigation_date'] = fields.Datetime.now().date()
        return super().write(vals)