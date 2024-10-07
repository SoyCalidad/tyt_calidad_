from odoo import models, api, fields, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError

class MgmtsystemNonconformity(models.Model):
    _inherit = "mgmtsystem.nonconformity"

    found_description = fields.Text(u'Descripción')
    stakeholder_requirement = fields.Text(string="Requerimiento de la parte interesada")
    compliance = fields.Boolean(string="Conforme (Sí/No)")