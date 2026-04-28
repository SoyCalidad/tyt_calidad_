from odoo import models, fields, api
from odoo.exceptions import UserError

class RiskStage(models.Model):
    _name = 'tyt.risk.stage'
    _description = 'Etapa de Riesgo'
    _order = 'sequence'

    name = fields.Char(string='Nombre de la Etapa', required=True, translate=True)
    sequence = fields.Integer(default=1, help="Orden en el que se mostrará la etapa", string="Order")
    description = fields.Text(string='Descripción')
    active = fields.Boolean(default=True)
    

class RiskDomain(models.Model):
    _name = 'tyt.risk.domain'
    _description = "Dominio del riesgo"

    name = fields.Char(string='Nombre', required=True, translate=True)
    sequence = fields.Integer(default=1, help="Orden en el que se mostrará la etapa", string="Order")
    description = fields.Text(string='Descripción')
    active = fields.Boolean(default=True)
    
class RiskCOSO(models.Model):
    _name="tyt.risk.goal.coso"
    _description = "Objetivo COSO"

    name = fields.Char(string='Nombre', required=True, translate=True)
    sequence = fields.Integer(default=1, help="Orden en el que se mostrará la etapa")
    active = fields.Boolean(default=True)

class RiskAssertion(models.Model):
    _name="tyt.risk.assertion"
    _description = "Aseveraciones"

    name = fields.Char(string='Nombre', required=True, translate=True)
    sequence = fields.Integer(default=1, help="Orden en el que se mostrará la etapa")
    active = fields.Boolean(default=True)

class RiskFinancialStatementCategory(models.Model):
    _name="tyt.risk.financial.statement.category"
    _description = "Categoria estado financiero"

    name = fields.Char(string='Nombre', required=True, translate=True)
    sequence = fields.Integer(default=1, help="Orden en el que se mostrará la etapa")
    active = fields.Boolean(default=True)


class RiskMOComment(models.Model):
    _name = "tyt.risk.mo_comment"
    _description = "Control de documentos"

    name = fields.Char(string="Comentario", )
    
    risk_id = fields.Many2one(
        comodel_name='tyt.risk.management',
        string="Riesgo",
    )


class RiskMOFiles(models.Model):
    _name = "tyt.risk.mo_file"
    _description = "Control de documentos"

    name = fields.Char(string="Nombre", related="file_id.name", store=True)
    file_id = fields.Many2one(
        comodel_name='documents.document',
        domain=[('type', '=', 'binary')],
    )
    
    description = fields.Char(string="Descripción")
    risk_id = fields.Many2one(
        comodel_name='tyt.risk.management',
        string="Riesgo",
    )
    plan_id = fields.Many2one(
        comodel_name='tyt.risk.action.plan',
        string="Plan",
    )
    origin = fields.Selection(
        selection=[
            ('risk', 'Riesgo'),
            ('action_plan', 'Plan de acción')
        ],
        string="Origen"
    )

class RiskMOLink(models.Model):
    _name = "tyt.risk.mo_link"
    _description = "Control de documentos"

    name = fields.Char(string="Enlace", store=True)
 
    description = fields.Char(string="Descripción")
    risk_id = fields.Many2one(
        comodel_name='tyt.risk.management',
        string="Riesgo",
    )
    plan_id = fields.Many2one(
        comodel_name='tyt.risk.action.plan',
        string="Riesgo",
    )
    origin = fields.Selection(
        selection=[
            ('risk', 'Riesgo'),
            ('action_plan', 'Plan de acción')
        ],
        string="Origen"
    )

