import base64
import io

import lxml.html
from lxml import etree
from odoo import api, fields, models
from PIL import Image


class ComunicationPlanWizard(models.TransientModel):
    _name = 'comunication.plan.wizard'

    comunication_plan_id = fields.Many2one(
        'comunication.plan', string='Programa de comunicación', required=True)

    def action_print(self):
        data = self.read()[0]
        datas = {
            'ids': self._ids,
            'docs': self.comunication_plan_id.id,
            'is_wizard': True,
        }
        res = self.env.ref('mgmtsystem_comunication.report_comunication_plan').report_action(
            self, data=datas)
        return res


class ComunicationPlanLineWizard(models.TransientModel):
    _name = 'comunication.plan.line.wizard'

    comunication_plan_line_id = fields.Many2one(
        'comunication.plan.line', string='Plan de comunicación', required=True)

    def action_print(self):
        data = self.read()[0]
        datas = {
            'ids': self._ids,
            'docs': self.comunication_plan_line_id.id,
            'is_wizard': True,
        }
        res = self.env.ref('mgmtsystem_comunication.action_report_comunication_plan_line').report_action(
            self, data=datas)
        return res


class ComunicationPlanLineWizardReport(models.AbstractModel):
    _name = 'report.mgmtsystem_comunication.comunication_plan_line_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data.get('is_wizard'):
            plan_line_ids = self.env['comunication.plan.line'].browse(
                data['docs'])
        else:
            plan_line_ids = self.env['comunication.plan.line'].browse(docids)

        company = self.env.user.company_id
        return {
            'doc_ids': self.ids,
            'company': company,
            'docs': plan_line_ids,
        }


class RecordMeetingWizard(models.TransientModel):
    _name = 'record.meeting.wizard'

    record_meeting_id = fields.Many2one(
        'record.meeting', string='Acta de Reunión')

    def action_print(self):
        report_id = ''
        type_action = self._context.get('type_action', '')
        if type_action == '':
            return
        elif type_action == 'accordance':
            report_id = 'mgmtsystem_comunication.action_report_record_meeting'
        elif type_action == 'announcement':
            report_id = 'mgmtsystem_comunication.action_report_record_conv_meeting'
        elif type_action == 'attendance':
            report_id = 'mgmtsystem_comunication.action_report_record_ass_meeting'
        data = self.read()[0]
        datas = {
            'data': data,
            'ids': self._ids,
            'docs': self.record_meeting_id.id,
            'is_wizard': True,
        }
        if not report_id:
            return
        res = self.env.ref(report_id).report_action(
            self, data=datas)
        return res


class RecordMeetingWizardReport(models.AbstractModel):
    _name = 'report.mgmtsystem_comunication.record_meeting_report_template'

    @api.model
    def _get_report_values(self, docids, data=None):

        if data.get('is_wizard'):
            record_meeting_ids = self.env['record.meeting'].browse(
                data['docs'])
        else:
            record_meeting_ids = self.env['record.meeting'].browse(docids)

        company = self.env.user.company_id
        return {
            'doc_ids': self.ids,
            'company': company,
            'docs': record_meeting_ids,
        }
