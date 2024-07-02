from odoo import api, fields, models


class AnnouncementWizard(models.TransientModel):
    _name = 'announcement.wizard'

    company_id = fields.Many2one(
        string=u'Compañia',
        comodel_name='res.company', required=True,
        domain=lambda self: [('id', 'in', self.env.user.company_ids.ids)],
        default=lambda self: self.env.user.company_id.id,
    )

    training_ids = fields.Many2one(
        string='Plan de Capacitaciones',
        comodel_name='mgmtsystem.plan.training',
        relation='training_wizard_report_rel',
        column1='training_id',
        column2='wizard_id',
    )

    def action_print(self):
        report_id = ''
        type_action = self._context.get('type_action', '')
        if type_action == '':
            return
        elif type_action == 'announcement':
            report_id = 'mgmtsystem_employees.report_announcement'
        elif type_action == 'attendance':
            report_id = 'mgmtsystem_employees.report_employee'
        data = self.read()[0]
        datas = {
            'data': data,
            'ids': self._ids,
            'docs': self.training_ids.id,
            'is_wizard': True,
        }
        if not report_id:
            return
        res = self.env.ref(report_id).report_action(self.training_ids)
        return res

    def export_xls(self):
        return self.env.ref('mgmtsystem_employees.report_training_complete_xlsx').report_action(self.training_ids)


class AnnouncementReport(models.AbstractModel):
    _name = 'report.mgmtsystem_employees.report_announcement_template'

    @api.model
    def _get_report_values(self, docids, data=None):

        if data and data.get('is_wizard'):
            training_id = self.env['mgmtsystem.plan.training'].browse(
                data['docs'])
        else:
            training_id = self.env['mgmtsystem.plan.training'].browse(docids)

        company = self.env.user.company_id
        return {
            'doc_ids': self.ids,
            'company': company,
            'docs': training_id,
        }
