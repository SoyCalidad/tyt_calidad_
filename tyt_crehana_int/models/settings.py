# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MyModuleSettings(models.TransientModel):
    _name = 'tyt_crehana.crehana_settings'
    _description = 'Configuraciones'

    api_key = fields.Char(string="api-Key", )
    secret_access = fields.Char(string="secret-access")
    organization_slug = fields.Char(string="Organización")

    @api.model
    def create(self, values):
        # Verificar si ya existe un registro
        if self.search([]):
            raise UserError("Ya existe un registro de configuración. No puedes crear otro.")
        return super(MyModuleSettings, self).create(values)