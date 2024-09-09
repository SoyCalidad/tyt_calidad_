# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Requisition(models.Model):
    _name = 'tyt_recruitment.requisition'
    _description = 'tyt_recruitment.requisition'

    request_date = fields.Datetime()
    closing_date = fields.Datetime()
    weeks = fields.Char()
    current_staff = fields.Integer()
    request_staff = fields.Integer()
    goal_staff = fields.Integer()
    turn = fields.Selection([('AM', 'AM'), ('PM', 'PM')])
    priority = fields.Selection([('1', '1'), ('2', '2')])
    campaign_id = fields.Many2one("tyt_recruitment.campaign", "Campaña")
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class Campaign(models.Model):
    _name = 'tyt_recruitment.campaign'
    _description = 'tyt_recruitment.campaign'

    name = fields.Char(required=True, help="Rellene el campo")
    description = fields.Text()