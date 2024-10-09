from odoo import api, exceptions, fields, models, _


class Survey(models.Model):
    _inherit = 'survey.survey'

    authorized_group_id = fields.Many2one('intranet.groups', string='Authorized Group')
    department_id = fields.Many2one(related='authorized_group_id.department_id', string='Department', store=True)
    job_id = fields.Many2one(related='authorized_group_id.job_id', string='Job Position', store=True)
    sitio_id = fields.Many2one(related='authorized_group_id.sitio_id', string='Site', store=True)
    employee_ids = fields.Many2many(related='authorized_group_id.employee_ids', string='Employees')
    employee_count = fields.Integer(related='authorized_group_id.employee_count', string='Employee Count')
    user_ids = fields.Many2many(related='authorized_group_id.user_ids', string='Users')
    published_start_date = fields.Date('Published Start Date', copy=False)
    published_end_date = fields.Date('Published End Date', copy=False)
    is_published = fields.Boolean('Published', default=False, copy=False)
    access_mode = fields.Selection(selection_add=[('intranet', 'Intranet')], ondelete={'intranet': 'cascade'})
    questions_mandatory = fields.Boolean('Mandatory Questions', compute='_compute_questions_mandatory', readonly=False)

    @api.depends('access_mode')
    def _compute_questions_mandatory(self):
        for survey in self:
            if survey.access_mode == 'intranet':
                survey.questions_mandatory = True
            else:
                survey.questions_mandatory = False

    def _has_survey_answered(self, partner):
        user_input = self._get_oldest_survey_answer(partner)
        return user_input and user_input.state == 'done'

    def _get_survey_answer_state(self, partner):
        user_input = self._get_oldest_survey_answer(partner)
        return user_input and user_input.state or 'new'

    def _get_oldest_survey_answer(self, partner):
        user_input = self.user_input_ids.filtered(lambda u: u.partner_id == partner).sorted(key='create_date')[:1]
        return user_input

    def action_show_employees(self):
        self.ensure_one()
        return {
            'name': _('Employees'),
            'view_mode': 'tree,form',
            'res_model': 'hr.employee',
            'type': 'ir.actions.act_window',
            'context': {'create': False, 'delete': False},
            'domain': [('id', 'in', self.employee_ids.ids)],
            'target': 'current',
        }