class PlanAction(models.Model):
    _name = "tyt.risk.action.plan"
    _inherit = ['mail.thread']
    _description = "Plan de acción "
    _order = "id,sequence"

    name = fields.Text(string="Plan de acción")
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Usuario responsable"
    )
    remediation_date = fields.Date(string="Fecha de remediación")
    status = fields.Selection(
        selection=[
            ('pending', 'Pendiente'),
            ('under_review', 'En revisión'), #amarillo
            ('complete', 'Completado'),
        ],
        string="Estatus",
        default="pending"
    )
    sequence = fields.Integer(default=1)
    risk_id = fields.Many2one(
        comodel_name='tyt.risk.management',
        string="Riesgo",
    )
    link_ids = fields.One2many(
        comodel_name='tyt.risk.mo_link',
        inverse_name='plan_id',
        string="Enlaces relacionados",
        domain=[('origin', '=','action_plan')],
        context={'default_origin': 'action_plan'}
    )
    document_ids = fields.One2many(
        comodel_name='tyt.risk.mo_file',
        inverse_name='plan_id',
        string="Documentación soporte",
        domain=[('origin', '=', 'action_plan')],
        context={'default_origin': 'action_plan', }
    )
    origin = fields.Selection(
        selection=[
            ('review', 'Revisión'),
            ('audit', 'Auditoria'),
        ],
    )

    def action_send_reject(self,):
        self.ensure_one()
        self.write({
            'status': 'pending',
        })

    def action_send_complete(self,):
        self.ensure_one()
        self.write({
            'status': 'complete',
        })

    def action_send_review(self,):
        self.ensure_one()
        self.write({
            'status': 'under_review',
        })

    def action_attendance_action_plan(self,):
        self.ensure_one()
        view_id = self.env.ref('tyt_risk_management.view_risk_action_plan_attendance_form').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Plan de acción',
            'res_model': 'tyt.risk.action.plan',
            'view_mode': 'form',
            'target': 'new',
            'res_id': self.id,
            'views': [(view_id, 'form')], 
            'context': {
            }
        }

MESES = [
            ('01', 'Enero'),
            ('02', 'Febrero'),
            ('03', 'Marzo'),
            ('04', 'Abril'),
            ('05', 'Mayo'),
            ('06', 'Junio'),
            ('07', 'Julio'),
            ('08', 'Agosto'),
            ('09', 'Septiembre'),
            ('10', 'Octubre'),
            ('11', 'Noviembre'),
            ('12', 'Diciembre'),
        ]

