from odoo import fields, models, api


class RecordMeeting(models.Model):
    _inherit = 'record.meeting'

    objective = fields.Text(string='Objetivo')
    meeting_time = fields.Float(string='Duración de la reunión')


class RecordMeetingLine(models.Model):
    _inherit = 'record.meeting.line'

    comment = fields.Text(string='Comentarios')
