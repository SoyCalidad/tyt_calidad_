from odoo import api, exceptions, fields, models, _
from odoo.exceptions import UserError


class SurveyManagement(models.Model):
    _name = 'tyt.survey.management'
    _description = 'TYT Survey Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    user_id = fields.Many2one('res.users', string='Responsible', domain=[('share', '=', False)], tracking=True, default=lambda self: self.env.user)
    authorized_group_id = fields.Many2one('intranet.groups', string='Authorized Group')
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    survey_ids = fields.Many2many('survey.survey', string='Surveys')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
    ], string='State', default='draft')

    def action_publish(self):
        self.ensure_one()
        if all(not survey.is_published for survey in self.survey_ids):
            self.state = 'published'
            self.survey_ids.write({
                'is_published': True,
                'published_start_date': self.start_date,
                'published_end_date': self.end_date,
            })
        else:
            raise UserError(_('All surveys must be unpublished before publishing.'))

    def action_draft(self):
        self.ensure_one()
        self.state = 'draft'
        self.survey_ids.write({
            'is_published': False,
            'published_start_date': False,
            'published_end_date': False
        })
