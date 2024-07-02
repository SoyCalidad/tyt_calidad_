from odoo import _, api, fields, models


class AuditWizard(models.Model):
    _name = 'audit.report.wizard'

    # start_date = fields.Date(string='Fecha inicial')
    # end_date = fields.Date(string='Fecha final')
    audit_id = fields.Many2one(
        comodel_name='audit.audit', string='Plan de auditoría', required=True)

    def action_print(self):
        data = self.read()[0]
        # self.env.cr.execute("""SELECT id FROM audit_audit
        #                   WHERE date_init>=%s AND date_fin<=%s""", [self.start_date, self.end_date],)
        # info = self.env.cr.dictfetchall()
        # ids = tuple([x['id'] for x in info])
        datas = {
            'is_wizard': True,
            'data': data,
            'ids': self.audit_id.id,
        }
        return self.env.ref('mgmtsystem_audit.action_report_audit').report_action(self, data=datas)


class AuditReport(models.AbstractModel):
    _name = 'report.mgmtsystem_audit.audit_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data and data.get('is_wizard'):
            audit_ids = self.env['audit.audit'].browse(data['ids'])
        else:
            audit_ids = self.env['audit.audit'].browse(docids)
        company = self.env.user.company_id

        return {
            'doc_ids': self.ids,
            'docs': audit_ids,
            'company': company,
        }


class AuditPlanWizard(models.Model):
    _name = 'audit.plan.report.wizard'

    audit_plan_id = fields.Many2one(
        comodel_name='audit.plan', string='Programa de auditorías', required=True)

    def action_print(self):
        data = self.read()[0]
        datas = {
            'is_wizard': True,
            'data': data,
            'ids': self.audit_plan_id.id,
        }
        return self.env.ref('mgmtsystem_audit.reporte_plananual02').report_action(self, data=datas)

    def action_print_xls(self):
        data = self.read()[0]
        datas = {
            'is_wizard': True,
            'data': data,
            'ids': self.audit_plan_id.id,
        }
        return self.env.ref('mgmtsystem_audit.report_audit_plan').report_action(self, data=datas)


class AuditPlanReport(models.AbstractModel):
    _name = 'report.mgmtsystem_audit.reporte_plananual02_auditorias_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data and data.get('is_wizard'):
            audit_ids = self.env['audit.plan'].browse(data['ids'])
        else:
            audit_ids = self.env['audit.plan'].browse(docids)
        company = self.env.user.company_id

        return {
            'doc_ids': self.ids,
            'docs': audit_ids,
            'company': company,
        }


class AuditReportWizard(models.Model):
    _name = 'audit.report.report.wizard'

    audit_report_id = fields.Many2one(
        comodel_name='audit.report', string='Informe de auditoría', required=True)

    def action_print(self):
        data = self.read()[0]
        datas = {
            'is_wizard': True,
            'data': data,
            'ids': self.audit_report_id.id,
        }
        return self.env.ref('mgmtsystem_audit.report_informe').report_action(self, data=datas)

class AuditReportReport(models.AbstractModel):
    _name = 'report.mgmtsystem_audit.report_informe_auditorias_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data and data.get('is_wizard'):
            audit_ids = self.env['audit.report'].browse(data['ids'])
        else:
            audit_ids = self.env['audit.report'].browse(docids)
        company = self.env.user.company_id

        return {
            'doc_ids': self.ids,
            'docs': audit_ids,
            'company': company,
        }
