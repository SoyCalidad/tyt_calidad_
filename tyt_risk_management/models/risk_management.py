from odoo import models, fields, api
from odoo.exceptions import UserError

from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import logging

_logger = logging.getLogger(__name__)

class RiskDegreeMitigation(models.Model):
    _name = "tyt.risk.degree.mitigation"
    _description = "Grado de mitigación"

    name = fields.Char(string='Nombre', required=True,  )
    sequence = fields.Integer(default=1, help="Orden en el que se mostrará la etapa", string="Order")
    description = fields.Text(string='Descripción')
    active = fields.Boolean(default=True)
    status = fields.Selection(
        selection=[
            ('unmitigated', 'No Mitigado'),
            ('partialmitigated', 'Parcialmente Mitigado'),
            ('mitigated', 'Mitigado'),
        ],
        string="Estatus de mitigación",
    )
    value = fields.Integer(default=0)


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
    mitigation_id = fields.Many2one(
        comodel_name='tyt.risk.mitigation',
        string="Mitigación",
    )
    action_plan_id = fields.Many2one(
        comodel_name='tyt.risk.action.plan',
        string="Plan de acción ",
        ondelete="cascade",
    )
    


class RiskMOFiles(models.Model):
    _name = "tyt.risk.mo_file"
    _description = "Control de documentos"

    name = fields.Char(string="Nombre", related="file_id.name", store=True)
    file_id = fields.Many2one(
        comodel_name='documents.document',
        domain=[('type', '=', 'binary')],
        string="Archivo",
    )
    
    description = fields.Char(string="Descripción")
    risk_id = fields.Many2one(
        comodel_name='tyt.risk.management',
        string="Riesgo",
    )
    mitigation_id = fields.Many2one(
        comodel_name='tyt.risk.mitigation',
        string="Mitigación",
    )
    
    plan_id = fields.Many2one(
        comodel_name='tyt.risk.action.plan',
        string="Plan",
    )
    origin = fields.Selection(
        selection=[
            ('risk', 'Riesgo'),
            ('action_plan', 'Plan de acción'),
            ('mitigation_owner', 'Mitigación Dueño')
        ],
        string="Origen"
    )

    def _default_folder(self):
        folder = self.env.ref(
            'tyt_risk_management.folder_risk_management',
            raise_if_not_found=False
        )
        return folder or False
    
    default_folder = fields.Many2one(
        comodel_name='documents.document',
        default=_default_folder,
    )


    def action_open_file(self):
        self.ensure_one()
        if not self.file_id or not self.file_id.access_url:
            return
        if self.file_id.mimetype in (
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/msword',                                                      # doc
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'application/vnd.ms-excel',                                                # xls
            ):
            return self.file_id.sudo().action_open_document_in_office()

        return {
            'type': 'ir.actions.act_url',
            'url': self.file_id.access_url,
            'target': 'new',
        }

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
    mitigation_id = fields.Many2one(
        'tyt.risk.mitigation', 
        string='Mitigación de Riesgo',
        ondelete='cascade', 
    )
    #origen is not necesary
    origin = fields.Selection(
        selection=[
            ('risk', 'Riesgo'),
            ('action_plan', 'Plan de acción'),
            ('mitigation_owner', 'Mitigación Dueño'),

        ],
        string="Origen"
    )

