from odoo import api, fields, models


class SoycalidadChangeRequestArea(models.Model):
    _name = 'soycalidad.change_request.area'
    _description = 'Area de Planificación de Cambio'

    name = fields.Char(string='Nombre')


class ChangeRequest(models.Model):
    _name = 'soycalidad.change_request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Planificación de cambio'

    name = fields.Char('Nombre', required=True)
    request_date = fields.Date(string='Fecha de solicitud', required=True)
    employee_id = fields.Many2one(
        'hr.employee', string='Solicitante', required=True)

    background = fields.Text(
        string='Antecedentes del cambio (¿Por qué se requiere?)')
    description = fields.Text(string='Descripción del cambio')
    benefit = fields.Text(
        string='Acción aplicada para asegurar la conformidad del producto/servicio en el Sistema de gestión')
    consequence = fields.Text(
        string='Posible impacto en la conformidad del producto/servicio en el Sistema de gestión')
    needing = fields.Text(
        string='Necesidad de asignación o reasignación de responsibilidades y autoridades')

    #dms_document_ids = fields.Many2many('dms.file', string='Documentos anexos')
    #documents_count = fields.Integer(
        #compute='_compute_documents_count', string='Documentos anexos')

    responsible_id = fields.Many2one(
        'res.users', string='Persona que autoriza el cambio')
    change_request_area_id = fields.Many2one(
        'soycalidad.change_request.area', string='Área')
    area_id = fields.Selection([
        ('area1', 'Cambios en el producto/servicio'),
        ('area2', 'Cambios en los recursos'),
        ('area3', 'Cambios en las partes interesadas'),
        ('area4', 'Cambios en los procesos de trabajo'),
        ('area5', 'Cambios en las partes interesadas'),
        ('area6', 'Cambios en cuestiones internas y externas'),
    ], string='Área en la que se produce el cambio')
    approval = fields.Boolean(string='Aprobado')
    response_date = fields.Date(string='Fecha de aplicación del cambio')

    observations = fields.Text(string='Observaciones')

    action_ids = fields.Many2many('mgmtsystem.action', string='Acciones')
    actions_count = fields.Integer(
        compute='_compute_actions_count', string='Acciones')

    target_ids = fields.Many2many('mgmtsystem.target', string='Objetivos')
    targets_count = fields.Integer(
        compute='_compute_targets_count', string='Objetivos')

    resource_ids = fields.Many2many('mgmt.process.resource', string='Recursos')

    @ api.depends('action_ids')
    def _compute_actions_count(self):
        for each in self:
            if each.action_ids:
                each.actions_count = len(self.action_ids)
            else:
                each.actions_count = 0

    @ api.depends('target_ids')
    def _compute_targets_count(self):
        for each in self:
            if each.target_ids:
                each.targets_count = len(self.target_ids)
            else:
                each.targets_count = 0

    current_user_can_validate = fields.Boolean(
        compute='_get_current_user_can_validate', string='Usuario actual está autorizado para aprobar')

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('send', 'Enviada'),
        ('done', 'Aprobada'),
    ], string='Estado', default='draft')

    def to_send(self):
        """
        Cambia el estado a 'Enviada' y notifica al responsable
        """
        for each in self:
            each.state = 'send'
            each.notify_to_responsible()

    def to_done(self):
        """
        Cambia el estado a 'Aprobada' y termina el proceso
        """
        for each in self:
            notification_ids = []
            body = 'Su cambio ha sido aprobado'
            try:
                if each.employee_id and each.employee_id.user_id and each.employee_id.user_id.partner_id:
                    notification_ids.append((0, 0, {
                        'res_partner_id': each.employee_id.user_id.partner_id.id,
                        'notification_type': 'inbox'}))
                    self.message_post(body=body, message_type='notification',
                                      subtype_xmlid='mail.mt_comment', author_id=2, notification_ids=notification_ids)
                                    # "subtype" parameter to "subtype_xmlid" to make it compatible with Odoo 15 
            except:
                pass
            finally:
                each.state = 'done'
                each.approval = True

    @ api.depends('responsible_id')
    def _get_current_user_can_validate(self):
        current_user = self.env.user
        for each in self:
            if each.responsible_id.id == current_user.id:
                each.current_user_can_validate = True
            else:
                each.current_user_can_validate = False

    #def set_root_directory(self):
        #directory = 'soycalidad_improve.directory_improve'
        #return directory

    #@ api.depends('dms_document_ids')
    #def _compute_documents_count(self):
        #for each in self:
            #each.documents_count = len(each.dms_document_ids)

    #def action_document_ids(self):
        #result = self.env.ref(
            #'dms.action_dms_file').read()[0]
        #directory = self.set_root_directory()
        #result['domain'] = [('id', 'in', self.dms_document_ids.ids)]
        #result['context'] = {
            #'default_directory_id': self.env.ref(directory).id}
        #return result

    def notify_to_responsible(self):
        name = self.description or ''
        body = 'Solicitud de cambio'

        # Envía una notificación mediante correo
        mail_content = "  Saludos  " + self.responsible_id.name + \
            ",<br/>Hay una solicitud de cambio asignada a usted:  " + name
        main_content = {
            'subject': body,
            'author_id': self.env.user.partner_id.id,
            'body_html': mail_content,
            'email_to': self.responsible_id.login,
        }
        self.env['mail.mail'].create(main_content).send()

        # Envía una notificación mediante el sistema
        notification_ids = []
        notification_ids.append((0, 0, {
            'res_partner_id': self.responsible_id.partner_id.id,
            'notification_type': 'inbox'}))
        self.message_post(body=body, message_type='notification',
                          subtype_xmlid='mail.mt_comment', author_id=2, notification_ids=notification_ids)
                        # "subtype" parameter to "subtype_xmlid" to make it compatible with Odoo 15 
    def action_maintenanceplan_views(self):
        type_action = self._context.get('type_action', '')
        if type_action == '':
            return
        ids = []
        if type_action == 'target':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.action_maintenance_plan_target').read()[0]
            for each in self:
                ids.extend(each.target_ids.ids)
                domain = [('id', 'in', ids)]
                action_rec['domain'] = domain

        elif type_action == 'nc':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.action_maintenance_plan_nc').read()[0]
            for each in self:
                ids.extend(each.nonconformity_ids.ids)
                domain = [('id', 'in', ids)]
                action_rec['domain'] = domain

        elif type_action == 'action':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.action_maintenance_plan_action').read()[0]
            for each in self:
                ids.extend(each.action_ids.ids)
                domain = [('id', 'in', ids)]
                action_rec['domain'] = domain

        return action_rec
