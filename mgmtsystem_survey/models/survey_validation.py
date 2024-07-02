from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SurveySurvey(models.Model):
    _inherit = 'survey.survey'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'survey_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'survey_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'survey_validation_id', string='Validación')

    parent_edition = fields.Many2one(
        comodel_name='survey.survey', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='survey.survey', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    state = fields.Selection(
        string="Survey Stage",
        selection=[
            ('elaborate', 'En elaboración'),
            ('review', 'En revisión'),
            ('validate', 'En validación'),
            ('validate_ok', 'Validado'),
            ('draft', 'Draft'),
            ('open', 'In Progress'),
            ('closed', 'Closed'),
            ('cancel', 'Obsoleto')
        ], default='elaborate', required=True,
        group_expand='_read_group_states'
    )

    process_id = fields.Many2one(
        comodel_name='process.edition', string='Procedimiento', required=False)

    first_step = fields.Boolean(string='Etapa de validación', default=True)
    second_step = fields.Boolean(string='Etapa de encuesta', default=False)

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_survey.action_survey_form').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result

    def notify_to_step_users(self, steps, type):
        body = ''
        self.env.cr.execute("""SELECT id FROM ir_model 
                            WHERE model = %s""", (str(self._name),))
        info = self.env.cr.dictfetchall()
        if info:
            model_id = info[0]['id']
        if type == 'elaboration':
            body += 'Elaboración de documento'
        elif type == 'review':
            body += 'Revisión de documento'
        elif type == 'validation':
            body += 'Validación de documento'
        for step in steps:
            if step.user_id:
                todo_id = self.env['mail.activity.type'].search(
                    [('name', '=', 'To Do')], limit=1).id
                self.env['mail.activity'].create({
                    'res_id': self.ids[0],
                    'res_model_id': model_id,
                    'res_model': self._name,
                    'summary': body,
                    'user_id': step.user_id.id,
                    'activity_type_id': int(todo_id),
                })


class SurveySurveyValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    survey_elaboration_id = fields.Many2one(
        'survey.survey', string='Padre')
    survey_review_id = fields.Many2one(
        'survey.survey', string='Padre')
    survey_validation_id = fields.Many2one(
        'survey.survey', string='Padre')
