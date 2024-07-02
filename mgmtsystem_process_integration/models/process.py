from odoo import api, fields, models
from odoo.exceptions import UserError


class MgmtCateg(models.Model):
    _inherit = 'mgmt.categ'
    _description = 'Mgmt Categ'

    # Version 2 fields

    purpose = fields.Text(
        string='Objetivo')
    start = fields.Text(
        string='Inicio')
    end = fields.Text(
        string='Fin')

    # Process

    resource_ids = fields.One2many(
        'mgmt.process.resource',
        'categ_id',
        string='Recursos')

    process_line_in_ids = fields.One2many(
        'mgmt.process.line',
        'categ_in_id',
        string='Lineas')

    process_line_out_ids = fields.One2many(
        'mgmt.process.line',
        'categ_out_id',
        string='Lineas')

    interaction_plan = fields.Many2many(
        'mgmt.process.interaction',
        string='Planificar',
        relation='categ_plan_rel',
        domain='[("type","=","plan")]')
    interaction_do = fields.Many2many(
        'mgmt.process.interaction',
        string='Hacer',
        relation='categ_do_rel',
        domain='[("type","=","do")]')
    interaction_verify = fields.Many2many(
        'mgmt.process.interaction',
        string='Verificar',
        relation='categ_verify_rel',
        domain='[("type","=","verify")]')
    interaction_act = fields.Many2many(
        'mgmt.process.interaction',
        string='Actuar',
        relation='categ_act_rel',
        domain='[("type","=","act")]')