class RiskManagement(models.Model):
    _name = 'tyt.risk.management'
    _description = 'Riesgo Operativo'
    _inherit = ['mail.thread']

    name = fields.Text(string='Riesgo asociado', required=True)
    active = fields.Boolean(default=True, string="Activo")
    
    department_id = fields.Many2one(
        comodel_name='hr.department',
        string="Sitio",
    )
    domain_id = fields.Many2one(
        comodel_name='tyt.risk.domain',
        string="Dominio"
    )
    process_id = fields.Many2one(
        'tyt.business.process', 
        string='Proceso', 
        required=True,
        domain="[('active', '=', True)]" # Solo procesos activos
    )
    subprocess_id = fields.Many2one(
        'tyt.business.process', 
        string='Sub Proceso', 
        required=True,
        domain="[('active', '=', True), ('level', '=',2)]"
    )
    control_objective = fields.Text(string="Objetivo de control")
    control_activity = fields.Text(string="Actividad de control")
    owner_id = fields.Many2one(
        comodel_name='res.users',
        string="Dueño",
        tracking=True,
    )
    reviewer_id = fields.Many2one(
        comodel_name='res.users',
        string="Revisor",
        tracking=True,
    )
    auditor_id = fields.Many2one(
        comodel_name='res.users',
        string="Auditor",
        tracking=True,
    )
    goal_coso_ids = fields.Many2many(
        comodel_name='tyt.risk.goal.coso',
        string="Objetivo COSO",

    )
    assertion_ids = fields.Many2many(
        comodel_name='tyt.risk.assertion',
        string="Aseveraciones"
    )
    frequency_id = fields.Many2one(
        comodel_name='tyt.catalog.frequency',
        string="Frecuencia"
    )
    fsc_id = fields.Many2one(
        comodel_name='tyt.risk.financial.statement.category',
        string="Categoría del estado financiero",
    )
    quantification = fields.Float(string="Cuantificación")
    type_ma = fields.Selection(selection=[
        ('manual', 'Manual'),
        ('automatic', 'Automático')
    ], string="Manual o Automático")
    system_control = fields.Char(string="Sistema de control")
    required_load_initial_files = fields.Boolean(string="Require carga inicial de archivos")
    required_mitigation_files = fields.Boolean(string="Require archivos de mitigación")
    type_pd = fields.Selection(selection=[
        ('preventive', 'Preventivo'),
        ('detective', 'Detectivo')
    ], string="Preventivo o Detectivo")
    type_cf = fields.Selection(selection=[
        ('yes', 'Si'),
        ('no', 'No')
    ], string="Control de fraude")
    low_scenery = fields.Text(string="Escenario bajo ")
    middle_scenery = fields.Text(string="Escenario medio ")
    high_scenery = fields.Text(string="Escenario alto ")
    impact = fields.Selection(
        selection=[
            ('low', 'Bajo'),
            ('medium', 'Medio'),
            ('high', 'Alto')
        ],
        string="Impacto"
    )
    occurrence = fields.Selection(
        selection=[
            ('low', 'Bajo'),
            ('medium', 'Medio'),
            ('high', 'Alto')
            
        ],
        string="Ocurrencia"
    )
    is_scheduled = fields.Boolean(string="Programada", default=False)
    status = fields.Selection(
        selection=[
            ('unmitigated', 'No mitigado'),
            ('review', 'En revisión', ),
            ('mitigated', 'Mitigado'),
            ('filled', 'Completado'),
            ('pending', 'Pendiente'),
            ('partial_mitigated', 'Parcialmente mitigado')
        ],
        string="Estatus",
        default="unmitigated",
    )
    assigned_to = fields.Many2one(
        comodel_name='res.users',
        string="Asignado a"
    )
    period_str = fields.Char(string="Periodo")
    activity_state = fields.Selection(
        selection=[
            ('mitigation', 'Mitigación'),
            ('action_plan', 'Plan de acción'),
            ('unmitigated', 'No mitigado'), 
        ],
        default='unmitigated',
        string="Actividad",
        tracking=True,
    )
    type_risk = fields.Char(default="Ventas", string="Tipo")
    value_risk = fields.Float(default=500000, string="Valor")

    def open_reviewer_guide(self):
        return {
            "type": "ir.actions.client",
            "tag": "tyt_risk_management.reviewer_guide",
            'name': 'Guía del revisor',
            
            "target": "new",  
        }

    def action_scheduled(self):
        self.ensure_one()
        if not self.cr_month or not self.cr_year:
            raise UserError("Debe ingresar el mes y el año")
        self.write({
            'is_scheduled': True, 
            'assigned_to': self.reviewer_id,
            'activity_state': 'mitigation',    
        })

    #confi revision
    cr_peoriod = fields.Selection(
        selection=[
            ('fortnightly', 'Quincenal'),
            ('month', 'Mensual'),
            ('bi', 'Bimestral'),
            ('tri', 'Trimestral'),
            ('cua', 'Cuatrimestral'),
            ('se', 'Semestral'),
            ('anual', 'Anual'),
        ],
        string="Periodo",
    )
    cr_month = fields.Selection(
        selection=MESES,
        string="Mes inicial"
    )
    cr_year = fields.Integer(string="Año incial")
    cr_month_result = fields.Char(
        string="Meses del periodo",
        compute="_compute_month_result",
        store=False
    )

    @api.depends('cr_month', 'cr_peoriod')
    def _compute_month_result(self):
        mapa_saltos = {
            'fortnightly': 1,
            'month': 1,
            'bi': 2,
            'tri': 3,
            'cua': 4,
            'se': 6,
            'anual': 12,
        }

        meses_dict = dict(MESES)

        for record in self:
            if not record.cr_month or not record.cr_peoriod:
                record.cr_month_result = ""
                continue

            salto = mapa_saltos.get(record.cr_peoriod, 1)
            mes_inicio = int(record.cr_month)

            meses = []
            for i in range(0, 12, salto):
                mes_calc = ((mes_inicio - 1 + i) % 12) + 1
                key = f"{mes_calc:02d}"
                meses.append(meses_dict[key])

            record.cr_month_result = " - ".join(meses)

    #mitigation owner
    mo_document_ids = fields.One2many(
        comodel_name='tyt.risk.mo_file',
        inverse_name='risk_id',
        string="Documentación soporte",
        domain=[('origin', '=', 'risk')],
    )
    mo_link_ids = fields.One2many(
        comodel_name='tyt.risk.mo_link',
        inverse_name='risk_id',
        string="Enlaces relacionados",
        domain=[('origin', '=', 'risk')]
    )
    mo_comment_ids = fields.One2many(
        comodel_name='tyt.risk.mo_comment',
        inverse_name='risk_id',
        string="Comentarios"
    )

    mo_comment_ids_count = fields.Integer(string="N° comentarios", compute="_compute_mo_comment_ids_count")
    mo_period_str = fields.Char(string="Periodo calc", compute="_compute_mo_period_str")


    @api.depends('cr_month', 'cr_year')
    def _compute_mo_period_str(self):
        for record in self:
            if record.is_scheduled and record.cr_month and record.cr_year:
                mes = record.cr_month.zfill(2)
                anio = str(record.cr_year)

                if record.cr_peoriod == 'fortnightly':
                    record.mo_period_str = f"01-{mes}-{anio} al 09-{mes}-{anio}"
                else:
                    record.mo_period_str = f"01-{mes}-{anio} al 11-{mes}-{anio}"
            else:
                record.mo_period_str = False



    @api.depends('mo_comment_ids')
    def _compute_mo_comment_ids_count(self):
        for record in self:
            record.mo_comment_ids_count = len(record.mo_comment_ids)


    #mitigation reviewer
    mr_period_str = fields.Char(string="Periodo revision", compute="_compute_mr_period_str")
    @api.depends('cr_month', 'cr_year')
    def _compute_mr_period_str(self):
        for record in self:
            if record.is_scheduled and record.cr_month and record.cr_year:
                mes = record.cr_month.zfill(2)
                anio = str(record.cr_year)
                if record.cr_peoriod == 'fortnightly':
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
    mr_degree_mitigation = fields.Selection(
        selection=[
            ('0', '0%'),
            ('25', '25%'),
            ('50', '50%'),
            ('75', '75%'),
            ('100', '100%'),
        ],
        string="Grado de mitigación"
    )
    mr_residual_risk = fields.Float(string="Riesgo residual", compute="_compute_mr_residual_risk")

    @api.depends('quantification', 'mr_degree_mitigation')
    def _compute_mr_residual_risk(self):
        for record in self:
            if record.quantification and record.mr_degree_mitigation:
                record.mr_residual_risk = ((100 - int(record.mr_degree_mitigation)) * record.quantification) / 100
            else:
                record.mr_residual_risk = 0



    @api.onchange('mr_status_mitigation')
    def _onchange_mr_status_mitigation(self):
        if self.mr_status_mitigation:
            if self.mr_status_mitigation == 'unmitigated':
                self.mr_degree_mitigation = '0'
            if self.mr_status_mitigation == 'partialmitigated':
                self.mr_degree_mitigation = '25'
            if self.mr_status_mitigation == 'mitigated':
                self.mr_degree_mitigation = '100'
        else:
            self.mr_degree_mitigation = False

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
    mr_level_compliance = fields.Char(string="Grado de cumplimiento", default="Programado")
    mr_action_plan_ids = fields.One2many(
        comodel_name='tyt.risk.action.plan',
        inverse_name='risk_id',
        string="Plan de acción",
        domain=[('origin', '=', 'review')]

    )
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
        if self.mr_degree_mitigation == '0':
            self.maturity_level = 'none'
        if self.mr_degree_mitigation == '25':
            self.maturity_level = 'initial'
        if self.mr_degree_mitigation == '50':
            self.maturity_level = 'limited'
        if self.mr_degree_mitigation == '75':
            self.maturity_level = 'defined'
        if self.mr_degree_mitigation == '100':
            self.maturity_level = 'optimize'

    
    #mitigation audit
    ma_period_str = fields.Char(string="Periodo revision", compute="_compute_ma_period_str")
    @api.depends('cr_month', 'cr_year')
    def _compute_ma_period_str(self):
        for record in self:
            if record.is_scheduled and record.cr_month and record.cr_year:
                mes = record.cr_month.zfill(2)
                anio = str(record.cr_year)
                if record.cr_peoriod == 'fortnightly':
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
    ma_degree_mitigation = fields.Selection(
        selection=[
            ('0', '0%'),
            ('25', '25%'),
            ('50', '50%'),
            ('75', '75%'),
            ('100', '100%'),
        ],
        string="Grado de mitigación"
    )
    ma_residual_risk = fields.Float(string="Riesgo residual", compute="_compute_ma_residual_risk")

    @api.depends('quantification', 'ma_degree_mitigation')
    def _compute_ma_residual_risk(self):
        for record in self:
            if record.quantification and record.ma_degree_mitigation:
                record.ma_residual_risk = ((100 - int(record.ma_degree_mitigation)) * record.quantification) / 100
            else:
                record.ma_residual_risk = 0



    @api.onchange('ma_status_mitigation')
    def _onchange_ma_status_mitigation(self):
        if self.ma_status_mitigation:
            if self.ma_status_mitigation == 'unmitigated':
                self.ma_degree_mitigation = '0'
            if self.ma_status_mitigation == 'partialmitigated':
                self.ma_degree_mitigation = '25'
            if self.ma_status_mitigation == 'mitigated':
                self.ma_degree_mitigation = '100'
        else:
            self.ma_degree_mitigation = False

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
        if self.ma_degree_mitigation == '0':
            self.ma_maturity_level = 'none'
        if self.ma_degree_mitigation == '25':
            self.ma_maturity_level = 'initial'
        if self.ma_degree_mitigation == '50':
            self.ma_maturity_level = 'limited'
        if self.ma_degree_mitigation == '75':
            self.ma_maturity_level = 'defined'
        if self.ma_degree_mitigation == '100':
            self.ma_maturity_level = 'optimize'

    


    stage_id = fields.Many2one(
        'tyt.risk.stage', 
        string='Etapa', 
        group_expand='_read_group_stage_ids', # Para que salgan todas las columnas en Kanban
        tracking=True,
        index=True,
        default=lambda self: self.env['tyt.risk.stage'].search([], limit=1)
    )
    
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        # Esta función hace que en la vista Kanban aparezcan todas las etapas 
        return self.env['tyt.risk.stage'].search([('active', '=', True)])
    

    def action_create_action_plan(self,):
        self.ensure_one()
        self.write({
            'activity_state': 'action_plan',
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
                'default_risk_id': self.id,
                'default_user_id': self.owner_id.id,
                'default_origin': 'review',
            }
        }

    def action_create_action_plan_audit(self,):
        self.ensure_one()
        self.write({
            'activity_state': 'action_plan',
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
                'default_risk_id': self.id,
                'default_user_id': self.owner_id.id,
                'default_origin': 'audit',
            }
        }




    def action_notify_revision(self,):
        #open wizard to write coment and send email
        msg = "Enviado a {0} para su revisión".format(self.assigned_to.display_name if self.assigned_to else '')

        return {
            'type': 'ir.actions.act_window',
            'name': 'Notificar',
            'res_model': 'tyt.risk.notification.revision',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_risk_id': self.id,
            }
        }
    #     return {
    #     'type': 'ir.actions.client',
    #     'tag': 'display_notification',
    #     'params': {
    #         'title': 'Éxito',
    #         'message': 'El proceso se ejecutó correctamente',
    #         'type': 'success',  # success, warning, danger
    #         'sticky': False,
    #     }
    # }


