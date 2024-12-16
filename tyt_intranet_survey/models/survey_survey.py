from odoo import api, exceptions, fields, models, _


class Survey(models.Model):
    _inherit = 'survey.survey'

    published_start_date = fields.Date('Published Start Date', copy=False)
    published_end_date = fields.Date('Published End Date', copy=False)
    is_published = fields.Boolean('Published', default=False, copy=False)
    access_mode = fields.Selection(selection_add=[('intranet', 'Intranet')], ondelete={'intranet': 'cascade'})
    questions_mandatory = fields.Boolean('Mandatory Questions', compute='_compute_questions_mandatory',
                                         store=True, readonly=False, default=False)

    job_id = fields.Many2one('hr.job', string='Job Position')
    department_id = fields.Many2one('hr.department', string='Department')
    gps = fields.Boolean(string='gps')
    group_ids = fields.Many2many('res.groups', string='Groups')

    @api.onchange('gps')
    def onchange_gps(self):
        self.ensure_one()
        if self.gps and self.job_id:
            groups = self.env['res.groups'].search([('x_studio_job', '=', self.job_id.id)])
            self.group_ids = [(6, 0, groups.ids)] if groups else []
            self.gps = False

    @api.depends('access_mode')
    def _compute_questions_mandatory(self):
        for survey in self:
            if survey.access_mode == 'intranet':
                survey.questions_mandatory = True
                survey.users_can_go_back = True
                survey.scoring_type = 'scoring_without_answers'
                survey.scoring_success_min = 0

    # def _has_survey_answered(self, partner):
    #     user_input = self._get_oldest_survey_answer(partner)
    #     return user_input and user_input.state == 'done'
    #
    # def _get_survey_answer_state(self, partner):
    #     user_input = self._get_oldest_survey_answer(partner)
    #     return user_input and user_input.state or 'new'
    #
    # def _get_oldest_survey_answer(self, partner):
    #     user_input = self.user_input_ids.filtered(lambda u: u.partner_id == partner).sorted(key='create_date')[:1]
    #     return user_input

    def action_show_employees(self):
        pass
        # self.ensure_one()
        # return {
        #     'name': _('Employees'),
        #     'view_mode': 'tree,form',
        #     'res_model': 'hr.employee',
        #     'type': 'ir.actions.act_window',
        #     'context': {'create': False, 'delete': False},
        #     'domain': [('id', 'in', self.employee_ids.ids)],
        #     'target': 'current',
        # }