class Process(models.Model):
    _name = 'mgmt.process'
    _inherit = ['mgmt.process', 'model.origin.abstract']

    purpose = fields.Text(
        string='Finalidad del proceso')
    resources = fields.Text(
        string='Recursos del proceso')
    risk_ids = fields.Many2many('matrix.block.line', relation='process_risk_rel',
                                string='Riesgos', domain=[('type', '=', 'risk')])
    risks_count = fields.Integer(
        compute='_compute_risks_count', string='Riesgos')

    opp_ids = fields.Many2many('matrix.block.line', relation='process_op_rel',
                               string='Oportunidades', domain=[('type', '=', 'opportunity')])
    opps_count = fields.Integer(
        compute='_compute_opps_count', string='Oportunidades')

    nonconformity_ids = fields.Many2many(
        'mgmtsystem.nonconformity', string='No conformidades', relation="nc_process_rel")
    nonconformities_count = fields.Integer(
        compute='_compute_nonconformities_count', string='No conformidades')

    action_ids = fields.Many2many(
        'mgmtsystem.action', string='Acciones', relation='action_process_rel')
    actions_count = fields.Integer(
        compute='_compute_actions_count', string='Acciones')

    legal_ids = fields.Many2many('legal.legal', string='Requisitos legales')
    legals_count = fields.Integer(
        compute='_compute_legals_count', string='Requisitos legales')

    def action_opp_views(self):
        ids = []
        action_rec = self.env.ref(
            'mgmtsystem_legal.legal_legal_action').read()[0]
        for each in self:
            ids.extend(each.legal_ids.ids)
        domain = [('id', 'in', ids)]
        action_rec['domain'] = domain
        return action_rec

    @api.depends('legal_ids')
    def _compute_legals_count(self):
        for each in self:
            each.legals_count = len(each.legal_ids)

    @api.depends('action_ids')
    def _compute_actions_count(self):
        for each in self:
            if each.action_ids:
                each.actions_count = len(self.action_ids)
            else:
                each.actions_count = 0

    @api.depends('nonconformity_ids')
    def _compute_nonconformities_count(self):
        for each in self:
            if each.nonconformity_ids:
                each.nonconformities_count = len(each.nonconformity_ids)
            else:
                each.nonconformities_count = 0

    # Ayuda a ingresar el modelo de origen, no se guarda en la base de datos
    def compute_model_id(self):
        for record in self:
            record.model_id = self.env['ir.model'].search(
                [('model', '=', self._name)], limit=1)

    model_id = fields.Many2one(
        string='Modelo',
        comodel_name='ir.model',
        ondelete='cascade',
        compute=compute_model_id,
        store=False,
    )

    def write(self, values):
        result = super(Process, self).write(values)
        self.verify_origin()
        return result

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

    def action_opp_views(self):
        type_action = self._context.get(
            'type_action', '')
        if type_action == '':
            return
        ids = []
        if type_action == 'risk':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.show_risk_action_action').read()[0]
            for each in self:
                ids.extend(each.risk_ids.ids)
        elif type_action == 'opp':
            action_rec = self.env.ref(
                'mgmtsystem_process_integration.show_opp_action_action').read()[0]
            for each in self:
                ids.extend(each.opp_ids.ids)
        domain = [('id', 'in', ids)]
        action_rec['domain'] = domain
        return action_rec

    def action_legal_views(self):
        ids = []
        action_rec = self.env.ref(
            'mgmtsystem_legal.legal_legal_action').read()[0]
        for each in self:
            ids.extend(each.legal_ids.ids)
        domain = [('id', 'in', ids)]
        action_rec['domain'] = domain
        return action_rec

    # Process

    resource_ids = fields.One2many(
        'mgmt.process.resource', 'process_id', string='Recursos')

    process_line_in_ids = fields.One2many(
        'mgmt.process.line', 'process_in_id', string='Lineas')

    inputs_count = fields.Integer(compute='_compute_inputs', string='')

    @api.depends('process_line_in_ids')
    def _compute_inputs(self):
        total = 0
        for each in self:
            for line in each.process_line_in_ids:
                total += len(line.input_id)
            each.inputs_count = total

    clients_count = fields.Integer(
        compute='_compute_clients_count', string='Clientes')

    @api.depends('process_line_in_ids')
    def _compute_clients_count(self):
        total = 0
        for each in self:
            for line in each.process_line_in_ids:
                total += len(line.client_area_id)
            each.clients_count = total

    process_line_out_ids = fields.One2many(
        'mgmt.process.line', 'process_out_id', string='Lineas')

    outputs_count = fields.Integer(
        compute='_compute_outputs_count', string='Salidas')

    @api.depends('process_line_out_ids')
    def _compute_outputs_count(self):
        total = 0
        for each in self:
            for line in each.process_line_out_ids:
                total += len(line.output_id)
            each.outputs_count = total

    suppliers_count = fields.Integer(
        compute='_compute_suppliers_count', string='Proveedores')

    @api.depends('process_line_out_ids')
    def _compute_suppliers_count(self):
        total = 0
        for each in self:
            for line in each.process_line_out_ids:
                total += len(line.supplier_id)
            each.suppliers_count = total

    interaction_plan = fields.Many2many(
        'mgmt.process.interaction', string='Planificar', relation='process_plan_rel', domain='[("type","=","plan")]')
    interaction_do = fields.Many2many(
        'mgmt.process.interaction', string='Hacer', relation='process_do_rel', domain='[("type","=","do")]')
    interaction_verify = fields.Many2many(
        'mgmt.process.interaction', string='Verificar', relation='process_verify_rel', domain='[("type","=","verify")]')
    interaction_act = fields.Many2many(
        'mgmt.process.interaction', string='Actuar', relation='process_act_rel', domain='[("type","=","act")]')

    def action_print_report(self):
        edition_id = self.env['process.edition'].search(
            [('process_id', '=', self.id), ('active', '=', True)], limit=1)
        if edition_id:
            return self.env.ref('mgmtsystem_process.report_process_edition').report_action(edition_id)
        else:
            raise UserError(_('No se encontro una edicion para este proceso'))


class ProcessResourceType(models.Model):
    _name = 'mgmt.process.resource.type'
    _description = 'Tipo de recurso de proceso'

    name = fields.Text(string='TIpo')


