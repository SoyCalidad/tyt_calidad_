from odoo import api, fields, models


class WizardReportDummy(models.Model):
    _name = 'wizard.report.dummy'
    _description = 'Clase genérica de apoyo'

    name = fields.Char(string='Nombre')


class WizardReport(models.AbstractModel):
    _name = 'wizard.report'
    _description = 'Wizard para reportes'

    entry_id = fields.Many2one('wizard.report.dummy', string='Entrada')
    
    pdf_bool = fields.Boolean(string='PDF flag', default=True)
    xls_bool = fields.Boolean(string='XLS flag', default=False)

    def action_print(self, action_report):
        data = self.read()[0]
        datas = {
            'is_wizard': True,
            'data': data,
            'ids': self.audit_plan_id.id,
        }
        return self.env.ref('action_report').report_action(self, data=datas)

    def action_print_xls(self, action_report):
        data = self.read()[0]
        datas = {
            'is_wizard': True,
            'data': data,
            'ids': self.audit_plan_id.id,
        }
        return self.env.ref('action_report').report_action(self, data=datas)
