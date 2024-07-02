from odoo import api, fields, models, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError
from lxml import etree


class Context(models.Model):
    _name = 'mgmtsystem.context'

    name = fields.Char(string='Nombre')
    date = fields.Date(string='Fecha de Creación')
    current_internal_issues = fields.Char(
        string='Factores internos vigentes', compute='_compute_internal_edition')
    current_external_issues = fields.Char(
        string='Análisis de Porter vigentes', compute='_compute_external_edition')

    @api.depends('name')
    def _compute_internal_edition(self):
        for record in self:
            document = self.env['mgmtsystem.context.internal_issue'].search([
                ('state', '=', 'validate_ok'),
            ], order='id desc', limit=1)
            if document:
                record.current_internal_issues = _("<a data-oe-id=%s data-oe-model='mgmtsystem.context.internal_issue' href=#id=%s&model=mgmtsystem.context.internal_issue>%s</a> vigente desde %s") % (
                    document.id, document.id, document.name, document.date_validate)
            else:
                record.current_internal_issues = 'No existe edición vigente'

    @api.depends('name')
    def _compute_external_edition(self):
        for record in self:
            external_issue = self.env['mgmtsystem.context.external_issue'].search([
                ('state', '=', 'validate_ok'),
            ], order='id desc', limit=1)
            if external_issue:
                record.current_external_issues = _("<a data-oe-id=%s data-oe-model='mgmtsystem.context.external_issue' href=#id=%s&model=mgmtsystem.context.external_issue>%s</a> vigente desde %s") % (
                    external_issue.id, external_issue.id, external_issue.name, external_issue.date_validate)
            else:
                record.current_external_issues = 'No existe edición vigente'


