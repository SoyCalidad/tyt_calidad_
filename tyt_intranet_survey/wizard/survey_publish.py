import pytz

from odoo import api, exceptions, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime, time


class SurveyPublish(models.TransientModel):
    _name = 'survey.publish'
    _description = 'Publish Survey'

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    deadline = fields.Datetime('Deadline', compute='_compute_deadline', store=True)
    survey_ids = fields.Many2many('survey.survey', string='Surveys')

    @api.depends('end_date')
    def _compute_deadline(self):
        for record in self:
            if record.end_date:
                user_tz = self.env.user.tz or 'UTC'
                user_pytz = pytz.timezone(user_tz)
                end_datetime_naive = datetime.combine(record.end_date, time(23, 59, 59))
                end_datetime = user_pytz.localize(end_datetime_naive)
                deadline_utc = end_datetime.astimezone(pytz.UTC)
                record.deadline = fields.Datetime.to_string(deadline_utc)
            else:
                record.deadline = False

    @api.model
    def default_get(self, field_names):
        defaults_dict = super().default_get(field_names)
        active_ids = self.env.context.get('active_ids', [])
        surveys = self.env['survey.survey'].search([
            ('id', 'in', active_ids),
            ('group_ids', '!=', False),
            ('access_mode', '=', 'intranet')],
        )
        if surveys:
            defaults_dict['survey_ids'] = [(6, 0, surveys.ids)]
        else:
            defaults_dict['survey_ids'] = []
        return defaults_dict

    def action_publish(self):
        self.ensure_one()
        if not (self.start_date and self.end_date):
            raise UserError(_('Start Date and End Date are required.'))

        if all(survey.publish_state != 'published' for survey in self.survey_ids):
            self.survey_ids.write({
                'published_start_date': self.start_date,
                'published_end_date': self.end_date,
                'publish_state': 'published',
            })
            self.action_invite()
        else:
            raise UserError(_('All surveys must be unpublished before publishing.'))

    def action_unpublish(self):
        self.ensure_one()
        if all(survey.publish_state == 'published' for survey in self.survey_ids):
            self.survey_ids.write({
                'published_start_date': False,
                'published_end_date': False,
                'publish_state': 'draft',
            })
            self._unlink_survey_user_input()
        else:
            raise UserError(_('All surveys must be published before unpublishing.'))

    def action_invite(self):
        self.ensure_one()
        for survey in self.survey_ids:
            partners = survey.group_ids.mapped('users').mapped('partner_id')
            wizard = self.env['survey.invite']
            wizard.create({
                'survey_id': survey.id,
                'partner_ids': [(6, 0, partners.ids)],
                'deadline': self.deadline,
            })._prepare_answers(partners=partners, emails=[])

    def _unlink_survey_user_input(self):
        self.ensure_one()
        for survey in self.survey_ids:
            survey.user_input_ids.unlink()
        return True
