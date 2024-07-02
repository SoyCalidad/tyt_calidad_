# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

from dateutil.relativedelta import relativedelta
from datetime import date, timedelta


class Partner(models.Model):
    _inherit = 'res.partner'

    evaluation_id = fields.Many2one(
        string='Tipo de evaluación',
        comodel_name='res.partner.evaluation',
        ondelete='cascade',
    )
    history_ids = fields.One2many(
        string='Historial',
        comodel_name='res.partner.evaluation.history',
        inverse_name='partner_id',
    )

    customer = fields.Boolean(string='Cliente')
    vip_customer = fields.Boolean(string='Cliente crítico')

    supplier = fields.Boolean(string='Proveedor')
    vip_supplier = fields.Boolean(string='Proveedor crítico')

    stockist = fields.Boolean(string='Distribuidor')

    evaluation_date = fields.Date(
        string='Fecha de primera evaluación')
    # frequency_id = fields.Date(string='Frecuencia')
    frequency_id = fields.Many2one('mgmtsystem.frequency', string='Frecuencia')
    frequency = fields.Selection([
        ('weekly', 'Semanal'),
        ('monthly', 'Mensual'),
        ('yearly', 'Anual'),
    ], string='Frecuencia de evaluación')

    next_evaluation_date = fields.Date(string='Próxima fecha de evaluación')

    responsible_id = fields.Many2one(
        'hr.employee', string='Responsable de evaluación')

    def get_frequency(self):
        for each in self:
            if each.evaluation_date and each.frequency:
                if each.frequency == 'weekly':
                    frequency = relativedelta(
                        weeks=1,
                    )
                if each.frequency == 'monthly':
                    frequency = relativedelta(
                        months=1,
                    )
                if each.frequency == 'yearly':
                    frequency = relativedelta(
                        years=1,
                    )
                if frequency:
                    return frequency
            else:
                return None

    @api.onchange('evaluation_date')
    def _onchange_evaluation_date(self):
        for each in self:
            if each.frequency_id and each.evaluation_date:
                each.next_evaluation_date = each.evaluation_date + each.frequency_id.get()

    @api.onchange('frequency')
    def _onchange_frequency(self):
        for each in self:
            if each.get_frequency() and each.evaluation_date:
                each.next_evaluation_date = each.evaluation_date + each.get_frequency()

    def action_notify(self):
        for each in self:
            tomorrow = date.today() + timedelta(days=1)
            if tomorrow == each.next_evaluation_date:
                date = each.evaluation_date.strftime('%d/%m/%Y')
                self.env.cr.execute("""SELECT id FROM ir_model 
                                WHERE model = %s""", (str(each._name),))
                info = self.env.cr.dictfetchall()
                if info:
                    model_id = info[0]['id']
                body = "Reevaluación de proveedor: " + each.name + ' el ' + date
                if each.responsible_id.user_id:
                    self.env['mail.activity'].create({
                        'res_id': each.ids[0],
                        'res_model_id': model_id,
                        'res_model': each._name,
                        'summary': 'Reevaluación de proveedor',
                        'note': body,
                        'date_deadline': each.date_training,
                        'user_id': each.responsible_id.user_id.id,
                    })
                elif each.responsible_id.parent_id:
                    if each.responsible_id.parent_id.user_id:
                        self.env['mail.activity'].create({
                            'res_id': each.ids[0],
                            'res_model_id': model_id,
                            'res_model': each._name,
                            'summary': 'Reevaluación de proveedor',
                            'note': body,
                            'date_deadline': each.date_training,
                            'user_id': each.responsible_id.parent_id.user_id.id,
                        })

    def print_evaluation(self):
        if not self.history_ids:
            raise ValidationError(
                'El proveedor no cuenta con evaluaciones de seguimiento')
        data = {}
        return self.env.ref('mgmtsystem_partner_qualification.action_report_res_partner_evaluation').report_action(self.history_ids, data=data)


