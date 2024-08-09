# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class PlanCateg(models.Model):
    _name = 'audit.plan.categ'
    _description = "Categoria de plan de auditoría"

    name = fields.Char(
        string=u'Nombre',
        required=True,
    )
    sequence_id = fields.Many2one(
        string=u'Secuencia de ediciones',
        comodel_name='ir.sequence',
        ondelete='restrict',
    )

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
        result = super(PlanCateg, self).create(values)
        return result

    plan_ids = fields.One2many(
        string=u'Ediciones',
        comodel_name='audit.plan',
        inverse_name='categ_id',
        copy=True,
    )


class Plan(models.Model):
    _name = "audit.plan"
    _inherit = ['mgmtsystem.validation.mail', 'mgmtsystem.code']
    _description = "Programa de auditorías"

    active = fields.Boolean('Active', default=True)
    audit_ids = fields.One2many(
        string=u'Auditorías',
        comodel_name='audit.audit',
        inverse_name='plan_id',
        copy=True,
    )

    categ_id = fields.Many2one(
        string=u'Categoría',
        comodel_name='audit.plan.categ',
        ondelete='restrict',
    )

    @api.onchange('categ_id')
    def _onchange_categ_id(self):
        self.name = self.categ_id.name

    sequence_id = fields.Many2one(
        string=u'Secuencia de ediciones',
        comodel_name='ir.sequence',
        related='categ_id.sequence_id',
    )

    name = fields.Char(
        string=u'Nombre',
        required=True,
        default="PROGRAMA DE AUDITORIA"
    )
    edition_id = fields.Many2one(
        string=u'Procedimiento',
        comodel_name='process.edition',
        domain="[('state', '=', 'validate_ok'), ('active', '=', True)]",
        ondelete='cascade',
    )

    numero = fields.Char(
        string="Numero de secuencia",
        readonly=True,
        required=True,
        copy=False,
        default='Sin definir'
    )

    parent_edition = fields.Many2one(
        comodel_name='audit.plan', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='audit.plan', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_audit.audit_plan_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
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
        for training in self.audit_ids:
            training.write({'aproval': True})

    def open_audit_ids(self):
        """Método para abrir los planes de auditoría relacionados al programa de auditorías
        """
        result = self.env.ref(
            'mgmtsystem_audit.audit_audit_action').read()[0]
        result['domain'] = [('id', 'in', self.audit_ids.ids)]
        result['context'] = {'default_plan_id': self.id}
        return result
