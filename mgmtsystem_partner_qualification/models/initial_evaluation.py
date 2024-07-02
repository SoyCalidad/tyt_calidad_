# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InitialEvaluationItem(models.Model):
    _name = 'evaluation.initial_evaluation.item'
    _description = 'Criterio de evaluación inicial'

    name = fields.Char(string='Nombre')
    initial_evaluation_id = fields.Many2one(
        'evaluation.initial_evaluation', string='Evaluación')


class InitialEvaluation(models.Model):
    _name = 'evaluation.initial_evaluation'
    _inherit = 'mgmtsystem.validation.mail'
    _description = 'Evaluación inicial'

    # initial_evaluation_date = fields.Date(string='Fecha de evaluación')

    name = fields.Char(string='Nombre')
    final_criteria = fields.Text(string='Criterios de evaluación')
    item_ids = fields.One2many(
        'evaluation.initial_evaluation.item', 'initial_evaluation_id', string='Criterios', copy=True)


class PartnerInitialEvaluationItem(models.Model):
    _name = 'res.partner.initial_evaluation.item'
    _description = 'Criterio de evaluación incial de proveedor'

    name = fields.Char(string='Nombre')

    yes = fields.Boolean(string='Sí')
    no = fields.Boolean(string='No')
    no_apply = fields.Boolean(string='No Aplica') #making it compatible with odoo v15
    initial_evaluation_id = fields.Many2one(
        'res.partner.initial_evaluation', string='Evaluación')

    @api.onchange('yes')
    def _onchange_yes(self):
        if self.yes:
            self.no = False
            self.no_apply = False

    @api.onchange('no')
    def _onchange_no(self):
        if self.no:
            self.yes = False
            self.no_apply = False

    @api.onchange('no_apply')
    def _onchange_no_apply(self):
        if self.no_apply:
            self.yes = False
            self.no = False


class PartnerInitialEvaluation(models.Model):
    _name = 'res.partner.initial_evaluation'
    _inherit = ['mgmtsystem.code']
    _description = 'Evaluación inicial de proveedor'
    _rec_name = 'initial_evaluation_id'

    initial_evaluation_id = fields.Many2one(
        'evaluation.initial_evaluation', string='Evaluación', domain="[('state','=','validate_ok')]", required=True)
    initial_evaluation_date = fields.Datetime(
        string='Fecha y hora de selección')
    employee_id = fields.Many2one('hr.employee', string='Evaluador')
    final_criteria = fields.Text(string='Criterios de evaluación')
    observations = fields.Text(string='Observaciones')
    item_ids = fields.One2many(
        'res.partner.initial_evaluation.item', 'initial_evaluation_id', string='Criterios', copy=True)

    partner_id = fields.Many2one('res.partner', string='Proveedor')

    select_yes = fields.Boolean(string='Sí')
    select_no = fields.Boolean(string='No')

    @api.onchange('select_yes', 'select_no')
    def _onchange_select_yes(self):
        if self.select_yes:
            self.select_no = False
        if self.select_no:
            self.select_yes = False

    @api.onchange('initial_evaluation_id')
    def _onchange_initial_evaluation_id(self):
        for each in self:
            item_ids = []
            if each.initial_evaluation_id:
                each.final_criteria = each.initial_evaluation_id.final_criteria
                names = [x.name for x in each.initial_evaluation_id.item_ids]
                for name in names:
                    item_id = self.env['res.partner.initial_evaluation.item'].create({
                        'name': name,
                        'initial_evaluation_id': each.id,
                    })
                    item_ids.append(item_id.id)
            each.item_ids = [(6, 0, tuple(item_ids))]

    def print_evaluation(self):
        return self.env.ref('mgmtsystem_partner_qualification.action_report_initial_evaluation').report_action(self.id)


class ResPartner(models.Model):
    """ Hereda del modelo res.partner
    """
    _inherit = 'res.partner'

    initial_evaluation_ids = fields.One2many(
        'res.partner.initial_evaluation', 'partner_id', string='Evaluaciones')

    current_initial_evaluation_id = fields.Many2one(
        'res.partner.initial_evaluation', compute='_compute_current_initial_evaluation_id', string='Evaluación')

    @api.depends('initial_evaluation_ids')
    def _compute_current_initial_evaluation_id(self):
        for each in self:
            ev = self.env['res.partner.initial_evaluation'].search(
                [('partner_id', '=', each.id)], order='initial_evaluation_date desc', limit=1)
            each.current_initial_evaluation_id = ev.id if ev else None

    product_ids = fields.Many2many(
        'product.product', string='Productos y servicios')

    # initial_evaluation_count = fields.Integer(
    #     string=u'Fichas',
    #     compute='initial_evaluation_count',
    #     store=False,
    # )

    # def initial_evaluation_count(self):
    #     for record in self:
    #         data = record.env['initial_evaluation.initial_evaluation'].search([('res.partner_picking_id', '=', record.id)])
    #         count = len(data)
    #         record['initial_evaluation_count'] = count
