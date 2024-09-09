# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class ProcessDescription(models.Model):
    _name = 'mgmtsystem.process.description'
    _description = 'Procedimiento con descripción'

    name = fields.Char(
        string='Nombre',
        related='process_id.name',
        store=True
    )
    process_id = fields.Many2one(
        string='Procedimiento',
        comodel_name='mgmt.process',
        ondelete='cascade',
        required=True,
    )
    description = fields.Text(
        string='Descripción',
        required=True,
    )


class QualityManual(models.Model):
    _name = 'mgmtsystem.qualitymanual'
    _inherit = ['mgmtsystem.validation.mail']
    _description = 'Manual de calidad'

    name = fields.Char(
        string='Nombre',
        required=True,
    )
    is_template = fields.Boolean(
        string='¿Es plantilla?',
        default=False,
    )
    process_ids = fields.Many2many(
        string='Procedimientos asociados',
        comodel_name='mgmt.process',
        relation='qualitymanual_process_rel',
        column1='process_id',
        column2='qualitymanual_id',
    )

    state = fields.Selection(
        string=u'Estado',
        selection=[
            ('elaborate', 'En elaboración'),
            ('review', 'En revisión'),
            ('validate', 'En validación'),
            ('validate_ok', 'Validado'),
            ('cancel', 'Obsoleto')
        ],
        default='elaborate',
        copy=False,
    )

    def create_action(self, vuser_id):
        action = self.env.ref('hola_calidad.p_mail_activity_action').read()[0]
        self.env.cr.execute("""SELECT id FROM ir_model 
                          WHERE model = %s""", (str(self._name),))
        info = self.env.cr.dictfetchall()
        if info:
            model_id = info[0]['id']
        action['context'] = {
            'default_res_id': self.ids[0],
            'default_res_model': self._name,
            'default_res_model_id': model_id,
            'default_user_id': vuser_id,
        }
        return action

    introduction = fields.Text(
        string='Introducción',
    )
    objective = fields.Text(
        string='Objeto y campo de aplicación',
    )
    scope = fields.Text(
        string='Alcance del sistema de gestión de calidad',
        related='internal_issue_id.scope'
    )
    internal_issue_id = fields.Many2one(comodel_name='mgmtsystem.context.internal_issue',
                                        string='Contexto de la organización',)

    references = fields.Text(
        string='Referencias normativas',
    )
    abbreviation_ids = fields.Many2many(
        string='Terminos y definiciones',
        comodel_name='edition.abbreviation',
        relation='template_qualitymanual_abbreviation_rel',
        column1='abbreviation_id',
        column2='template_id',
    )

    ###################
    def get_link(self, process):
        link = ("<a data-oe-id=%s data-oe-model='mgmt.process' href=#id=%s&model=mgmt.process>%s %s</a>") % (
            process.id, process.id, process.code, process.name)
        return link

    def change_string(self, text):
        for process in self.process_ids:
            a_change = ("//%s//") % (process.code)
            text = text.replace(a_change, self.get_link(process))
        return str(text)

    # Contexto de la organización

    context = fields.Text(string='Contexto de la organización')
    mission = fields.Text(string='Misión', related='internal_issue_id.mission')
    vision = fields.Text(string='Visión', related='internal_issue_id.vision')
    process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_context_d_rel',
                                  string='Procedimiento',)

    context_objective = fields.Text(
        string='4.1 Comprensión de la organización y de su contexto',
    )

    porter_id = fields.Many2one(comodel_name='mgmtsystem.context.external_issue',
                                string='Análisis de Porter',)
    foda_id = fields.Many2one(comodel_name='mgmtsystem.context.swot',
                              string='FODA',)
    pest_id = fields.Many2one(comodel_name='mgmtsystem.context.pest',
                              string='Análisis AMOFHIT/PESTEL',)
    context_context_process_ids = fields.Many2many(comodel_name='mgmt.process', relation='q_context_process_rel',
                                                   string='Procedimiento',)

    context_needs = fields.Text(
        string='4.2 Comprensión de las necesidades y expectativas de las partes interesadas',
    )
    context_needs_process_ids = fields.Many2many(comodel_name='mgmt.process', relation='q_needs_process_rel',
                                                 string='Procedimiento',)

    stakeholders_id = fields.Many2one(comodel_name='mgmtsystem.stakeholders',
                                      string='Matriz de partes interesadas',)

    context_scope = fields.Text(
        string='4.3 Determinación del alcance del sistema de gestión de calidad',
        related='internal_issue_id.scope'
    )

    context_processdescription_ids = fields.Html(
        compute='_compute_context_processdescription_ids', string='4.4 Sistema de gestión de calidad y sus procesos')

    quality_process = fields.Html(
        string='Sistema de Gestión de Calidad y sus procesos')

    process_preview = fields.Html(
        'Mapa de procesos', compute="generate_preview")

    def generate_preview(self):
        report = self.env['ir.actions.report']._get_report_from_name(
            'mgmtsystem_process.reporte_process_hola_calidad_template')
        categs_ids = self.env['mgmt.categ'].search([])
        ids = [x.id for x in categs_ids]
        context = dict(self.env.context)
        result = report.with_context(context).render(ids, data={})
        html = result[0] if result else ''
        self.process_preview = html

    def _compute_context_processdescription_ids(self):
        process_categ_types = self.env['mgmt.categ.type'].search([])
        res = "<table class='table table-bordered'><tr><th>Código</th><th>Nombre</th><th>Descripción</th></tr>"
        for each in process_categ_types:
            code = each.code if each.code else ''
            name = each.name if each.name else ''
            description = each.description if each.description else ''
            res += "<tr><td>" + code + "</td><td>" + name + \
                "</td><td>" + description + "</td></tr>"
        res += "</table>"
        res += "<br></br>"
        process_categ = self.env['mgmt.categ'].search([])
        res += "<table class='table table-bordered'><tr><th>Tipo</th><th>Código</th><th>Nombre</th><th>Descripción</th><th>Creado en</th></tr>"
        for each in process_categ:
            type = each.type.name if each.type else ''
            code = each.code if each.code else ''
            name = each.name if each.name else ''
            description = each.description if each.description else ''
            date = each.create_date.strftime('%d/%m/%Y') if each.create_date else ''

            res += "<tr><td>" + type + "</td><td>" + code + "</td><td>" + name + \
                "</td><td>" + description + "</td><td>" + date + "</td></tr>"
        res += "</table>"

        self.context_processdescription_ids = res

    # fields.Many2many(
    #     string='Sistema de gestión de calidad y sus procesos',
    #     comodel_name='mgmtsystem.process.description',
    #     relation='processdescription_templatequalitymanual_rel',
    #     column1='processdescription_id',
    #     column2='template_id',
    # )

    # Liderazgo
    leader_generalities = fields.Text(
        string='5.1.1 Generalidades',
    )
    leader_clientfocus = fields.Text(
        string='5.1.2 Enfoque al cliente',
    )
    legal_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_legal_d_rel',
                                        string='Procedimiento',)
    legal_ids = fields.Many2many('legal.legal', string='Requisitos Legales',
                                 relation='qlty_legal_rel',)

    opp_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_opp_d_rel',
                                      string='Procedimiento',)
    risk_ids = fields.Many2many('matrix.block.line', relation='qlty_risk_rel',
                                string='Riesgos', domain="[('type', '=', 'risk'), ('state','=','validate')]")
    opp_ids = fields.Many2many('matrix.block.line', string='Oportunidades',
                               relation='qlty_opp_rel', domain="[('type', '=', 'opportunity'), ('state','=','validate')]")

    survey_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_survey_d_rel',
                                         string='Procedimiento',)
    survey_ids = fields.Many2many(
        'survey.survey', relation='qlty_survey_rel', string='Encuestas')

    leader_politic = fields.Text(
        string='5.2.1 Establecimiento de la política de la calidad',
    )
    politic_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_politic_rel',
                                          string='Procedimiento',)
    politic_ids = fields.Many2many('mgmtsystem.context.policy', relation='qlty_policy_rel',
                                   string='Políticas',)

    leader_comunication = fields.Text(
        string='5.2.2 Comunicación de la política de la calidad',
    )
    comunication_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_comu_d_rel',
                                               string='Procedimiento',)
    comunication_plan_id = fields.Many2many(
        'comunication.plan.line', relation='qlty_comuplan_rel', string='Plan de comunicaciones', domain="[('state','=','closed')]")

    leader_rol = fields.Text(
        string='5.3 Roles, responsabilidades y autoridades en la organización',
    )
    rol_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_rol_d_rel',
                                      string='Procedimiento',)
    job_ids = fields.Many2many('hr.job', relation='qlty_job_rel',
                               string='Puestos',)

    # Planificación
    plan_body = fields.Text(string='Planificación')
    plan_riskopp = fields.Text(
        string='6.1 Acciones para abordar riesgos y oportunidades',
    )
    matrix_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_matrix_d_rel',
                                         string='Procedimiento',)
    risk_matrix_ids = fields.Many2many('matrix.matrix', relation='qlty_riskmatrix_rel',
                                       string='Matriz de Riesgos', domain="[('type', '=', 'risk'), ('state','=','validate_ok')]")
    opp_matrix_ids = fields.Many2many('matrix.matrix', string='Matriz de Oportunidades',
                                      relation='qlty_oppmatrix_rel', domain="[('type', '=', 'opportunity'), ('state','=','validate_ok')]")

    plan_scope = fields.Text(
        string='6.2 Objetivos de la calidad y planificación para lograrlos',
    )
    target_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_target_d_rel',
                                         string='Procedimiento',)
    target_ids = fields.Many2many('mgmtsystem.target', relation='qlty_target_rel',
                                  string='Objetivos',)

    plan_changes = fields.Text(
        string='6.3 Planificación de los cambios',
    )
    plan_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_plan_d_rel',
                                       string='Procedimiento',)

    # Apoyo
    support_regeneralities = fields.Text(
        string='7.1.1 Generalidades',
    )
    support_people = fields.Text(
        string='7.1.2 Personas',
    )
    people_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_people_d_rel',
                                         string='Procedimiento',)
    employee_ids = fields.Many2many(
        'hr.employee', relation='qlty_empl_rel', string='Empleados')
    applicant_ids = fields.Many2many(
        'hr.applicant', relation='qlty_applicant_rel', string='Solicitudes de reclutamiento')

    support_infrastructure = fields.Text(
        string='7.1.3 Infraestructura',
    )
    infra_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_infra_d_rel',
                                        string='Procedimiento',)
    infrastructure_ids = fields.Many2many(
        'mgmtsystem.infrastructure', relation='qlty_infra_rel', string='Inventariado',)
    maintenance_plan_ids = fields.Many2many(
        'mgmtsystem.maintenance.plan', relation='qlty_maintplan_rel', string='Programa de mantenimientos',)

    support_environment = fields.Text(
        string='7.1.4 Ambiente para la operación de los procesos',
    )
    environment_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_env_d_rel',
                                              string='Procedimiento',)
    internal_survey_ids = fields.Many2many(
        'survey.survey', relation="qlty_intsurr_rel", string='Encuesta interna')

    support_measure = fields.Text(
        string='7.1.5 Recursos de seguimiento y medición',)
    support_measure_general = fields.Text(
        string='7.1.5.1. Generalidades',)
    support_measure_traz = fields.Text(
        string='7.1.5.2. Trazabilidad de las mediciones',)
    measure_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_measure_d_rel',
                                          string='Procedimiento',)
    calibration_plan_ids = fields.Many2many(
        'mgmtsystem.calibration.plan', relation='qlty_calibration_rel', string='Programa de calibraciones')

    support_knowledge = fields.Text(
        string='7.1.6 Conocimientos de la organización',
    )
    knowledge_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_know_d_rel',
                                            string='Procedimiento',)
    training_plan_ids = fields.Many2many(
        'mgmtsystem.plan', relation='qlty_training_rel', string='Programa de capacitaciones',)

    support_competitions = fields.Text(
        string='7.2 Competencias',
    )
    competitions_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_comp_d_rel',
                                               string='Procedimiento',)
    training_knw_ids = fields.Many2many(
        'mgmtsystem.plan.training', relation='qlty_traknow_rel', string='Plan de capacitaciones recibidas')
    training_survey_ids = fields.Many2many(
        'survey.survey', relation='qlty_trasur_rel', string='Eficacia de la capacitación')

    support_awareness = fields.Text(
        string='7.3 Toma de conciencia',
    )
    awareness_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_aw_d_rel',
                                            string='Procedimiento',)
    training_aw_ids = fields.Many2many(
        'mgmtsystem.plan.training', relation='qlty_trainingaw_rel', string='Plan de capacitaciones')
    training_survey2_ids = fields.Many2one(
        'survey.survey', string='Evaluacíón')

    support_comunication = fields.Text(
        string='7.4 Comunicación',
    )
    comunication_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_comun_d_rel',
                                               string='Procedimiento',)
    training_com_ids = fields.Many2many(
        'comunication.plan.line', relation='qlty_traincom2_rel', string='Plan de comunicaciones',)

    support_generalities = fields.Text(
        string='7.5.1 Generalidades',
    )
    support_creation = fields.Text(
        string='7.5.2 Creación y actualización',
    )
    creation_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_creat_d_rel',
                                           string='Procedimiento',)
    attachment_ids = fields.Many2many(
        'ir.attachment', relation='qlty_attch_rel', string='Documentos')

    def _get_docs(self):
        return self.env['documentary.control'].search([]).ids

    support_control = fields.Text(
        string='7.5.3 Control de la información documentada',
    )
    control_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_control_d_rel',
                                          string='Procedimiento',)
    document_ids = fields.Many2many(
        'documentary.control', relation='qlty_doc_rel', string='Lista Maestra', default=_get_docs)

    # Operacion
    ope_plan = fields.Text(
        string='8.1 Planificación y control operacional',
    )
    ope_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_ope_d_rel',
                                      string='Procedimiento',)
    ope_comunication = fields.Text(
        string='8.2.1 Comunicación con el cliente',
    )
    complaint_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_compla_d_rel',
                                            string='Procedimiento',)
    complaints_ids = fields.Many2many(
        'complaint.complaint', relation='qlty_complaint_rel', string='Reclamos',)

    ope_determination = fields.Text(
        string='8.2.2 Determinación de los requisitos para los productos y servicios',
    )
    determination_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_det_d_rel',
                                                string='Procedimiento',)

    ope_review = fields.Text(
        string='8.2.3 Revisión de los requisitos para los productos y servicios',
    )
    review_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_rev_d_rel',
                                         string='Procedimiento',)

    ope_changes = fields.Text(
        string='8.2.4 Cambios en los requisitos para los productos y servicios',
    )
    changes_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_chang_e_rel',
                                          string='Procedimiento',)

    ope_cgeneral = fields.Text(
        string='8.3.1 Generalidades',
    )
    cgneral_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_cgneral_d_rel',
                                          string='Procedimiento',)

    ope_design = fields.Text(
        string='8.3.2 Planificación del diseño y desarrollo',
    )
    design_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_design_d_rel',
                                         string='Procedimiento',)

    ope_entries = fields.Text(
        string='8.3.3 Entradas para el diseño y desarrollo',
    )
    entries_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_entrie_d_rel',
                                          string='Procedimiento',)

    ope_ddcontrols = fields.Text(
        string='8.3.4 Controles del diseño y desarrollo',
    )
    ddcontrols_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_ddcontrols_d_rel',
                                             string='Procedimiento',)

    ope_ddoutputs = fields.Text(
        string='8.3.5 Salidas del diseño y desarrollo',
    )
    ddoutputs_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_ddoutputs_d_rel',
                                            string='Procedimiento',)

    ope_ddchanges = fields.Text(
        string='8.3.6 Cambios del diseño y desarrollo',
    )
    ddchanges_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_ddchanges_d_rel',
                                            string='Procedimiento',)

    ope_dchanges = fields.Text(
        string='8.4.1 Generalidades',
    )
    dchanges_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_dchanges_e_rel',
                                           string='Procedimiento',)
    stock_inspection_ids = fields.Many2many(
        comodel_name='stock_inspection.stock_inspection', relation='qlty_stkinsp_rel', string='Fichas de inspección', domain="[('state','=','validate')]")

    ope_type = fields.Text(
        string='8.4.2 Tipo y alcance del control',
    )
    ope_type_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_opetype_d_rel',
                                           string='Procedimiento',)
    partner_evaluation_ids = fields.Many2many(
        comodel_name='res.partner.evaluation', relation='qlty_eval_rel', string='Evaluaciones')

    ope_information = fields.Text(
        string='8.4.3 Información para los proveedores externos',
    )
    information_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_infpro_d_rel',
                                              string='Procedimiento',)
    supplier_ids = fields.Many2many(
        comodel_name='res.partner', relation='qlty_supplier_rel', string='Proveedores', domain="[('supplier','=',1)]")

    ope_procontrol = fields.Text(
        string='8.5.1 Control de la producción y de la provisión del servicio',
    )
    procontrol_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_procontrol_d_rel',
                                             string='Procedimiento',)

    ope_proide = fields.Text(
        string='8.5.2 Identificación y trazabilidad',
    )
    proide_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_proide_d_rel',
                                         string='Procedimiento',)

    ope_property = fields.Text(
        string='8.5.3 Propiedad perteneciente a los clientes o proveedores externos',
    )
    property_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_property_d_rel',
                                           string='Procedimiento',)

    ope_preservation = fields.Text(
        string='8.5.4 Preservación',
    )
    preservation_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_preser_d_rel',
                                               string='Procedimiento',)

    ope_postdelivery = fields.Text(
        string='8.5.5 Actividades posteriores a la entrega',
    )
    postdelivery_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_postdel_d_rel',
                                               string='Procedimiento',)

    ope_changecontrol = fields.Text(
        string='8.5.6 Control de los cambios',
    )
    changecontrol_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_changcont_d_rel',
                                                string='Procedimiento',)

    ope_realese = fields.Text(
        string='8.6 Liberación de los productos y servicios',
    )
    release_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_relese_d_rel',
                                          string='Procedimiento',)

    ope_control = fields.Text(
        string='8.7 Control de las salidas no conformes',
    )
    opecontrol_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_opecontrol_d_rel',
                                             string='Procedimiento',)

    # Evaluacion
    eva_tgeneral = fields.Text(
        string='9.1.1 Generalidades',
    )
    tgeneral_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_tgenral_d_rel',
                                           string='Procedimiento',)
    indicator_ids = fields.Many2many(
        comodel_name='mgmtsystem.indicator', relation='qlty_indicator_rel', string='Indicadores')

    eva_tcustomer = fields.Text(
        string='9.1.2 Satisfacción del cliente',
    )
    tcustomer_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_tcustomer_d_rel',
                                            string='Procedimiento',)
    complaint_int_ids = fields.Many2many(
        comodel_name='complaint.complaint', relation='qlty_compint_rel', string='Reclamos internos', domain="[('type','=','customer')]")
    complaint_ext_ids = fields.Many2many(
        comodel_name='complaint.complaint', relation='qlty_compext_rel', string='Reclamos externos', domain="[('type','=','supplier')]")
    eva_survey_ids = fields.Many2many(
        comodel_name='survey.survey', relation='qlty_evasurvey_rel', string='Encuestas')

    eva_tana = fields.Text(
        string='9.1.3 Análisis y evaluación',
    )
    tana_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_tana_d_rel',
                                       string='Procedimiento',)
    eva_taudit = fields.Text(
        string='9.2 Auditoría interna',
    )
    taudit_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_taudit_d_rel',
                                         string='Procedimiento',)
    audit_plan_ids = fields.Many2many(
        comodel_name='audit.plan', relation='qlty_audit_rel', string='Programa de auditorías',)
    eva_rgeneral = fields.Text(
        string='9.3.1 Generalidades',
    )
    rgeneral_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_rgeneal_d_rel',
                                           string='Procedimiento',)
    mgmt_review_ids = fields.Many2many(
        comodel_name='management.review', relation='qlty_mgmre_rel', string='Programa de revisión',)
    mgmt_reviewplan_ids = fields.Many2many(
        comodel_name='management.review.plan', relation='qlty_mgmrepl_rel', string='Revisión por la dirección',)
    eva_rreview = fields.Text(
        string='9.3.2 Entradas de la revisión por la dirección',
    )
    eva_rexist = fields.Text(
        string='9.3.3 Salidas de la revisión por la dirección',
    )

    # Mejora
    imp_general = fields.Text(
        string='10.1 Generalidades',
    )
    imp_nonconfor = fields.Text(
        string='10.2 No conformidad y acción correctiva',
    )
    nonconfor_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_noncofor_d_rel',
                                            string='Procedimiento',)
    action_ids = fields.Many2many(
        comodel_name='mgmtsystem.action', relation='qlty_action_rel', string='Acciones')
    nc_ids = fields.Many2many(
        comodel_name='mgmtsystem.nonconformity', relation='qlty_nc_rel', string='No conformidades')
    imp_improvement = fields.Text(
        string='10.3 Mejora continua',
    )
    impro_process_id = fields.Many2many(comodel_name='mgmt.process', relation='q_impro_d_rel',
                                        string='Procedimiento',)
    action2_ids = fields.Many2many(
        comodel_name='mgmtsystem.action', relation='qlty_action2_rel', string='Acciones')

    release =fields.Text('Liberación de los servicios')
    scope_system=fields.Text('Alcance del sistema de gestión de calidad')
    comunication_plan_process_id=fields.Many2many(comodel_name='comunication.plan.line', relation='relation_comunication_plan',
                                         string='Plan de comunicaciones',)
    comunication_ids = fields.Many2many('comunication.plan.line', relation='qlty_comun_rel', string='Plan de comunicaciones')

    def _get_new_values(self, values):
        """
            @return: dict con valores casteados por el código de proceso separado por //CODE//
        """
        fields = self._fields
        for field in fields:
            value = values.get(str(field), False)
            if value and isinstance(value, str):
                values[str(field)] = self.change_string(value)
        return values

    @api.model
    def create(self, values):
        result = super(QualityManual, self).create(
            self._get_new_values(values))
        return result

    def write(self, values):
        result = super(QualityManual, self).write(self._get_new_values(values))
        return result
