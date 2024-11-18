# -*- coding: utf-8 -*-
from odoo import models, fields

class XSitios(models.Model):
    _name = 'x_sitios'
    _description = 'Modelo de Sitios'

    name = fields.Char(
        string="Nombre",
        required=True,
        help="Nombre del sitio o ubicación"
    )
    location = fields.Char(
        string="Ubicación",
        help="Ubicación geográfica del sitio"
    )
    code = fields.Char(
        string="Código",
        help="Código único para identificar el sitio"
    )
