# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Employee(models.Model):
    _inherit = "hr.employee"

    @api.model
    def create(self, values):
        result = super(Employee, self).create(values)
        if values.get('name', False):
            res = self.env['res.partner']
            vals = {
                'name': values.get('name'),
                'is_employee': True,
            }
            res.create(vals)
        return result


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_employee = fields.Boolean(
        string=u'Empleado',
        default=False,
    )