from odoo import models, fields, api, exceptions, _


class ComplaintComplaintCauseWhy(models.Model):
    _name = 'mgmtsystem.nonconformity.cause_why'
    _description = 'Complaint Complaint Cause Why'

    name = fields.Char(compute='_compute_name', string='Nombre')

    @api.depends('cause_id', 'why_id')
    def _compute_name(self):
        for record in self:
            record.name = record.cause_id.name or '' + record.why_id.name or ''

    cause_id = fields.Many2one(
        'mgmtsystem.nonconformity.cause', string='Causa', domain="[('parent_id', '=', False)]")
    why_id = fields.Many2one(
        'mgmtsystem.nonconformity.why', string='¿Por qué?')

    cause_why_type = fields.Selection([
        ('cause', 'Causa'),
        ('why', '¿Por qué?'),
    ], string='Tipo')

    description = fields.Text('Descripción')

    subcause_ids = fields.One2many('mgmtsystem.nonconformity.cause',
                                   'cause_why_id', string='Subcausas', domain="[('parent_id','=',cause_id)]")
    attachment_ids = fields.Many2many('ir.attachment', string='Adjuntos')



class MgmtsystemNonconformityCauseWhy(models.Model):

    """Por qué de la No conformidad/accion."""

    _name = "mgmtsystem.nonconformity.why"
    _description = "Por qué de la No conformidad/accion en el sistema de gestión"
    _order = 'name'

    name = fields.Char('¿Por qué?', required=True, translate=True)
    description = fields.Text('Descripción')


class MgmtsystemNonconformityCause(models.Model):

    """Causa de la No conformidad/accion."""

    _name = "mgmtsystem.nonconformity.cause"
    _description = "Causa de la No conformidad/accion en el sistema de gestión"
    _order = 'sequence, name'

    name = fields.Char('Causa', required=True, translate=True)
    description = fields.Text('Descripción')
    parent_id = fields.Many2one(
        'mgmtsystem.nonconformity.cause', string='Padre')
    subcause_ids = fields.One2many('mgmtsystem.nonconformity.cause',
                                   'parent_id', string='Subcausas', domain="[('parent_id','=',parent_id)]")
    sequence = fields.Integer(
        'Secuencia',
        help="Defines the order to present items",
    )
    is_base = fields.Boolean(string='Es base')
    
    # Added one2many reference to mgmtsystem.nonconformity.cause_why model

    cause_why_id = fields.Many2one(
        'mgmtsystem.nonconformity.cause_why', string='Causa o Por qué')
