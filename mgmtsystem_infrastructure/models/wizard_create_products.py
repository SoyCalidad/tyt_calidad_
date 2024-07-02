# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class WizardCreateProducts(models.TransientModel):
    _name = 'wizard.create.products'
    _description = u'Creación de productos'

    lines_ids = fields.One2many(
        string=u'Lineas',
        comodel_name='wizard.create.products.line',
        inverse_name='wizard_create_id',
    )
    equipment_id = fields.Many2one(
        string=u'Equipo base',
        comodel_name='maintenance.equipment',
        ondelete='cascade',
    )

    def create_products(self):
        for line in self.lines_ids:
            data = {
                'name': line.name,
                'category_id': line.category_id.id,
                'default_code': line.serial_number,
                'cost': line.cost,
                'assign_date': line.assign_date,
                'scrap_date': line.scrap_date,
                'location': line.location,
            }
            if line == self.lines_ids[0]:
                product = self.env['maintenance.equipment'].browse(self.equipment_id.id)
                product.write(data)
            else:
                self.env['maintenance.equipment'].create(data)


class WizardCreateProductsLine(models.TransientModel):
    _name = 'wizard.create.products.line'
    _description = u'Creación de lineas de productos'

    wizard_create_id = fields.Many2one(
        string=u'Wizard mayor',
        comodel_name='wizard.create.products',
        ondelete='cascade',
    )
    equipment_id = fields.Many2one(
        string=u'Equipo base',
        comodel_name='maintenance.equipment',
        related='wizard_create_id.equipment_id',
        ondelete='cascade',
    )

    name = fields.Char(u'Nombre')
    serial_number = fields.Char(
        string=u'Número de serie',
    )
    category_id = fields.Many2one(
        string=u'Categoría',
        comodel_name='maintenance.equipment.category',
        ondelete='cascade',
    )
    cost = fields.Float(
        string=u'Costo',
    )
    assign_date = fields.Date(
        string=u'Fecha de adquisición',
    )
    location = fields.Char(
        string=u'Ubicación',
    )
    scrap_date = fields.Date(
        string=u'Fecha de caducidad',
    )

    @api.onchange('equipment_id')
    def _onchange_equipment_id(self):
        qty = len(self.wizard_create_id.lines_ids)
        self.name = self.equipment_id.name
        self.serial_number = self.equipment_id.default_code + str(qty) if self.equipment_id.default_code else ""
        self.category_id = self.equipment_id.category_id
        self.cost = self.equipment_id.cost
        self.assign_date = self.equipment_id.assign_date
        self.scrap_date = self.equipment_id.scrap_date
        self.location = self.equipment_id.location