MAPA_SALTOS = {
    'fortnightly': 1,
    'month': 2,
    'bi': 4,
    'tri': 6,
    'cua': 8,
    'se': 12,
    'anual': 24,
}
class PlanAction(models.Model):
    _name = "tyt.risk.action.plan"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Plan de acción "
    _order = "id,sequence"

    active = fields.Boolean(string="Activo", default=True)
    name = fields.Text(string="Plan de acción")
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Usuario responsable"
    )
    current_user = fields.Many2one(
        comodel_name='res.users',
        compute='_compute_current_user',
    )

    def _compute_current_user(self):
        for rec in self:
            rec.current_user = self.env.user
    
    remediation_date = fields.Date(string="Fecha de remediación")
    status = fields.Selection(
        selection=[
            ('pending', 'Pendiente'),
            ('under_review', 'En revisión'), #amarillo
            ('complete', 'Completado'),
            ('rejected', 'Rechazado'), 
        ],
        string="Estatus",
        default="pending",
        tracking=True,
    )
    sequence = fields.Integer(default=1)
    risk_id = fields.Many2one(
        comodel_name='tyt.risk.management',
        string="Riesgo",
    )
    risk_id_id = fields.Integer(
        related="risk_id.id",
        store=True,
        string="ID Riesgo"
    ) 
    mitigation_id = fields.Many2one(
        comodel_name='tyt.risk.mitigation', 
        string='Mitigación', 
        ondelete='cascade')
    mitigation_id_period_str = fields.Char(
        related='mitigation_id.period_str'
    )
    mitigation_id_year = fields.Integer(
        related='mitigation_id.year'
    )
    mitigation_id_month = fields.Selection(
        related='mitigation_id.month'
    )
    #data related to risk
    risk_id_subprocess_id = fields.Many2one(
        related="risk_id.subprocess_id",
        store=True
    )

    risk_id_process_id = fields.Many2one(
        related="risk_id.process_id",
        string="Proceso",
        store=True,

    )
    risk_id_name = fields.Text(
        related="risk_id.name",
        store=True,
    )
    risk_id_department_id = fields.Many2one(
        related="risk_id.department_id",
        store=True,
    )
    risk_id_domain_id = fields.Many2one(
        related="risk_id.domain_id",
        store=True,
    )
    risk_id_pdomain_id = fields.Many2one(
        related="risk_id.pdomain_id",
        store=True,
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

    comment_ids = fields.One2many(
        comodel_name='tyt.risk.mo_comment',
        inverse_name='action_plan_id',
        string="Comentarios"
    )


    def _send_notification_email(self, mitigation, email_to, plan_action_name):
        # Datos para el correo
        current_user = self.env.user.display_name
        reviewer_email = mitigation.risk_id_reviewer_id.email 
        status_label = dict(mitigation._fields['status'].selection).get(mitigation.status, mitigation.status)
        
        if not email_to:
            return # O lanza un ValidationError si es obligatorio

        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        # Formateo del cuerpo en HTML (Tabla invertida)
        body_html = f"""
            <h3>Actividad asignada</h3>
            <table border="1" class="table" style="border-collapse: collapse; width: 100%; font-family: sans-serif;">
                <tr>
                    <th style="padding: 8px; background-color: #f2f2f2; text-align: left;">Actividad</th>
                    <td style="padding: 8px;">Plan de acción</td>
                </tr>
                <tr>
                    <th style="padding: 8px; background-color: #f2f2f2; text-align: left;">Riesgo</th>
                    <td style="padding: 8px;">R-{mitigation.risk_id_id} - {mitigation.risk_id_domain_id.display_name or ''}</td>
                </tr>
                <tr>
                    <th style="padding: 8px; background-color: #f2f2f2; text-align: left;">Plan de acción</th>
                    <td style="padding: 8px;">{plan_action_name}</td>
                </tr>
                <tr>
                    <th style="padding: 8px; background-color: #f2f2f2; text-align: left;">Estatus</th>
                    <td style="padding: 8px;">Pendiente</td>
                </tr>
                <tr>
                    <th style="padding: 8px; background-color: #f2f2f2; text-align: left; width: 30%;">De</th>
                    <td style="padding: 8px;">{current_user}</td>
                </tr>
                <tr>
                    <th style="padding: 8px; background-color: #f2f2f2; text-align: left;">Comentario</th>
                    <td style="padding: 8px;"></td>
                </tr>
            </table>
            <p>Estimado usuario, por favor revise sus actividades pendientes en la plataforma.</p>
            <div class="row justify-content-center">
            <a href="{base_url}" target="_blank" rel="noopener noreferrer" data-auth="NotApplicable" style="text-decoration: none; display: inline-block; color: rgb(255, 255, 255) !important; background-color: rgb(93, 71, 161) !important; border-radius: 4px; width: auto; border-width: 1px; border-style: solid; border-color: rgb(15, 11, 91); padding-top: 0px; padding-bottom: 5px; font-family: Arial, &quot;Helvetica Neue&quot;, Helvetica, sans-serif; text-align: center; word-break: keep-all;" data-linkindex="0" title="{base_url}" data-ogsb="rgb(15, 11, 91)"><span style="padding-left:20px; padding-right:20px; font-size:24px; display:inline-block; letter-spacing:normal"><span style="font-size:16px; margin:0px; line-height:2; word-break:break-word"><strong><span style="font-size:24px; line-height:48px">ODOO TYT</span></strong></span></span></a> 
            
            </div>
        """

        # Crear y enviar el correo
        email_from = self.env.user.email_formatted or self.env.company.email_formatted
        if email_from:
            mail_values = {
                'subject': f'Plan de acción R-{mitigation.risk_id_id}',
                'body_html': body_html,
                'email_to': email_to,
                'email_from': email_from,
            }
            
            # Creamos el registro de correo y lo enviamos inmediatamente
            self.env['mail.mail'].sudo().create(mail_values).send()


    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            if rec.mitigation_id:
                email_to = rec.user_id.email_formatted 
                plan_action_name = rec.display_name
                self._send_notification_email(rec.mitigation_id, email_to, plan_action_name)

        return records

    def action_view_mitigation(self):
        self.ensure_one() 
        view_id = self.env.ref('tyt_risk_management.view_risk_mitigation_my_activity_form').id

        return {
            'name': 'Plan de acción',
            'type': 'ir.actions.act_window',
            'res_model': 'tyt.risk.mitigation',
            'view_mode': 'form',
            'res_id': self.mitigation_id.id, 
            'target': 'current', 
            'views': [(view_id, 'form')], 

        }

    def action_send_reject(self,):
        self.ensure_one()
        if self.mitigation_id:
            others_plan = self.env['tyt.risk.action.plan'].search_count([
                ('mitigation_id', '=', self.mitigation_id.id),
                ('status', '=', 'under_review'),
                ('id', '!=', self.id),
            ])
            if others_plan == 0:
                if self.mitigation_id.status == 'mitigated': 
                    pass 
                else:
                    self.mitigation_id.status = 'rejected'
        self.write({
            'status': 'rejected',
        })

    def action_send_complete(self,):
        self.ensure_one()
        self.write({
            'status': 'complete',
        })

    def action_send_review(self,):
        self.ensure_one()
        if self.mitigation_id:
            others_plan = self.env['tyt.risk.action.plan'].search_count([
                ('mitigation_id', '=', self.mitigation_id.id),
                ('id', '!=', self.id),
            ])
            if others_plan == 0:
                if self.mitigation_id.status == 'mitigated': 
                    pass 
                else:
                    self.mitigation_id.status = 'under_review'
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
        string="Dominio (obsoleto)"
    )
    pdomain_id = fields.Many2one(
        comodel_name='tyt.business.process',
        string="Dominio",
        tracking=True,
    )
    process_id = fields.Many2one(
        'tyt.business.process', 
        string='Proceso', 
        required=True,
        domain="[('active', '=', True)]",
        tracking=True,
    )
    subprocess_id = fields.Many2one(
        'tyt.business.process', 
        string='Sub Proceso', 
        required=True,
        tracking=True,
        domain="[('active', '=', True), ('level', '=',3)]"
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
        string="Impacto",
        tracking=True,
    )
    occurrence = fields.Selection(
        selection=[
            ('low', 'Bajo'),
            ('medium', 'Medio'),
            ('high', 'Alto')
            
        ],
        string="Ocurrencia",
        tracking=True,
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
    # period_str = fields.Char(string="Periodo")
     
    type_risk = fields.Char(default="Ventas", string="Tipo")
    value_risk = fields.Float(default=500000, string="Valor")

    def open_reviewer_guide(self):
        return {
            "type": "ir.actions.client",
            "tag": "tyt_risk_management.reviewer_guide",
            'name': 'Guía del revisor',
            
            "target": "new",  
        }

    def _get_mitigation_dates(self):
        self.ensure_one()

        start_date = date(self.cr_year, int(self.cr_month), 1)
        today = fields.Date.today()

        frequencies = {
            'month': 1,
            'bi': 2,
            'tri': 3,
            'cua': 4,
            'se': 6,
            'anual': 12,
        }

        dates = []

        if self.cr_peoriod == "fortnightly":
            current = start_date

            while current <= today:

                # Primera quincena: 01 -> 15
                first_initial = current.replace(day=1)
                first_limit = current.replace(day=15)

                if first_limit <= today:
                    dates.append((first_initial, first_limit))

                # Segunda quincena: 15 -> último día
                second_initial = current.replace(day=16)
                second_limit = current + relativedelta(day=31)

                if second_limit <= today:
                    dates.append((second_initial, second_limit))

                current += relativedelta(months=1)

        else:
            step = frequencies[self.cr_peoriod]

            current = start_date

            while current <= today:
                limit_date = current + relativedelta(day=31)

                dates.append((current, limit_date))

                current += relativedelta(months=step)

        return dates

    def _generate_missing_mitigations(self):
        activity_type = self.env.ref("mail.mail_activity_data_todo")

        today = fields.Date.today()

        for risk in self:

            for initial_date, limit_date in risk._get_mitigation_dates():

                mitigation = self.env["tyt.risk.mitigation"].search([
                    ("risk_id", "=", risk.id),
                    ("active", "=", True),
                    ("initial_date", "=", initial_date),
                ], limit=1)

                if mitigation:
                    _logger.info(f"exist mitigation {initial_date}")
                    continue

                mitigation = self.env["tyt.risk.mitigation"].create({
                    "risk_id": risk.id,
                    "initial_date": initial_date,
                    "mitigation_date": datetime.combine(limit_date, datetime.min.time()),
                    "year": initial_date.year,
                    "month": str(initial_date.month),
                    "assigned_to": risk.owner_id.id,
                })

                if (
                    limit_date.year == today.year
                    and limit_date.month == today.month
                ):
                    mitigation.activity_schedule(
                        activity_type_id=activity_type.id,
                        summary="Revisar riesgo",
                        note="Debe cargar la información de la mitigación del dueño.",
                        user_id=risk.owner_id.id,
                        date_deadline=initial_date + timedelta(days=3),
                    )

    def action_scheduled(self):
        for risk in self:
            if not risk.cr_month or not risk.cr_year or not risk.cr_peoriod:
                raise UserError("Debe ingresar el mes y el año.")

            risk.is_scheduled = True

            risk._generate_missing_mitigations()

    @api.model
    def cron_generate_mitigations(self):
        risks = self.search([
            ("is_scheduled", "=", True),
            ("active", "=", True),
        ])

        risks._generate_missing_mitigations()

    @api.model 
    def update_access_folder(self):
        partners = {}
        for rec in self.search([]):
            if rec.owner_id.partner_id and not rec.owner_id.partner_id in partners:
                partners[rec.owner_id.partner_id] = ("edit", False)
            if rec.reviewer_id.partner_id and not rec.reviewer_id.partner_id in partners:
                partners[rec.reviewer_id.partner_id] = ("edit", False)
            if rec.auditor_id.partner_id and not rec.auditor_id.partner_id in partners:
                partners[rec.auditor_id.partner_id] = ("edit", False)

        folder = self.env.ref('tyt_risk_management.folder_risk_management')
        if folder:
            folder.action_update_access_rights(partners=partners)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)

        self.update_access_folder()

        for rec in records:
            if rec.pdomain_id and rec.pdomain_id.level!=1:
                rec.pdomain_id.parent_id = False 

            if rec.process_id and rec.process_id.level!=2 and rec.pdomain_id:
                rec.process_id.parent_id = rec.pdomain_id 

            if rec.subprocess_id and rec.subprocess_id.level!=3 and rec.process_id:
                rec.subprocess_id.parent_id = rec.process_id 

        return records

    def write(self, vals):

        res = super().write(vals)

        if 'owner_id' in vals or 'reviewer_id' in vals or 'auditor_id' in vals:
            self.update_access_folder()


        return res


    def _get_end_month(self, month, cr_period):
        if month==2:
            if cr_period=='fortnightly':#quincenal
                return 15 
            else:
                return 28
        else:
            if cr_period == 'fortnightly':
                return 15
            else:
                return 30

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

    quadrant = fields.Integer(
        string="Cuadrante",
        compute="_compute_quadrant",
        store=True 
    )

    @api.depends('impact', 'occurrence')
    def _compute_quadrant(self):
        for rec in self:
            if rec.impact == 'high' and rec.occurrence== 'high':
                rec.quadrant = 9
            elif rec.impact == 'medium' and rec.occurrence== 'high':
                rec.quadrant = 8
            elif rec.impact == 'high' and rec.occurrence== 'medium':
                rec.quadrant = 7
            elif rec.impact == 'low' and rec.occurrence== 'high':
                rec.quadrant = 6
            elif rec.impact == 'medium' and rec.occurrence== 'medium':
                rec.quadrant = 5
            elif rec.impact == 'high' and rec.occurrence== 'low':
                rec.quadrant = 4
            elif rec.impact == 'low' and rec.occurrence== 'medium':
                rec.quadrant = 3
            elif rec.impact == 'medium' and rec.occurrence== 'low':
                rec.quadrant = 2
            else:
                rec.quadrant = 1
                