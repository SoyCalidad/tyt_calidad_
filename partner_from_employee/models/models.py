# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Employee(models.Model):
    _inherit = "hr.employee"

    # @api.model
    # def create(self, values):
    #     result = super(Employee, self).create(values)
    #     if values.get('name', False):
    #         res = self.env['res.partner']
    #         vals = {
    #             'name': values.get('name'),
    #             'is_employee': True,
    #         }
    #         res.create(vals)
    #     return result

    @api.model_create_multi
    def create(self, vals_list):
        partner_vals_list = []
        for vals in vals_list:
            if vals.get('name', False):
                # Preparar los valores para res.partner
                partner_vals = {
                    'name': vals['name'],
                    'is_employee': True,
                }
                partner_vals_list.append(partner_vals)

        # Crear todos los registros de hr.employee de una sola vez
        employees = super(Employee, self).create(vals_list)

        # Crear todos los registros de res.partner de una sola vez
        if partner_vals_list:
            self.env['res.partner'].create(partner_vals_list)

        return employees


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_employee = fields.Boolean(
        string=u'Empleado',
        default=False,
    )