class Evaluation(models.Model):
    _name = 'res.partner.evaluation'
    _inherit = ['mgmtsystem.validation.mail']
    _description = 'Evaluación de socio'

    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string=u'Estado',
        selection=[
            ('elaborate', 'En elaboración'),
            ('review', 'En revisión'),
            ('validate', 'En validación'),
            ('validate_ok', 'Validado'),
            ('cancel', 'Obsoleto')
        ],
        default='elaborate',
        copy=False,
    )

    def create_action(self, vuser_id):
        action = self.env.ref('hola_calidad.p_mail_activity_action').read()[0]
        self.env.cr.execute("""SELECT id FROM ir_model 
                          WHERE model = %s""", (str(self._name),))
        info = self.env.cr.dictfetchall()
        if info:
            model_id = info[0]['id']
        action['context'] = {
            'default_res_id': self.ids[0],
            'default_res_model': self._name,
            'default_res_model_id': model_id,
            'default_user_id': vuser_id,
        }
        return action

    name = fields.Char(
        string='Nombre',
        required=True,
    )

    partner_ids = fields.One2many(
        string='Socios',
        comodel_name='res.partner',
        inverse_name='evaluation_id',
    )
    item_ids = fields.One2many(
        string='Aspectos',
        comodel_name='res.partner.evaluation.item',
        inverse_name='evaluation_id',
        copy=True,
    )
    weight_limit_total = fields.Float(
        string='Puntos limites',
        readonly=False,
        store=True,
        default=100,
    )
    weight_do_total = fields.Float(
        string='Puntos hechos',
        compute='_compute_weight_limit_total',
        readonly=False,
        default=0,
    )

    @api.onchange('item_id')
    def _onchange_item_ids(self):
        total = sum([x.weight_total for x in self.item_ids])
        if total > self.weight_limit_total:
            raise UserError('No se puede sobre los puntos límites')

    @api.depends('item_ids.weight_total')
    def _compute_weight_limit_total(self):
        for record in self:
            if not record.item_ids:
                record.weight_do_total = 0
            do_total = 0
            for item in record.item_ids:
                do_total += item.weight_total
            record.weight_do_total = do_total


class EvaluationItem(models.Model):
    _name = 'res.partner.evaluation.item'
    _description = 'Linea de evaluación/Aspecto'

    name = fields.Char(
        string='Nombre',
        required=True,
    )
    evaluation_id = fields.Many2one(
        string='Calificación',
        comodel_name='res.partner.evaluation',
        ondelete='cascade',
    )
    weight_total = fields.Float(
        string='Puntos sobre límite',
        compute='_compute_weight_total',
        readonly=False,
        store=True,
        copy=True,
        default=100,
    )

    line_ids = fields.One2many(
        string='Criterios',
        comodel_name='res.partner.evaluation.item.line',
        inverse_name='item_id',
        copy=True,
    )

    @api.depends('line_ids')
    def _compute_weight_total(self):
        for record in self:
            if not record.line_ids:
                return
            weight = 0
            for line in record.line_ids:
                weight += line.weight
            record.weight_total = weight


class EvaluationItemLine(models.Model):
    _name = 'res.partner.evaluation.item.line'
    _description = 'Criterio de aspecto'

    name = fields.Char(
        string='Nombre',
        required=True,
    )
    weight = fields.Float(
        string='Puntos',
    )
    item_id = fields.Many2one(
        string='Aspecto',
        comodel_name='res.partner.evaluation.item',
        ondelete='cascade',
    )


