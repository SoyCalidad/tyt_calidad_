from odoo import api, fields, models
from odoo.exceptions import Warning, UserError


class InternalIssue(models.Model):
    _name = 'mgmtsystem.context.internal_issue'
    _inherit = ['mgmtsystem.context.internal_issue', 'mgmtsystem.level']

    items_level_1 = fields.One2many(
        'checklist.item', 'internal_issue_id1', string='Requisitos nivel 1')
    items_level_2 = fields.One2many(
        'checklist.item', 'internal_issue_id2', string='Requisitos nivel 2')
    items_level_3 = fields.One2many(
        'checklist.item', 'internal_issue_id3', string='Requisitos nivel 3')

    def send_review(self):
        if not self.review_ids:
            raise UserError('Ingrese los usuarios de Revisado')
        res = super(InternalIssue, self).send_review()
        self.verify_policy_level(self.current_level)
        return res

    def send_validate(self):
        res = super(InternalIssue, self).send_validate()
        self.verify_policy_level(self.current_level)
        return res

    def send_validate_ok(self):
        res = super(InternalIssue, self).send_validate_ok()
        self.verify_policy_level(self.current_level)
        return res

    def verify_policy_level(self, current_level):
        _na = {
            'na': [],
            '1': ['1', '2', '3'],
            '2': ['2', '3'],
            '3': ['3'],
        }
        for each in self:
            if each.quality_policy:
                if each.quality_policy.current_level and current_level:
                    print (each.quality_policy.current_level, current_level)
                    if each.quality_policy.current_level in _na[current_level]:
                        pass
                    else:
                        raise Warning(
                            'La política de calidad tiene un nivel inferior al solicitado')

    @api.model
    def default_get(self, fields_list):
        res = super(InternalIssue, self).default_get(fields_list)
        vals1 = [(0, 0, {'name': 'Trabajadores'}), ]
        vals2 = [(0, 0, {'name': 'Proveedores'}),
                 (0, 0, {'name': 'Clientes'}), ]
        vals3 = [(0, 0, {'name': 'Demás partes interesadas'}), ]
        res.update({'items_level_1': vals1})
        res.update({'items_level_2': vals2})
        res.update({'items_level_3': vals3})
        return res

    def verify_required(self, current_level):
        self.verify_policy_level(current_level)
        return True

    def write(self, values):
        result = super(InternalIssue, self).write(values)
        self.verify_policy_level(self.current_level)
        if not self.morals:
            raise Warning('Los valores son obligatorios')
        return result

    @api.model
    def create(self, values):
        result = super(InternalIssue, self).create(values)
        if not result.morals:
            raise Warning('Los valores son obligatorios')
        return result


class ContextPolicyTemplate(models.Model):
    _inherit = 'mgmtsystem.context.policy.template'

    social_resp = fields.Text(string='Responsabilidad social')
    ethic_behavior = fields.Text(string='Comportamiento ético')


class ContextPolicy(models.Model):
    _name = 'mgmtsystem.context.policy'
    _inherit = ['mgmtsystem.context.policy', 'mgmtsystem.level']

    social_resp = fields.Text(string='Responsabilidad social')
    ethic_behavior = fields.Text(string='Comportamiento ético', required=True)

    items_level_1 = fields.One2many(
        'checklist.item', 'policy_id1', string='Requisitos nivel 1')
    items_level_2 = fields.One2many(
        'checklist.item', 'policy_id2', string='Requisitos nivel 2')
    items_level_3 = fields.One2many(
        'checklist.item', 'policy_id3', string='Requisitos nivel 3')

    def write(self, values):
        result = super(ContextPolicy, self).write(values)
        if self.current_level == '3' and not self.social_resp:
            raise Warning(
                'La política de responsabilidad social es necesaria para el nivel 3')
        return result

    # def verify_required(self):
    #     self.verify_policy_level()
