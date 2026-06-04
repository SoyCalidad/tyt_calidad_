from odoo import fields, models, api 

class CustomizedReportWizard(models.TransientModel):
    _name = "tyt.customized.report.wizard"
    _description = "Customized Report Wizard"

    department_ids = fields.Many2many(
        comodel_name='hr.department',
    )
    pdomain_ids = fields.Many2many(
        comodel_name='tyt.business.process',
        relation="tyt_customized_report_wizard_pdomain_rel"
    )
    process_ids = fields.Many2many(
        comodel_name='tyt.business.process',
        relation="tyt_customized_report_wizard_process_rel"
    )
    years = fields.Char(string="Años")
    months = fields.Char(string="Meses")

    is_acumulate = fields.Boolean(default=False, string="Es acumulado?")

    def action_generate_xlsx(self):
        self.ensure_one()

        return self.env.ref(
            "tyt_risk_management.customized_report_action_report"
        ).report_action(self)

    def action_generate_accumulated_xlsx(self):
        self.ensure_one()

        return self.env.ref(
            "tyt_risk_management.accumulated_customized_report_action_report"
        ).report_action(self)