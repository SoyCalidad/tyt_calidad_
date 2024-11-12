from odoo import api, fields, models, _
from odoo.exceptions import UserError


class TYTSatisfactionSurveyHistory(models.TransientModel):
    _name = 'tyt.satisfaction.survey.history'
    _description = 'TYT Satisfaction survey history'

    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')

    @api.constrains('from_date', 'to_date')
    def _constrains_from_date(self):
        if self.from_date and self.to_date and self.from_date > self.to_date:
            raise UserError(_("The 'From Date' must be earlier than 'To Date'."))

    def action_print_report(self):
        datas = {
            'from_date': self.from_date,
            'to_date': self.to_date
        }
        return self.env.ref('tyt_customer_satisfaction_history.action_report_tyt_ssh').report_action(self, data=datas)
    
    def action_print_report_cx(self):
        datas = {
            'from_date': self.from_date,
            'to_date': self.to_date
        }
        return self.env.ref('tyt_customer_satisfaction_history.action_report_tyt_sscx').report_action(self, data=datas)