class InternalIssue(models.Model):
    _name = 'mgmtsystem.context.internal_issue'
    _inherit = ['mgmtsystem.validation.mail', 'mgmtsystem.code']
    _description = 'Contexto de la organización'

    process_id = fields.Many2one(
        'mgmt.process', string='Proceso', domain=[('active','=',True)])
    system_id = fields.Many2one(
        'mgmtsystem.context.system', string='Identificador', default=lambda self: self.env.ref('hola_calidad.policy_system_1'))

    name = fields.Char(string='Nombre', required=True)
    introduction = fields.Text(string='Introducción')
    mission = fields.Text(string='Misión', required=True)
    vision = fields.Text(string='Visión', required=True)
    morals = fields.One2many('mgmtsystem.context.moral',
                             'issue_id', string='Valores', copy=True)
    active = fields.Boolean('Active', default=True)
    current_policy = fields.Char(
        compute='_compute_current_policy', string='Política Actual')
    quality_policy = fields.Many2one(
        'mgmtsystem.context.policy', string='Política de calidad', domain="[('state','!=','cancel')]")
    scope = fields.Text(string='Alcance del sistema de gestión')
    product_ids = fields.Many2many(
        'product.product', string='Productos y servicios')
    
    parent_edition = fields.Many2one(
        comodel_name='mgmtsystem.context.internal_issue', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='mgmtsystem.context.internal_issue', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    @api.depends('name')
    def _compute_current_policy(self):
        for record in self:
            document = self.env['mgmtsystem.context.policy'].search([
                ('issue_id', '=', record.id),
                ('state', '=', 'validate_ok'),
            ], order='id desc', limit=1)
            if document:  # "<a data-oe-id=%s data-oe-model="account.journal" href=#id=%s&model=account.journal>email alias</a>
                record.current_policy = _("<a data-oe-id=%s data-oe-model='mgmtsystem.context.policy' href=#id=%s&model=mgmtsystem.context.policy>%s</a> vigente desde %s") % (
                    document.id, document.id, document.name, document.date_validate)
            else:
                record.current_policy = 'No existe edición vigente'

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_context.context_internal_issue_cancel_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result


class ContextMoral(models.Model):
    _name = 'mgmtsystem.context.moral'
    _description = 'Valores'

    issue_id = fields.Many2one(
        'mgmtsystem.context.internal_issue', string='Factor')
    name = fields.Char(string='Descripción', required=True)


class ContextPolicy(models.Model):
    _name = 'mgmtsystem.context.policy'
    _inherit = ['mgmtsystem.validation.mail', 'mgmtsystem.code']
    _description = 'Políticas'

    def _default_company(self):
        return self.env.user.company_id

    def _get_process_default(self):
        sequence = self.env['mgmt.process'].search([('code', '=', 'E-PE-1-')])
        code = sequence[0].code
        return sequence[0].id

    process_id = fields.Many2one(
        'mgmt.process', string='Proceso', )
    system_id = fields.Many2one(
        'mgmtsystem.context.system', string='Identificador', default=lambda self: self.env.ref('hola_calidad.policy_system_1'))

    custom = fields.Boolean(string='Política personalizada')

    issue_id = fields.Many2one(
        'mgmtsystem.context.internal_issue', string='Factor')
    name = fields.Char(string='Nombre de la política', required=True)
    introduction = fields.Text(string='Introducción')
    custom_text = fields.Text(string='Texto')
    #attached_files = fields.Many2many('ir.attachment', string='Archivos Adjuntos', attachment=True)
    date = fields.Date(string='Fecha de la política')
    company_id = fields.Many2one(
        'res.company',
        'Company',
        default=_default_company,
    )
    active = fields.Boolean('Active', default=True)
    template_ = fields.Many2one(
        'mgmtsystem.context.policy.template', string='Plantilla')
    parent_edition = fields.Many2one(
        comodel_name='mgmtsystem.context.policy', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='mgmtsystem.context.policy', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    organization_context = fields.Text(string='Contexto de la organización')
    direction_help = fields.Text(string='Apoyo para la dirección')
    customer_satisfaction = fields.Text(string='Satisfacción del cliente')
    legal_req = fields.Text(string='Requisitos Legales')
    standar_commitment = fields.Text(
        string='Compromiso para los requisitos de la norma')
    staff_participation = fields.Text(string='Participación del personal')
    continous_improvement = fields.Text(string='Mejora Continua')
    durability = fields.Text(string='Durabilidad')
    quality_assurance = fields.Text(string='Aseguramiento de la calidad')
    quality_goal_pre = fields.Text(string='Objetivos para la calidad')
    goals = fields.One2many(
        'mgmtsystem.context.policy.action', 'policy_id', string='Objetivos')
    communication = fields.Text(string='Comunicación')

    policy_report_content = fields.Char(
        compute='_compute_policy_report_content', string='')

    def get_content_by_type(self):
        pass

    def print_by_type(self):
        res = self.get_content_by_type()
        print(res)
        return res

    @api.depends('name')
    def _compute_policy_report_content(self):
        for each in self:
            print(each.print_by_type())
            each.policy_report_content = each.print_by_type()

    @api.onchange('template_')
    def _onchange_template_(self):
        self.name = self.template_.name
        self.introduction = self.template_.introduction
        self.organization_context = self.template_.organization_context
        self.direction_help = self.template_.direction_help
        self.customer_satisfaction = self.template_.customer_satisfaction
        self.legal_req = self.template_.legal_req
        self.standar_commitment = self.template_.standar_commitment
        self.staff_participation = self.template_.staff_participation
        self.continous_improvement = self.template_.continous_improvement
        self.durability = self.template_.durability
        self.quality_assurance = self.template_.quality_assurance
        self.quality_goal_pre = self.template_.quality_goal_pre
        self.communication = self.template_.communication

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_context.policies_cancel_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result
    
    def get_send_to_emails(self):
        return ''

    def notify_policy(self):
        self.ensure_one()
        template = 'mgmtsystem_context.email_template_mgmtsystem_context_policy'
        return self.notify_users_by_email(template)


class PolicyTemplate(models.Model):
    _name = 'mgmtsystem.context.policy.template'
    _description = 'Plantilla de Política'

    name = fields.Char(string='Nombre')
    system_id = fields.Many2one(
        'mgmtsystem.context.system', string='Identificador', default=lambda self: self.env.ref('hola_calidad.policy_system_1'))
    custom = fields.Boolean(string='Política personalizada')
    custom_text = fields.Text(string='Texto')
    introduction = fields.Text(string='Introducción')
    organization_context = fields.Text(string='Contexto de la organización')
    direction_help = fields.Text(string='Apoyo para la dirección')
    customer_satisfaction = fields.Text(string='Satisfacción del cliente')
    legal_req = fields.Text(string='Requisitos Legales')
    standar_commitment = fields.Text(
        string='Compromiso para los requisitos de la norma')
    staff_participation = fields.Text(string='Participación del personal')
    continous_improvement = fields.Text(string='Mejora Continua')
    durability = fields.Text(string='Durabilidad')
    quality_assurance = fields.Text(string='Aseguramiento de la calidad')
    quality_goal_pre = fields.Text(string='Objetivos para la calidad')
    communication = fields.Text(string='Comunicación')


class PolicyAction(models.Model):
    _name = 'mgmtsystem.context.policy.action'
    _description = 'Acción de política'

    policy_id = fields.Many2one('mgmtsystem.context.policy', string='Política')
    code = fields.Char(string='Código')
    name = fields.Char(string='Descripción')


class ExternalIssue(models.Model):
    _name = 'mgmtsystem.context.external_issue'
    _inherit = ['mgmtsystem.validation.mail', 'mgmtsystem.code']
    _description = 'Análisis de Porter'

    def _get_process_default(self):
        sequence = self.env['mgmt.process'].search([('code', '=', 'E-PE-1-')])
        code = sequence[0].code
        return sequence[0].id

    process_id = fields.Many2one(
        'mgmt.process', string='Proceso', )

    name = fields.Char(string='Nombre', required=True)
    forces = fields.One2many('mgmtsystem.context.external_issue.force',
                             'external_issue_id', string='Fuerzas de Porter', required=True)
    additional_info = fields.Text(
        string='Información adicional')
    parent_edition = fields.Many2one(
        comodel_name='mgmtsystem.context.external_issue', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='mgmtsystem.context.external_issue', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})
    active = fields.Boolean('Active', default=True)

    @api.model
    def default_get(self, fields_list):
        res = super(ExternalIssue, self).default_get(fields_list)
        forces = self.env["mgmtsystem.context.force"].search([])
        vals = [(0, 0, {'context_force': forces[0].id}),
                (0, 0, {'context_force': forces[1].id}),
                (0, 0, {'context_force': forces[2].id}),
                (0, 0, {'context_force': forces[3].id}),
                (0, 0, {'context_force': forces[4].id}),
                ]
        res.update({'forces': vals})
        return res

    def verify_forces(self):
        """Check if all the five Porter's forces are in the current record
        """
        codes = ['F1', 'F2', 'F3', 'F4', 'F5']
        current_forces = [x.context_force.code for x in self.forces]
        needed = set(codes).difference(set(current_forces))
        message = ''
        message_list = []
        for each in needed:
            force, = self.env["mgmtsystem.context.force"].search(
                [('code', '=', each)])
            message_list.append('\t - ' + force.name)
        message = '\n'.join(map(str, message_list))
        if message_list:
            raise UserError("Faltan las siguientes fuerzas: \n" + message)

    def write(self, values):
        result = super(ExternalIssue, self).write(values)
        self.verify_forces()
        return result

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_context.context_external_issue_cancel_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result


class ExternalIssueForce(models.Model):
    _name = 'mgmtsystem.context.external_issue.force'
    _rec_name = "external_issue_id"
    _description = 'Fuerza de Porter'

    external_issue_id = fields.Many2one(
        'mgmtsystem.context.external_issue', string='Factor externo')
    context_force = fields.Many2one(
        'mgmtsystem.context.force', string='Fuerza de Porter')
    relevance = fields.Selection([
        ('1', '1 (se controla totalmente)'),
        ('2', '2 (se controla óptimamente)'),
        ('3', '3 (se controla medianamente)'),
        ('4', '4 (se controla escasamente)'),
        ('5', '5 (no se tiene control)'),
    ], string='Puntuación', index=True, default='1')
    description = fields.Text(string='Análisis')


class ContextForce(models.Model):
    _name = 'mgmtsystem.context.force'
    _description = 'Fuerza'

    code = fields.Char(string='Código')
    name = fields.Char(string='Fuerza', required=True)
    description = fields.Text(string='Descripción')


class StakeHolderList(models.Model):
    _name = 'mgmtsystem.stakeholders'
    _inherit = ['mgmtsystem.validation.mail', 'mgmtsystem.code']
    _description = 'Matriz de Interesados'

    def _get_process_default(self):
        sequence = self.env['mgmt.process'].search([('code', '=', 'E-PE-1-')])
        code = sequence[0].code
        return sequence[0].id

    name = fields.Char(string='Nombre', required=True)

    system_id = fields.Many2one(
        'mgmtsystem.context.system', string='Identificador', default=lambda self: self.env.ref('hola_calidad.policy_system_1'))

    process_id = fields.Many2one(
        'mgmt.process', string='Proceso', )

    stakeholder_in_ids = fields.Many2many(
        'mgmtsystem.stakeholder',
        'mgmtsystem_stakeholders_stakeholder_in_rel', 
        string='Interesados Internos', domain=[('type', '=', 'in')], )
    
    stakeholder_out_ids = fields.Many2many(
        'mgmtsystem.stakeholder', 
        'mgmtsystem_stakeholders_stakeholder_out_rel',
        string='Interesados Externos', domain=[('type', '=', 'out')], ) 
    
    #stakeholder_in_ids = fields.One2many(
        #'mgmtsystem.stakeholder', string='Interesados', inverse_name='list_id', domain=[('type', '=', 'in')], )
    #stakeholder_out_ids = fields.One2many(
        #'mgmtsystem.stakeholder', string='Interesados', inverse_name='list_id', domain=[('type', '=', 'out')], )
    parent_edition = fields.Many2one(
        comodel_name='mgmtsystem.stakeholders', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='mgmtsystem.stakeholders', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})
    active = fields.Boolean('Active', default=True)
    process_id = fields.Many2one('mgmt.process', domain=[('active','=',True)], string='Proceso')

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_context.stakeholders_cancel_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result


