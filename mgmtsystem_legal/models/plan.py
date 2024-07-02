# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class PlanCateg(models.Model):
    _name = 'legal.plan.categ'
    _description = "Categoria de plan legal"

    name = fields.Char(
        string=u'Nombre',
        required=True,
    )
    sequence_id = fields.Many2one(
        string=u'Secuencia de ediciones',
        comodel_name='ir.sequence',
        ondelete='restrict',
    )

    @api.onchange('name')
    def _onchange_name(self):
        self.sequence_id.name = 'Secuencia de '+self.name

    @api.model
    def create(self, values):
        sequence = self.env['ir.sequence'].create({
            'name': 'Secuencia de '+values.get('name'),
            'active': True,
            'prefix': 'Edición-nro.',
            'padding': 4,
            'number_next': 1,
            'number_increment': 1,
        })
        values['sequence_id'] = sequence.id
        result = super(PlanCateg, self).create(values)
        return result

    def unlink(self):
        for categ in self:
            categ.sequence_id.unlink()
        return super(PlanCateg, self).unlink()

    plan_ids = fields.One2many(
        string='plan',
        comodel_name='legal.plan',
        inverse_name='categ_id',
    )


class Plan(models.Model):
    _name = "legal.plan"
    _inherit = ['mgmtsystem.validation.mail', 'mgmtsystem.code']
    _description = "Programa de requisitos legales"

    parent_edition = fields.Many2one(
        comodel_name='legal.plan', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='legal.plan', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_legal.legal_plan_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result

    legal_ids = fields.Many2many(
        string='Requisitos',
        comodel_name='legal.legal',
        relation='plan_legal_leegal_rel',
        column1='plan_id',
        column2='legal_id',
    )

    line_ids = fields.One2many(
        string='Detalle de plan',
        comodel_name='legal.plan.line',
        inverse_name='plan_id',
    )

    history_ids = fields.One2many(
        string=u'Historial',
        comodel_name='legal.plan.history',
        inverse_name='plan_id',
    )

    name = fields.Char(
        string=u'Nombre',
    )

    @api.depends('categ_id', 'reference')
    def _compute_name(self):
        for record in self:
            if not record.categ_id:
                record.name = ''
            record.name = ("%s %s") % (record.categ_id.name, record.numero)

    reference = fields.Char(
        string="Referencia externa",
        readonly=True,
        required=True,
        copy=False,
        default='Sin definir'
    )

    categ_id = fields.Many2one(
        string=u'Categoría',
        comodel_name='legal.plan.categ',
        ondelete='restrict',
    )

    def _default_edition(self):
        process = self.env['res.company'].browse(
            self.env.user.company_id.id).legal_process_id
        if process:
            edition = self.env['process.edition'].search([
                ('process_id', '=', process.id),
                ('state', '=', 'validate_ok'),
                ('active', '=', True)
            ], order='create_date desc', limit=1)
            return edition
        else:
            return

    # edition_id = fields.Many2one(
    #     string=u'Procedimiento',
    #     comodel_name='process.edition',
    #     domain="[('state', '=', 'validate_ok')]",
    #     ondelete='cascade',
    #     default=_default_edition,
    #     required=True,
    # )

    @api.onchange('categ_id')
    def _onchange_categ_id(self):
        self.name = self.categ_id.name or "Plan de req. legales"

    sequence_id = fields.Many2one(
        string=u'Secuencia de ediciones',
        comodel_name='ir.sequence',
        related='categ_id.sequence_id',
    )

    numero = fields.Char(
        string="Numero de secuencia",
        readonly=True,
        required=True,
        copy=False,
        default='Sin definir'
    )

    state = fields.Selection(
        string=u'Estado',
        selection=[
            ('draft', 'Borrador'),
            ('plan', 'Plan'),
            ('elaborate', 'En elaboración'),
            ('review', 'En revisión'),
            ('validate', 'En validación'),
            ('validate_ok', 'Validado'),
            ('on_track', 'En seguimiento'),
            ('closed', 'Terminado'),
            ('cancel', 'Obsoleto')
        ],
        default='draft',
        copy=False,
    )

    def write(self, values):
        message = ""
        if len(self.categ_id.plan_ids) > 1 and values.get('state', False) == 'validate_ok':
            values['reference'] = self.categ_id.plan_ids[0].reference
            values['numero'] = self.sequence_id.next_by_id() or 'Sin definir'
            for plan in self.categ_id.plan_ids:
                if plan.state == 'validate_ok':
                    plan.write({'state': 'cancel'})
        elif values.get('reference', 'Sin definir') == 'Sin definir' and values.get('state', False) == 'validate_ok':
            values['reference'] = self.env['ir.sequence'].next_by_code(
                'planlegal.sequence') or 'Sin definir'

        if len(self.categ_id.plan_ids) == 1 and values.get('state', False) == 'validate_ok':
            values['numero'] = self.sequence_id.next_by_id() or 'Sin definir'

        result = super(Plan, self).write(values)

        if message != "":
            self.message_post(body=message)
        for legal in self.legal_ids:
            ids_ = [x.legal_id.id for x in self.line_ids]
            if legal.id not in ids_:
                self.env['legal.plan.line'].sudo().create({
                    'legal_id': legal.id,
                    'plan_id': self.id,
                })

        return result

    def unlink(self):
        for plan in self:
            if plan.state not in ('cancel'):
                raise UserError(
                    _('No puedes eliminar un plan que se encuentre en proceso. Deberías volverlo obsoleto.'))
        return super(Plan, self).unlink()

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

    def action_reset_all_aproval(self):
        for training in self.line_ids:
            training.write({'aproval': True})

    plan_state = fields.Selection([
        ('draft', 'Borrador'),
        ('plan', 'Plan')
    ], string='Fases del plan', default='draft')

    def init_plan(self):
        self.state = 'plan'

    def send_on_track(self):
        self.write({'state': 'on_track'})

    @api.onchange('legal_ids')
    def _onchange_legal_ids(self):
        pass

    def send_closed(self):
        if not self.history_ids:
            raise UserError('Las evaluaciones están vacías')
        self.write({'state': 'closed'})


class PlanLine(models.Model):
    _name = "legal.plan.line"
    _description = "Linea del plan legal"

    plan_id = fields.Many2one(
        string='Plan',
        comodel_name='legal.plan',
        ondelete='cascade',
    )
    legal_id = fields.Many2one(
        string=u'Requisito',
        comodel_name='legal.legal',
        ondelete='cascade',
    )
    entity_id = fields.Many2one(
        string=u'Entidad',
        related='legal_id.entity_id',
    )
    partner_id = fields.Many2one(
        string=u'Contacto',
        related='legal_id.partner_id',
    )
    date_release = fields.Date(
        string=u'Fecha de publicación',
        related='legal_id.date_release',
    )
    resume = fields.Text(
        string=u'Resumen',
        related='legal_id.resume',
    )
    action_id = fields.Many2one('mgmtsystem.action', string='Cómo se cumplirá')
    description_action = fields.Html(
        string='Descripción',
        related='action_id.description',
    )

    aproval = fields.Boolean(
        string=u'Aprobado',
        default=False,
    )
    observations = fields.Text(
        string=u'Observaciones',
    )

    user_id = fields.Many2one(
        string=u'Responsable',
        related='action_id.user_id',)

    # user_id = fields.Many2one('res.users', string='Responsable')

    state = fields.Selection(
        string=u'Estado',
        selection=[
            ('elaborate', 'En elaboración'),
            ('validate_ok', 'Validado'),
            ('on_track', 'En seguimiento'),
            ('closed', 'Terminado'),
            ('cancel', 'Obsoleto'),
        ],
        default='elaborate',
        copy=False,
    )


class HistoryLine(models.Model):
    _name = "legal.plan.history.line"
    _description = "Linea del historial del plan legal"

    history_id = fields.Many2one(
        string=u'Historial',
        comodel_name='legal.plan.history',
        ondelete='cascade',
    )
    legal_id = fields.Many2one(
        string=u'Requisito',
        comodel_name='legal.legal',
        ondelete='cascade',
        domain=[('state', '=', 'validate')],
        required=True,
    )
    date_track = fields.Date(
        string=u'Fecha de evaluación',
    )
    user_id = fields.Many2one(
        string=u'Evaluador',
        comodel_name='res.users',
        ondelete='cascade',
    )
    result = fields.Text(
        string=u'Resultados',
    )
    proposal_action_id = fields.Many2one(
        'mgmtsystem.action', string='Propuesta de acción')


class PlanHistory(models.Model):
    _name = "legal.plan.history"
    _description = 'Evaluación de plan legal'
    _order = 'date_track desc'

    name = fields.Char(
        string='Nombre',
        required=True,
    )

    plan_id = fields.Many2one(
        string='Programa',
        comodel_name='legal.plan',
        ondelete='cascade',
    )

    @api.onchange('plan_id')
    def _onchange_plan_id(self):
        if not self.plan_id:
            return
        ids_line = []
        for legal in self.plan_id.line_ids:
            tmp = self.env['legal.plan.history.line'].create({
                'legal_id': legal.legal_id.id,
            })
            ids_line.append(tmp.id)
        self.line_ids = ids_line

    line_ids = fields.One2many(
        string=u'Requisitos',
        comodel_name='legal.plan.history.line',
        inverse_name='history_id',
        copy=True,
    )

    date_track = fields.Date(
        string=u'Fecha de evaluación',
        default=fields.Date.context_today,
        required=True,
    )

    @api.onchange('date_track')
    def _onchange_date_track(self):
        self.name = 'Evaluación:'+str(self.date_track)
        for line in self.line_ids:
            line.date_track = self.date_track

    user_id = fields.Many2one(
        string=u'Evaluador',
        comodel_name='res.users',
        ondelete='cascade',
    )

    @api.onchange('user_id')
    def _onchange_user_id(self):
        if not self.user_id:
            return
        for line in self.line_ids:
            line.user_id = self.user_id

    observations = fields.Text(
        string=u'Observaciones',
    )
