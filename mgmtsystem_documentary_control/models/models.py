from odoo import api, fields, models


class MgmtCateg(models.Model):
    _name = 'mgmt.categ'
    _inherit = ['mgmt.categ', 'mgmtsystem.code']
