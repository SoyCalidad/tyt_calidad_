from odoo import api, fields, models, _


class MessageType(models.Model):
    _name = 'tyt.intranet.message_type'
    _description = 'Message Type'

    name = fields.Char(string='Name')


class ServiceArea(models.Model):
    _name = 'tyt.intranet.service_area'
    _description = 'Service Area'

    name = fields.Char(string='Name')
    active = fields.Boolean(string='Active', default=True)


class NotificationMatrixLine(models.Model):
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

    message_type_ids = fields.One2many(
        'tyt.intranet.notification_matrix.line.message_type', 'notification_matrix_line_id',
        string='Message Types')



class NotificationMatrix(models.Model):
    _name = 'tyt.intranet.notification_matrix'
    _description = 'Notification Matrix'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    site_id = fields.Many2one('x_sitios', string='Site')
    line_ids = fields.One2many('tyt.intranet.notification_matrix.line', 'notification_matrix_id', string='Lines')


