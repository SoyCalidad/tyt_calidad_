from odoo import api, fields, models


class Action(models.Model):
    _name = 'mgmtsystem.action'
    _inherit = ['mgmtsystem.action', 'model.origin.abstract']

    risk_ids = fields.Many2many('matrix.block.line',
                                relation='action_risk_rel',
                                column1='risk_id',
                                column2='action_id',
                                string='Riesgos',
                                domain=[('type', '=', 'risk')])
    risks_count = fields.Integer(
        compute='_compute_risks_count', string='Riesgos')

    opp_ids = fields.Many2many('matrix.block.line',
                               relation='action_op_rel',
                               column1='opp_id',
                               column2='action_id',
                               string='Oportunidades',
                               domain=[('type', '=', 'opportunity')])
    opps_count = fields.Integer(
        compute='_compute_opps_count', string='Oportunidades')

    @api.depends('risk_ids')
    def _compute_risks_count(self):
        for each in self:
            each.risks_count = 0
            if each.risk_ids:
                each.risks_count = len(each.risk_ids)

    @api.depends('opp_ids')
    def _compute_opps_count(self):
        for each in self:
            each.opps_count = 0
            if each.opp_ids:
                each.opps_count = len(each.opp_ids)

    
    #Ayuda a ingresar el modelo de origen, no se guarda en la base de datos
    def compute_model_id(self):
        for record in self:
            record.model_id = self.env['ir.model'].search([('model','=',self._name)], limit=1)

    model_id = fields.Many2one(
        string='Modelo',
        comodel_name='ir.model',
        ondelete='cascade',
        compute=compute_model_id,
        store=False,
    )

    def write(self, values):
        result = super(Action, self).write(values)
        """if not self.env.user.has_group('mgmtsystem_action.group_action_readonly_printreport'):
            if self.env.user.id !='1' :
                if self.user_id != self.env.user:
                    raise UserError('Error: Sin permisos de Edición!')"""
        self.verify_origin()
        return result


    def action_action_views(self):
        type_action = self._context.get('type_action', '')
        if type_action == '':
            return
        ids = []

        if type_action == 'opp':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.show_opp_action_action').read()[0]
            ids = self.opp_ids.ids
            domain = [('id', 'in', ids)]
            action_rec['domain'] = domain

        elif type_action == 'risk':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.show_risk_action_action').read()[0]
            ids = self.risk_ids.ids
            domain = [('id', 'in', ids)]
            action_rec['domain'] = domain
        
        return action_rec



class RiskOppAction(models.Model):
    _inherit = 'matrix.block.line'

    action_ids = fields.Many2many(
        'mgmtsystem.action',
        relation='action_risk_rel',
        column1='action_id',
        column2='risk_id',)
    
    action_opp_ids = fields.Many2many(
        'mgmtsystem.action',
        relation='action_op_rel',
        column1='action_id',
        column2='opp_id',)
    
    actions_count = fields.Integer(
        compute='_compute_actions_count', string='Acciones')

    @api.depends('action_ids')
    def _compute_actions_count(self):
        for each in self:
            risk = 0
            opp = 0
            if each.action_ids:
                risk = len(each.action_ids)
            if each.action_opp_ids:
                opp = len(each.action_opp_ids)
            each.actions_count = risk + opp
    
    def action_opportunity_action(self):
        action_rec = self.env.ref(
            'mgmtsystem_process_integration.show_ac_opportunity_action').read()[0]
        ids = self.action_ids.ids
        domain = [('id', 'in', ids)]
        action_rec['domain'] = domain
        return action_rec

    

    