class ProcessResource(models.Model):
    _name = 'mgmt.process.resource'

    process_id = fields.Many2one('mgmt.process', domain=[('active','=',True)], string='Procedimiento')
    categ_id = fields.Many2one('mgmt.categ', string='Proceso')

    name = fields.Char(string='Nombre')
    type_id = fields.Many2one('mgmt.process.resource.type', string='Tipo')
    description = fields.Text(string='Descripción')


class ProcessLineInteraction(models.Model):
    _name = 'mgmt.process.interaction'
    _description = 'Interacción de procesos'

    type = fields.Selection([
        ('plan', 'Planear'),
        ('do', 'Hacer'),
        ('verify', 'Verificar'),
        ('act', 'Actuar'),
    ], string='Tipo')

    name = fields.Text(string='Descripción')


class ProcessLineSupplier(models.Model):
    _name = 'mgmt.process.line.supplier'
    _description = 'Proveedor'

    name = fields.Reference(selection=[('res.partner', 'Proveedor externo'), (
        'mgmt.categ', 'Proveedor interno'), ], string="Proveedor")


class MgmtProcessLineOutputClient(models.Model):
    _name = 'mgmt.process.line.client_supplier'
    _description = 'Cliente/Proveedor'

    name = fields.Text(string='Nombre')
    type = fields.Selection([
        ('input', 'Proveedor'),
        ('output', 'Cliente'),
    ], string='Tipo')


class ProcessLine(models.Model):
    _name = 'mgmt.process.line'
    _description = 'Linea de proceso'

    # Inputs

    process_in_id = fields.Many2one(
        'mgmt.process', string='Procedimiento (Entradas)', domain=[('active','=',True)])
    categ_in_id = fields.Many2one('mgmt.categ', string='Proceso (Entrada)',)
    input_id = fields.Many2many('mgmt.process.line.input', string='Entrada')
    supplier_id = fields.Many2many(
        'mgmt.process.line.client_supplier', string='Proveedor', relation="input_supplier_process_rel", domain="[('type','=','input')]")

    # Outputs

    process_out_id = fields.Many2one(
        'mgmt.process', string='Procedimiento (Salida)', domain=[('active','=',True)])
    categ_out_id = fields.Many2one('mgmt.categ', string='Proceso (Salida)')
    output_id = fields.Many2many('mgmt.process.line.output', string='Salida')
    client_id = fields.Many2many(
        'mgmt.process.line.client_supplier', string='Cliente', relation="output_client_process_rel", domain="[('type','=','output')]")


class ProcessLineInput(models.Model):
    _name = 'mgmt.process.line.input'

    name = fields.Char(string='Nombre')
    description = fields.Text(string='Descripción')
    process_line_ids = fields.Many2many(
        'mgmt.process.line', string='Linea de proceso')


class ProcessLineOutput(models.Model):
    _name = 'mgmt.process.line.output'

    name = fields.Char(string='Nombre')
    description = fields.Text(string='Descripción')
    process_line_ids = fields.Many2many(
        'mgmt.process.line', string='Linea de proceso')


class NCProcess(models.Model):
    _inherit = 'mgmtsystem.nonconformity'

    process_ids = fields.Many2many(
        'mgmt.process', string='Procedimientos', relation="nc_process_rel", domain=[('active','=',True)])
    process_count = fields.Integer(
        compute='_compute_processs_count', string='Procedimientos')

    @api.depends('process_ids')
    def _compute_processs_count(self):
        for each in self:
            if each.process_ids:
                each.process_count = len(each.process_ids)
            else:
                each.process_count = 0


class ActionProcess(models.Model):
    _inherit = 'mgmtsystem.action'

    process_ids = fields.Many2many(
        'mgmt.process', string='Procedimientos', relation="action_process_rel", domain=[('active','=',True)])
    process_count = fields.Integer(
        compute='_compute_processs_count', string='Procedimientos')

    @api.depends('process_ids')
    def _compute_processs_count(self):
        for each in self:
            if each.process_ids:
                each.process_count = len(each.process_ids)
            else:
                each.process_count = 0
