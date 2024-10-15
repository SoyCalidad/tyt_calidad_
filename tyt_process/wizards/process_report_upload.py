from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError



class ProcessReportHelper(models.Model):
    _name = 'tyt.process.report.helper'
    _description = "TYT Process Report Helper"

    name = fields.Char(string='Name')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments', copy=False)

    @api.constrains('attachment_ids')
    def _check_single_attachment(self):
        for record in self:
            if len(record.attachment_ids) > 1:
                raise ValidationError("You can only attach one file.")


class ProcessReportUpload(models.Model):
    _name = 'tyt.process.report.upload'
    _description = "TYT Process Report Upload"

    name = fields.Char(string='Name')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments', copy=False)

    @api.constrains('attachment_ids')
    def _check_single_attachment(self):
        for record in self:
            if len(record.attachment_ids) > 1:
                raise ValidationError("You can only attach one file.")

    def action_communicate(self):
        pass
