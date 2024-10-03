# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    codigo_cliente = fields.Char(string='Código de Cliente', store = True)
    grupo = fields.Char(string='Grupo', store = True)
    segmento = fields.Selection(
        [('RESTAURANTES', 'RESTAURANTES'), 
        ('HOTELES', 'HOTELES'), 
        ('MAYORISTAS', 'MAYORISTAS')],
        string='Segmento', 
        store=True
    )
    
