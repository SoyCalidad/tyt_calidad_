# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class TypeSurvey(models.Model):
    _name = 'survey.type'

    name = fields.Char(
        string='Nombre',
        required=True,
    )
    description = fields.Text(
        string='Descripción',
    )


class SurveyReport(models.Model):
    _name = 'survey.report'

    # survey_id = fields.Many2one(
    #     string='Encuesta',
    #     comodel_name='survey.survey',
    #     ondelete='restrict',
    # )

    # name = fields.Char(
    #     string='Nombre',
    #     default=lambda self: "Reporte de ...",
    # )

    # # Ficha tecnica
    # title_complete = fields.Char(
    #     string='Título de la investigación',
    #     related="survey_id.title_complete",
    # )
    # sampling_unit = fields.Char(
    #     string='Unidad de muestreo',
    #     related="survey_id.sampling_unit",
    # )
    # type_id = fields.Many2one(
    #     string='Tipo de encuesta',
    #     related="survey_id.type_id",
    # )
    # site = fields.Char(
    #     string='Sitio de encuesta',
    #     related="survey_id.site",
    # )
    # sampling = fields.Text(
    #     string='Muestreo',
    #     related="survey_id.sampling",
    # )
    # target_audiences = fields.Text(
    #     string='Público objetivo',
    #     related="survey_id.target_audiences",
    # )
    # total_population = fields.Char(
    #     string='Población total',
    #     related="survey_id.total_population",
    # )
    # date_init = fields.Date(
    #     string='Fecha de realización',
    #     related="survey_id.date_init",
    # )
    # date_fin = fields.Date(
    #     string='Fecha de finalización',
    #     related="survey_id.date_fin",
    # )
    # date_process_init = fields.Date(
    #     string='Fecha de inicio de proceso',
    #     related="survey_id.date_process_init",
    # )
    # date_process_fin = fields.Date(
    #     string='Fecha de finalización de proceso',
    #     related="survey_id.date_process_fin",
    # )
    # type = fields.Selection(
    #     string='Tipo',
    #     selection=[('int', 'Interno'), ('ext', 'Externo')],
    #     default='ext',
    #     related="survey_id.type",
    # )
    # # end Ficha tecnica

    # line_ids = fields.One2many(
    #     string='Conclusiones y Recomendaciones',
    #     comodel_name='survey.report.actionnonc',
    #     inverse_name='report_id',
    # )

    # con_rec = fields.Text(string='Conclusiones y recomendaciones')

    # @api.model
    # def default_get(self, fields_list):
    #     res = super(SurveyReport, self).default_get(fields_list)

    #     if res.get('survey_id'):
    #         vals = []
    #         survey_id = self.env["survey.survey"].browse(res['survey_id'])
    #         for page in survey_id.page_ids:
    #             for question in page.question_ids:
    #                 vals.append(
    #                     (0, 0, {'question_id': question.id, 'attachment_ids': None}))
    #         print(vals)
    #         res.update({'line_ids': vals})
    #     return res


class ReportActionNoconf(models.Model):
    _name = 'survey.report.actionnonc'

    survey_id = fields.Many2one(
        string='Reporte',
        comodel_name='survey.survey',
        ondelete='restrict',
    )
    # survey_id = fields.Many2one(
    #     string='Encuesta',
    #     comodel_name='survey.survey',
    #     related='report_id.survey_id',
    # )

    description = fields.Text(
        string='Descripción',
        required=True,
    )
    action_id = fields.Many2one(
        string="Acción",
        comodel_name='mgmtsystem.action',
        ondelete='restrict',
    )
    nc_id = fields.Many2one(
        string="No conformidad",
        comodel_name='mgmtsystem.nonconformity',
        ondelete='restrict',
    )

    attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Adjuntos'
    )

    question_id = fields.Many2one(
        'survey.question',
        string='Pregunta',
        domain="[('survey_id','=',survey_id)]"
    )

    def open_form_view(self):
        view_id = self.env.ref(
            'mgmtsystem_survey.view_survey_report_actionnonc_form').id
        context = self._context.copy()
        return {
            'name': 'Conclusiones y recomendaciones',
            'view_type': 'form',
            'views': [(view_id, 'form')],
            'res_model': 'survey.report.actionnonc',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'target': 'new',
            'context': context,
        }


