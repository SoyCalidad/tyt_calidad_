from odoo import api, fields, models


class Fortalezas(models.Model):
    _inherit = 'mgmtsystem.context.swot.fortaleza'

    target_ids = fields.Many2many('mgmtsystem.target', string='Objetivos')
    risk_ids = fields.Many2many('matrix.block.line',
                                relation='swot_fo_risk_rel',
                                string='Riesgos',
                                domain=[('type', '=', 'risk')])

    opp_ids = fields.Many2many('matrix.block.line',
                               relation='swot_fo_op_rel',
                               string='Oportunidades',
                               domain=[('type', '=', 'opportunity')])


class Debilidades(models.Model):
    _inherit = 'mgmtsystem.context.swot.debilidad'

    target_ids = fields.Many2many('mgmtsystem.target', string='Objetivos')
    risk_ids = fields.Many2many('matrix.block.line',
                                relation='swot_de_risk_rel',
                                string='Riesgos',
                                domain=[('type', '=', 'risk')])

    opp_ids = fields.Many2many('matrix.block.line',
                               relation='swot_de_op_rel',
                               string='Oportunidades',
                               domain=[('type', '=', 'opportunity')])


class Oportunidades(models.Model):
    _inherit = 'mgmtsystem.context.swot.oportunidad'

    target_ids = fields.Many2many('mgmtsystem.target', string='Objetivos')
    risk_ids = fields.Many2many('matrix.block.line',
                                relation='swot_op_risk_rel',
                                string='Riesgos',
                                domain=[('type', '=', 'risk')])

    opp_ids = fields.Many2many('matrix.block.line',
                               relation='swot_op_op_rel',
                               string='Oportunidades',
                               domain=[('type', '=', 'opportunity')])


class Amenazas(models.Model):
    _inherit = 'mgmtsystem.context.swot.amenaza'

    target_ids = fields.Many2many('mgmtsystem.target', string='Objetivos')
    risk_ids = fields.Many2many('matrix.block.line',
                                relation='swot_am_risk_rel',
                                string='Riesgos',
                                domain=[('type', '=', 'risk')])

    opp_ids = fields.Many2many('matrix.block.line',
                               relation='swot_am_op_rel',
                               string='Oportunidades',
                               domain=[('type', '=', 'opportunity')])