class History(models.Model):
    _name = 'res.partner.evaluation.history'
    _inherit = ['mail.activity.mixin', 'mgmtsystem.code']
    _description = 'Historial de evaluación de proveedor'
    _order = 'date_history desc'

    name = fields.Char(
        string='Nombre',
        related='evaluation_id.name',
        readonly=True,
        store=True
    )
    partner_id = fields.Many2one(
        string='Proveedor',
        comodel_name='res.partner',
        ondelete='cascade',
    )
    date_history = fields.Datetime(
        string='Fecha de evaluación',
        default=fields.Datetime.now,
    )
    company_id = fields.Many2one(
        string=u'Compañia',
        comodel_name='res.company', required=True,
        default=lambda self: self.env.user.company_id.id,
    )
    evaluation_id = fields.Many2one(
        string='Evaluación',
        comodel_name='res.partner.evaluation',
        ondelete='cascade',
        domain="[('state','=','validate_ok')]"
    )
    history_item_ids = fields.One2many(
        string='Aspectos',
        comodel_name='res.partner.evaluation.history.item',
        inverse_name='history_id',
        copy=True,
    )
    qualification = fields.Float(
        string='Interpretación',
        compute='_compute_qualification',
    )
    history_items_total = fields.Float()

    @api.onchange('evaluation_id')
    def _onchange_evaluation_id(self):
        if not self.evaluation_id:
            return
        lines = []
        self.history_item_ids = None
        for item in self.evaluation_id.item_ids:
            lines.append((0, 0, {'name': item.name,
                                 'item_id': item.id, }))
            history_item = self.env['res.partner.evaluation.history.item'].create({
                'name': item.name,
                'item_id': item.id,
                'history_id': self.id,
            })
            history_item._onchange_item_id()
            lines.append(history_item.id)

    @api.depends('history_item_ids')
    def _compute_qualification(self):
        for record in self:
            if not record.history_item_ids:
                record.qualification = 0
            qualification = 0.0
            for item in record.history_item_ids:
                qualification = qualification + item.qualification_item
            record.qualification = qualification

    def send_email(self):
        self.ensure_one()
        template = self.env.ref(
            'mgmtsystem_partner_qualification.email_template_partner_evaluation_history')
        # self.env['mail.template'].browse(
        #     template.id).send_mail(self.id, force_send=True, notif_layout="mail.mail_notification_light",)
        if template.lang:
            lang = template._render_template(
                template.lang, 'res.partner.evaluation.history', self.ids[0])
        ctx = {
            'default_model': 'res.partner.evaluation.history',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template),
            'default_template_id': template.id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "mail.mail_notification_light",
            'force_email': True,
            'model_description': self.with_context(lang=lang).name,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    def print_evaluation(self):
        return self.env.ref('mgmtsystem_partner_qualification.action_report_res_partner_evaluation').report_action(self.id)


class HistoryItem(models.Model):
    _name = 'res.partner.evaluation.history.item'
    _description = 'Aspecto de historial de evaluación'

    name = fields.Char(
        string='Nombre',
        related='item_id.name',
        readonly=True,
        store=True
    )
    history_id = fields.Many2one(
        string='Historial',
        comodel_name='res.partner.evaluation.history',
        ondelete='cascade',
    )
    item_id = fields.Many2one(
        string='Aspecto',
        comodel_name='res.partner.evaluation.item',
        ondelete='cascade',
    )
    history_line_ids = fields.One2many(
        string='Calificaciones',
        comodel_name='res.partner.evaluation.history.item.line',
        inverse_name='history_item_id',
        copy=True,
    )
    qualification_item = fields.Integer(
        string='Calificación',
        compute='_compute_qualification_item',
    )
    weight_total = fields.Integer(
        string='Calificación objetivo',
        compute='_compute_qualification_item',
    )

    @api.depends('history_line_ids.scala')
    def _compute_qualification_item(self):
        for record in self:
            if not record.history_line_ids:
                record.qualification_item = 0
                record.weight_total = 0
            qua = qua_max = 0.0
            for line in record.history_line_ids:
                line._onchange_scala()
                qua = qua + line.qualification_line
                qua_max = qua_max + line.line_id.weight*5
            record.weight_total = int(record.item_id.weight_total)
            record.qualification_item = (
                qua*record.item_id.weight_total)/qua_max if qua_max > 0 else 0

    @api.onchange('item_id')
    def _onchange_item_id(self):
        if not self.item_id:
            return
        lines = []
        for item in self.item_id.line_ids:
            history_line = self.env['res.partner.evaluation.history.item.line'].create({
                'name': item.name,
                'line_id': item.id,
                'history_item_id': self.id,
            })
            lines.append(history_line.id)
        self.history_line_ids = lines


class HistoryItemLine(models.Model):
    _name = 'res.partner.evaluation.history.item.line'
    _description = 'Calificación de criterio'

    name = fields.Char(
        string='Nombre',
        related='line_id.name',
        readonly=True,
        store=True
    )
    history_item_id = fields.Many2one(
        string='Aspecto',
        comodel_name='res.partner.evaluation.history.item',
        ondelete='cascade',
    )
    line_id = fields.Many2one(
        string='Criterio',
        comodel_name='res.partner.evaluation.item.line',
        ondelete='cascade',
    )
    qualification_line = fields.Float(
        string='Puntos',
        readonly=False,
        store=True
    )
    scala = fields.Selection(
        string='Escala',
        selection=[
            ('1', '1 - Pésimo'),
            ('2', '2 - Deficiente'),
            ('3', '3 - Regular'),
            ('4', '4 - Bueno'),
            ('5', '5 - Muy bueno')],
    )

    @api.onchange('scala')
    def _onchange_scala(self):
        if not self.line_id:
            return
        self.qualification_line = self.line_id.weight * int(self.scala)
