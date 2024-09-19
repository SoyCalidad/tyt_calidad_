from odoo import models, api, fields, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError

class MgmtsystemNonconformity(models.Model):
    _inherit = "mgmtsystem.nonconformity"

    found_description = fields.Text(u'Descripción')
