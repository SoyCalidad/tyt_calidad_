from odoo import api, fields, models

class SurveyDatabase(models.TransientModel):
    _name = 'survey.survey.database_report'
    _description = 'Base de datos de encuestas'

    start_date = fields.Date(string='Fecha de inicio')
    end_date = fields.Date(string='Fecha final')

    def action_print(self):
        self.env.cr.execute("""SELECT id FROM survey_survey
                          WHERE date_init>=%s AND date_init<=%s""", [self.start_date, self.end_date],)
        info = self.env.cr.dictfetchall()
        ids = tuple([x['id'] for x in info])
        datas = {
            'ids': ids,
        }
        return self.env.ref('mgmtsystem_survey.action_report_survey_database').report_action(self, data=datas)

class SurveyDatabaseReport(models.AbstractModel):
    _name = 'report.mgmtsystem_survey.report_survey_database'

    @api.model
    def _get_report_values(self, docids, data=None):
        survey_ids = self.env['survey.survey'].browse(data.get('ids'))

        docs = self.env['survey.survey.database_report'].browse(docids)

        company = self.env.user.company_id
        return {
            'doc_ids': self.ids,
            'docs': docs,
            'company': company,
            'surveys': survey_ids,
        }