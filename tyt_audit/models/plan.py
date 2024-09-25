# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError




class Plan(models.Model):
    _inherit = "audit.plan"

    name = fields.Char(
        string=u'Nombre',
        required=True,
        default="CRONOGRAMA DE AUDITORIA"
    )