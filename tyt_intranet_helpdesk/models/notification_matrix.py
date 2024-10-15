from odoo import api, fields, models, _


class MessageType(models.Model):
    _name = 'tyt.intranet.message_type'
    _description = 'Message Type'

    name = fields.Char(string='Name')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Message type name must be unique!'),
    ]


class ServiceArea(models.Model):
    _name = 'tyt.intranet.service_area'
    _description = 'Service Area'

    name = fields.Char(string='Name')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Service area name must be unique!'),
    ]


class NotificationMatrixLineMessageType(models.Model):
    _name = 'tyt.intranet.notification_matrix.line.message_type'
    _description = 'Notification Matrix Line Message Type'

    notification_matrix_line_id = fields.Many2one('tyt.intranet.notification_matrix.line', string='Notification Matrix Line')
    message_type_id = fields.Many2one('tyt.intranet.message_type', string='Message Type')
    user_ids = fields.Many2many('res.users', 'notification_matrix_line_message_type_res_users_rel', string='Users')


class NotificationMatrixLine(models.Model):
    _name = 'tyt.intranet.notification_matrix.line'
    _description = 'Notification Matrix Line'

    notification_matrix_id = fields.Many2one('tyt.intranet.notification_matrix', string='Notification Matrix')
    service_area_id = fields.Many2one('tyt.intranet.service_area', string='Service Area')
    responsible_id = fields.Many2one('res.users', string='Responsible')
    matrix_line_message_type_ids = fields.One2many(
        'tyt.intranet.notification_matrix.line.message_type', 'notification_matrix_line_id',
        string='Notification Matrix Line Message Types')

    @api.onchange('notification_matrix_id')
    def _onchange_create_matrix_line_message_type_ids(self):
        """Create the One2many lines dynamically based on changes to matrix or service area."""
        for record in self:
            record.matrix_line_message_type_ids = [(5, 0, 0)]
            if record.notification_matrix_id:
                message_types = self.env['tyt.intranet.message_type'].search([])
                lines_to_create = []
                for message_type in message_types:
                    lines_to_create.append((0, 0, {
                        'message_type_id': message_type.id,
                    }))
                record.matrix_line_message_type_ids = lines_to_create


class NotificationMatrix(models.Model):
    _name = 'tyt.intranet.notification_matrix'
    _description = 'Notification Matrix'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    site_id = fields.Many2one('x_sitios', string='Site')
    matrix_line_ids = fields.One2many(
        'tyt.intranet.notification_matrix.line', 'notification_matrix_id',
        string='Notification Matrix Lines')
