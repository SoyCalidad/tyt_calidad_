from odoo import api, fields, models
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class NCTarget(models.Model):
    _name = 'mgmtsystem.nonconformity'
    _inherit = ['mgmtsystem.nonconformity', 'model.origin.abstract']

    target_ids = fields.Many2many('mgmtsystem.target', string='Objetivos')
    targets_count = fields.Integer(
        compute='_compute_indicators_count', string='Objetivos')

    internal_issue_ids = fields.Many2many(
        'mgmtsystem.context.internal_issue', string='Contexto organizacional', relation='internal_issue_nc')
    internal_isssues_count = fields.Integer(
        compute='_compute_internal_isssues_count', string='Contexto Organizacional')

    external_issue_ids = fields.Many2many(
        'mgmtsystem.context.external_issue', string='Factores externos', relation='external_issue_nc')
    external_issues_count = fields.Integer(
        compute='_compute_external_isssues_count', string='Contexto Organizacional')

    swot_ids = fields.Many2many(
        'mgmtsystem.context.swot', string='FODA', relation='swot_nc')
    swot_count = fields.Integer(
        compute='_compute_swot_count', string='Contexto Organizacional')

    cross_swot_ids = fields.Many2many(
        'mgmtsystem.context.cross.swot', string='FODA Cruzado', relation='cross_swot_nc')
    cross_swot_count = fields.Integer(
        compute='_compute_cross_swot_count', string='Contexto Organizacional')

    record_meeting_ids = fields.Many2many(
        'record.meeting', string='Actas de Reunión')
    record_meetings_count = fields.Integer(
        compute='_compute_record_meetings', string='Actas de Reunión')

    comunication_plan_line_ids = fields.Many2many(
        'comunication.plan.line', string='Comunicaciones')
    comunication_plan_lines_count = fields.Integer(
        compute='_compute_comunication_plans_count', string='Comunicaciones')

    risk_ids = fields.Many2many('matrix.block.line', relation='nc_risk_rel',
                                string='Riesgos', domain=[('type', '=', 'risk')])
    risks_count = fields.Integer(
        compute='_compute_risks_count', string='Riesgos')

    opp_ids = fields.Many2many('matrix.block.line', relation='nc_op_rel',
                               string='Oportunidades', domain=[('type', '=', 'opportunity')])
    opps_count = fields.Integer(
        compute='_compute_opps_count', string='Oportunidades')

    pest_ids = fields.Many2many(
        'mgmtsystem.context.pest', string='Análisis PESTEL', relation="nc_pest_rel")
    pest_count = fields.Integer(
        compute='_compute_pest_count', string='Análisis PESTEL')

    stakeholders_ids = fields.Many2many(
        'mgmtsystem.stakeholders', string='Interesados', relation="stak_nc_rel")
    stakeholders_count = fields.Integer(
        compute='_compute_stakeholders_count', string='Interesados')

    policy_ids = fields.Many2many(
        'mgmtsystem.context.policy', string='Políticas', relation="nc_policy_rel")
    policies_count = fields.Integer(
        compute='_compute_policies_count', string='Políticas')

    @api.depends('policy_ids')
    def _compute_policies_count(self):
        for each in self:
            if each.policy_ids:
                each.policies_count = len(self.policy_ids)
            else:
                each.policies_count = 0

    @api.depends('stakeholders_ids')
    def _compute_stakeholders_count(self):
        for each in self:
            if each.stakeholders_ids:
                each.stakeholders_count = len(self.stakeholders_ids)
            else:
                each.stakeholders_count = 0

    # Ayuda a ingresar el modelo de origen, no se guarda en la base de datos
    def compute_model_id(self):
        for record in self:
            record.model_id = self.env['ir.model'].search(
                [('model', '=', self._name)], limit=1)

    model_id = fields.Many2one(
        string='Modelo',
        comodel_name='ir.model',
        ondelete='cascade',
        compute=compute_model_id,
        store=False,
    )
    # edicion para usuario secundario

    def write(self, values):
        result = super(NCTarget, self).write(values)
        self.verify_origin()
        return result

    @api.depends('risk_ids')
    def _compute_risks_count(self):
        for each in self:
            each.risks_count = 0
            if each.risk_ids:
                each.risks_count = len(each.risk_ids)

    @api.depends('opp_ids')
    def _compute_opps_count(self):
        for each in self:
            each.opps_count = 0
            if each.opp_ids:
                each.opps_count = len(each.opp_ids)

    @api.depends('comunication_plan_line_ids')
    def _compute_comunication_plans_count(self):
        for each in self:
            if each.comunication_plan_line_ids:
                each.comunication_plan_lines_count = len(
                    each.comunication_plan_line_ids)
            else:
                each.record_meetings_count = 0

    @api.depends('record_meeting_ids')
    def _compute_record_meetings(self):
        for each in self:
            if each.record_meeting_ids:
                each.record_meetings_count = len(each.record_meeting_ids)
            else:
                each.record_meetings_count = 0

    @api.depends('internal_issue_ids')
    def _compute_internal_isssues_count(self):
        for each in self:
            each.internal_isssues_count = len(each.internal_issue_ids)

    @api.depends('external_issue_ids')
    def _compute_external_isssues_count(self):
        for each in self:
            each.internal_isssues_count = len(each.external_issue_ids)

    @api.depends('swot_ids')
    def _compute_swot_count(self):
        for each in self:
            each.internal_isssues_count = len(each.swot_ids)

    @api.depends('cross_swot_ids')
    def _compute_cross_swot_count(self):
        for each in self:
            each.internal_isssues_count = len(each.cross_swot_ids)

    @api.depends('target_ids')
    def _compute_indicators_count(self):
        for each in self:
            if each.target_ids:
                each.targets_count = len(self.target_ids)
            else:
                each.targets_count = 0

    @api.depends('pest_ids')
    def _compute_pest_count(self):
        for each in self:
            if each.pest_ids:
                each.pest_count = len(self.pest_ids)
            else:
                each.pest_count = 0


class TargetNC(models.Model):
    _inherit = 'mgmtsystem.target'

    nonconformity_ids = fields.Many2many(
        'mgmtsystem.nonconformity', string='No conformidades')
    nonconformities_count = fields.Integer(
        compute='_compute_nonconformities_count', string='No conformidades')

    @api.depends('nonconformity_ids')
    def _compute_nonconformities_count(self):
        for each in self:
            if each.nonconformity_ids:
                each.nonconformities_count = len(each.nonconformity_ids)
            else:
                each.nonconformities_count = 0


class RiskOppNC(models.Model):
    _inherit = 'matrix.block.line'

    nonconformity_ids = fields.Many2many(
        'mgmtsystem.nonconformity', string='No conformidades', relation='nc_risk_rel')
    nonconformities_count = fields.Integer(
        compute='_compute_nonconformities_count', string='No conformidades')

    @api.depends('nonconformity_ids')
    def _compute_nonconformities_count(self):
        for each in self:
            if each.nonconformity_ids:
                each.nonconformities_count = len(each.nonconformity_ids)
            else:
                each.nonconformities_count = 0
