from odoo import api, fields, models, _


class ModelOrigin(models.AbstractModel):
    _inherit = 'model.origin.abstract'

    change_request_ids = fields.Many2many('soycalidad.change_request', string='Solicitudes de cambio')
    change_requests_count = fields.Integer(compute='_compute_change_requests_count', string='Solicitudes de cambio')
    
    @api.depends('change_request_ids')
    def _compute_change_requests_count(self):
        for each in self:
            each.change_requests_count = len(each.change_request_ids)

    def exist_origin(self, type, type_id):
        sql = ""
        if type == 'action_ids':
            sql = "select count(*) from mgmtsystem_action m join mgmtsystem_action_origin as o on o.action_id = m.id "
        elif type == 'nonconformity_ids':
            sql = "select count(*) from mgmtsystem_nonconformity m join mgmtsystem_nonconformity_origin as o on o.nc_id = m.id"
        elif type == 'target_ids':
            sql = "select count(*) from mgmtsystem_target m join mgmtsystem_target_origin as o on o.target_id = m.id "
        elif type == 'risk_ids' or type == 'opp_ids':
            sql = "select count(*) from matrix_block_line m join matrix_block_line_origin as o on o.line_id = m.id "
        elif type == 'change_request_ids':
            sql = "select count(*) from soycalidad_change_request m join soycalidad_change_request_origin as o on o.change_request_id = m.id "
        cons = ("%s where m.id = %s and o.origin_model_id = %s and o.origin_int_id = %s") % (
            sql, type_id, self.model_id.id, self.id)
        self.env.cr.execute(cons)
        res_all = self.env.cr.fetchall()
        if res_all[0][0] == 0:
            return False
        return True

    # Verifica que los origenes tengan de origen el presente
    def verify_origin(self):
        fields = ['target_ids', 'nonconformity_ids',
                  'action_ids', 'risk_ids', 'opp_ids', 'change_request_ids']

        for field in fields:
            if hasattr(self, field):
                field_records = getattr(self, field)
                for record in field_records:
                    if not self.exist_origin(field, record.id):
                        record.write({
                            'origin_model_id': self.model_id.id,
                            'origin_int_id': self.id})

    def get_form_view_by_model(self):
        view = self.env['ir.ui.view'].search(
            [('active', '=', True), ('model', '=', self.model_id.model)], order='priority asc', limit=1)
        if view:
            result = self.env.ref(view.xml_id).read()[0]
            result['res_id'] = self.id
            return result

    def open_change_request_view(self):
        ids = []
        action_rec = self.env.ref(
                'soycalidad_improve.soycalidad_change_request_action').read()[0]
        for each in self:
            ids.extend(each.change_request_ids.ids)
            domain = [('id', 'in', ids)]
            action_rec['domain'] = domain
            return action_rec


class ChangeRequestOrigin(models.Model):
    _name = "soycalidad.change_request.origin"
    _inherit = 'model.origin'
    _description = "Origen"

    change_request_id = fields.Many2one(
        string='Solicitud de cambio',
        comodel_name='soycalidad.change_request',
        ondelete='cascade',
    )
    origin_model_id = fields.Many2one(
        'ir.model', string='Modelo origen', required=True, ondelete='cascade') #adding ondelete='cascade'en Odoo v15
    origin_int_id = fields.Integer(string='ID origen')
    origin_link = fields.Html(string='Link de origen',
                              compute='_compute_origin_link')

    def open_origin_record(self):
        for record in self:
            if record.origin_model_id and record.origin_int_id:
                return self.open_origin(record.origin_model_id, record.origin_int_id)
            else:
                return None

    @api.depends('origin_model_id', 'origin_int_id')
    def _compute_origin_link(self):
        for record in self:
            if record.origin_model_id and record.origin_int_id:
                record.origin_link = _("<a data-oe-id=%s data-oe-model='%s' href=#id=%s&model=%s>Ir al origen →</a>") % (
                    record.origin_int_id, record.origin_model_id.model, record.origin_int_id, record.origin_model_id.model)
            else:
                record.origin_link = ""


class Opportunity(models.Model):
    _inherit = 'soycalidad.change_request'

    origin_model_id = fields.Many2one('ir.model', string='Modelo de origen')
    origin_int_id = fields.Integer(string='ID Origen')

    def create_origin(self, origin_model_id, origin_int_id):
        return self.env['soycalidad.change_request.origin'].create({
            'change_request_id': self.id,
            'origin_model_id': origin_model_id,
            'origin_int_id': origin_int_id,
        })

    origin_ids = fields.One2many(
        string='Origenes',
        comodel_name='soycalidad.change_request.origin',
        inverse_name='change_request_id',
    )
    count_origin_ids = fields.Integer(
        string='# de origenes',
        compute='_compute_count_origin_ids',
    )

    @api.depends('origin_ids')
    def _compute_count_origin_ids(self):
        for record in self:
            record.count_origin_ids = len(record.origin_ids)

    @api.model
    def create(self, values):
        # Asignación de valores para crear el origen
        origin_model_id = values.get('origin_model_id', False)
        origin_int_id = values.get('origin_int_id', False)
        values['origin_model_id'] = False
        values['origin_int_id'] = None

        line = super(Opportunity, self).create(values)

        if origin_model_id and origin_int_id:
            line.create_origin(origin_model_id, origin_int_id)

        return line

    def write(self, values):
        if values.get('origin_model_id', False) and values.get('origin_int_id', False):
            self.create_origin(values.get('origin_model_id'),
                               values.get('origin_int_id'))
            values['origin_model_id'] = False
            values['origin_int_id'] = None
        result = super(Opportunity, self).write(values)
        return result