class StakeholderStakeholder(models.Model):
    _name = 'stakeholder.stakeholder'
    _description = 'Parte interesada'

    name = fields.Char(string='Nombre')


class StakeHolder(models.Model):
    _name = 'mgmtsystem.stakeholder'
    _description = 'Interesado'

    name = fields.Char(string='Parte interesada',
                       )
                       #, required=True related='stakeholder_id.name')
    #stakeholder_id = fields.Many2one(
        #'stakeholder.stakeholder', string='Parte interesada')
    #list_id = fields.Many2one(
        #comodel_name='mgmtsystem.stakeholders', string='Matriz')

    name = fields.Char(string='Parte interesada',
                       required=True )
   
    system_id = fields.Many2one(
        'mgmtsystem.context.system', string='Identificador', default=lambda self: self.env.ref('hola_calidad.policy_system_1'))
    partner_id = fields.Many2one('res.partner', string='Interesado')
    original = fields.Boolean(string='Original', default=False)
    requirements = fields.One2many(
        'mgmtsystem.stakeholder.req', 'stakeholder_id', string='Requisitos')
    power = fields.Selection([
        ('1', '1 (menor)'),
        ('2', '2 (mayor)')
        ], string='Poder', index=True )
    
    interest = fields.Selection([
        ('1', '1 (menor)'),
        ('2', '2 (mayor)')
        ], string='Interés', index=True )

    risk_ids = fields.Many2many(
        'matrix.block.line', string='Riesgos', domain="[('type','=','risk')]", relation='ris_stakeholder_rel',
    )
    opportunity_ids = fields.Many2many(
        'matrix.block.line', string='Oportunidades', domain="[('type','=','opportunity')]", relation='op_stakeholder_rel',
    )
    type = fields.Selection([
        ('out', 'Externo'),
        ('in', 'Interno')
    ], string='Tipo')


    membership = fields.Integer(
        compute='_compute_membership', string='Nivel de pertenencia', store=True)
      
    calification = fields.Char(
        compute='_compute_calification', string='Calificación', store=True)

    
    @api.depends('membership')
    def _compute_calification(self):
        for each in self:
            if each.membership == 1:
                each.calification = 'Monitorear'
            elif each.membership == 2:
                each.calification = 'Mantener satisfecho/Informado'
            elif each.membership == 4:
                each.calification = 'Gestionar atentamente'
            else:
                each.calification = 'No Calificado'

    
    @api.depends('power', 'interest')
    def _compute_membership(self):
        for each in self:
            if each.power and each.interest:
                each.membership = int(each.power) * int(each.interest)
            else:
                each.membership = 0
    

class StakeholderReq(models.Model):
    _name = 'mgmtsystem.stakeholder.req'

    name = fields.Char(string='Descripción')
    type = fields.Selection([
        ('nec', 'Necesidad'),
        ('exp', 'Expectativa'),
    ], string='Tipo')
    stakeholder_id = fields.Many2one(
        'mgmtsystem.stakeholder', string='Interesado')


class StakeholderOpportunity(models.Model):
    _name = 'mgmtsystem.stakeholder.opp'

    name = fields.Char(string='Descripción')
    stakeholder_id = fields.Many2one(
        'mgmtsystem.stakeholder', string='Interesado')
