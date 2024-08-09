# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class Categ(models.Model):
    _name = 'capa.categ'
    _description = "Categoria de programa de capacitación"

    name = fields.Char(
        string=u'Nombre',
        required=True,
    )
    sequence_id = fields.Many2one(
        string=u'Secuencia de ediciones',
        comodel_name='ir.sequence',
        ondelete='cascade',
    )

    @api.onchange('name')
    def _onchange_name(self):
        if self.sequence_id:
            self.sequence_id.name = 'Secuencia de '+self.name

    @api.model
    def create(self, values):
        sequence = self.env['ir.sequence'].sudo().create({
            'name': 'Secuencia de '+values.get('name'),
            'active': True,
            'prefix': 'Edición-nro.',
            'padding': 4,
            'number_next': 1,
            'number_increment': 1,
        })
        values['sequence_id'] = sequence.id
        result = super(Categ, self).create(values)
        return result

    def unlink(self):
        for categ in self:
            categ.sequence_id.unlink()
        return super(Categ, self).unlink()

    plan_ids = fields.One2many(
        string='plan',
        comodel_name='mgmtsystem.plan',
        inverse_name='categ_id',
    )


class Plan(models.Model):
    _name = "mgmtsystem.plan"
    _inherit = ['mgmtsystem.validation.mail', 'mgmtsystem.code']
    _description = "Programa de capacitaciones"

    training_ids = fields.One2many(
        string=u'Planes de Capacitaciones',
        comodel_name='mgmtsystem.plan.training',
        inverse_name='plan_id',
        copy=True,
        ondelete='cascade',
    )

    categ_id = fields.Many2one(
        string='Nombre',
        comodel_name='capa.categ',
        ondelete='restrict',
    )
    sequence_id = fields.Many2one(
        string=u'Secuencia de ediciones',
        comodel_name='ir.sequence',
        related='categ_id.sequence_id',
    )

    name = fields.Char(
        string=u'Nombre',
        required=True,
    )

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
        for training in self.training_ids:
            training.write({'aproval': True})

    trainings_count = fields.Integer(
        string='Planes de capacitación', compute='get_process_count')

    @api.depends('training_ids')
    def get_process_count(self):
        for each in self:
            if each.training_ids:
                each.trainings_count = len(each.training_ids)
            else:
                each.trainings_count = 0

    def action_trainings_views(self):
        ids = []
        action_rec = self.env.ref(
            'mgmtsystem_employees.hr_item_training_action').read()[0]
        # ids = [x.id for x in self.training_ids]

        domain = [('id', 'in', self.training_ids.ids)]
        action_rec['domain'] = domain
        action_rec['context'] = {}

        return action_rec