class Survey(models.Model):
    _name = 'survey.survey'
    _inherit = ['survey.survey', 'mgmtsystem.validation']

    # report_ids = fields.One2many(
    #     string='Reportes',
    #     comodel_name='survey.report',
    #     inverse_name='survey_id',
    # )
    # count_reports = fields.Integer(
    #     string='# de Reportes',
    #     compute='_compute_count_reports',
    # )
    count_actions = fields.Integer(
        string='# de Acciones',
        compute='_compute_count_reports',
    )
    count_ncs = fields.Integer(
        string='# de No conformidades',
        compute='_compute_count_reports',
    )
    count_lines = fields.Integer(
        string='# de Lineas',
        compute='_compute_count_reports',
    )

    @api.depends('line_ids')
    def _compute_count_reports(self):
        for record in self:
            # record.count_reports = len(record.report_ids) or 0
            num_action = num_ncs = 0
            for report in record.line_ids:
                if report.action_id:
                    num_action += 1
                if report.nc_id:
                    num_ncs += 1
            record.count_actions = num_action
            record.count_ncs = num_ncs
            record.count_lines =len(record.line_ids)

    # Ficha tecnica
    title_complete = fields.Char(
        string='Título de la investigación',
    )
    sampling_unit = fields.Char(
        string='Unidad de muestreo',
    )
    type_id = fields.Many2one(
        string='Tipo de encuesta',
        comodel_name='survey.type',
        ondelete='restrict',
    )
    site = fields.Char(
        string='Sitio de encuesta',
    )
    sampling = fields.Text(
        string='Muestreo',
    )
    target_audiences = fields.Text(
        string='Público objetivo',
    )
    total_population = fields.Char(
        string='Población total',
    )
    date_init = fields.Date(
        string='Fecha de realización'
    )
    date_fin = fields.Date(
        string='Fecha de finalización'
    )
    date_process_init = fields.Date(
        string='Fecha de inicio de proceso'
    )
    date_process_fin = fields.Date(
        string='Fecha de finalización de proceso'
    )
    type = fields.Selection(
        string='Tipo',
        selection=[('int', 'Interno'), ('ext', 'Externo')],
        default='ext',
    )
    # end Ficha tecnica

    line_ids = fields.One2many(
        string='Conclusiones y Recomendaciones',
        comodel_name='survey.report.actionnonc',
        inverse_name='survey_id',
    )

    con_rec = fields.Text(string='Conclusiones y recomendaciones')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        for page in self.page_ids:
            vals = []
            for question in page.question_ids:
                vals.append(
                    (0, 0, {'question_id': question.id, 'attachment_ids': None}))
            res.update({'line_ids': vals})
        return res

    state = fields.Selection(
        string="Survey Stage",
        selection=[
            ('draft', 'Draft'),
            ('open', 'In Progress'),
            ('closed', 'Closed'),
        ], default='draft', required=True,
        group_expand='_read_group_states'
    )

    def action_survey_views(self):
        type_action = self._context.get('type_action', '')
        if type_action == '':
            return

        if type_action == 'report':
            action_rec = self.env.ref(
                'mgmtsystem_survey.action_survey_report').read()[0]
            ctx = dict(self.env.context)
            ctx.update({'search_default_survey_id': self.ids[0]})

        elif type_action == 'action':
            action_rec = self.env.ref(
                'mgmtsystem_survey.action_survey_action_nc').read()[0]
            ctx = dict(self.env.context)
            ctx.update(
                {'search_default_survey_id': self.ids[0], 'search_default_true_action': 1})

        elif type_action == 'nc':
            action_rec = self.env.ref(
                'mgmtsystem_survey.action_survey_action_nc').read()[0]
            ctx = dict(self.env.context)
            ctx.update(
                {'search_default_survey_id': self.ids[0], 'search_default_true_nc': 1})

        action_rec['context'] = ctx
        return action_rec

    def action_survey_user_input_line(self):
        action_rec = self.env.ref(
            'mgmtsystem_survey.action_survey_input').read()[0]
        ctx = dict(self.env.context)
        ctx.update({'search_default_survey_id': self.ids[0]})
        action_rec['context'] = ctx
        return action_rec
