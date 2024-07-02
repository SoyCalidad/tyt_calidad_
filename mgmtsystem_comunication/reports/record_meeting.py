from odoo import api, fields, models

class RecordMeetingConvReport(models.AbstractModel):
    _name = 'report.mgmtsystem_comunication.record_meeting_con'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data.get('is_wizard'):
            record_meeting_id = self.env['record.meeting'].browse(data['docs'])
        else:
            record_meeting_id = self.env['record.meeting'].browse(docids)

        company = self.env.user.company_id
        return {
            'doc_ids': self.ids,
            'company': company,
            'docs': record_meeting_id,
        }

class RecordMeetingAssReport(models.AbstractModel):
    _name = 'report.mgmtsystem_comunication.record_meeting_assist'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data.get('is_wizard'):
            record_meeting_id = self.env['record.meeting'].browse(data['docs'])
        else:
            record_meeting_id = self.env['record.meeting'].browse(docids)

        company = self.env.user.company_id
        return {
            'doc_ids': self.ids,
            'company': company,
            'docs': record_meeting_id,
        }