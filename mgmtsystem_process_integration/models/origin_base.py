from odoo import api, fields, models, _


class ModelOrigin(models.AbstractModel):
    _name = 'model.origin.abstract'
    _description = 'Origen del modelo'

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
        result = super().write(values)
        self.verify_origin()
        return result

    def exist_origin(self, type, type_id):
        sql = ""
        if type == 'action_ids':
            sql = "select count(*) from mgmtsystem_action m join mgmtsystem_action_origin as o on o.action_id = m.id "
        if type == 'nonconformity_ids':
            sql = "select count(*) from mgmtsystem_nonconformity m join mgmtsystem_nonconformity_origin as o on o.nc_id = m.id "
        if type == 'target_ids':
            sql = "select count(*) from mgmtsystem_target m join mgmtsystem_target_origin as o on o.target_id = m.id "
        if type == 'risk_ids' or type == 'opp_ids':
            sql = "select count(*) from matrix_block_line m join matrix_block_line_origin as o on o.line_id = m.id "
        sql = ("%s where m.id = %s and o.origin_model_id = %s and o.origin_int_id = %s") % (
            sql, type_id, self.model_id.id, self.id)
        self.env.cr.execute(sql)
        res_all = self.env.cr.fetchall()
        if res_all[0][0] == 0:
            return False
        return True

    # Verifica que los origenes tengan de origen el presente
    def verify_origin(self):
        fields = ['target_ids', 'nonconformity_ids',
                  'action_ids', 'risk_ids', 'opp_ids', ]

        for field in fields:
            if hasattr(self, field):
                field_records = getattr(self, field)
                for record in field_records:
                    if not self.exist_origin(field, record.id):
                        record.write({
                            'origin_model_id': self.model_id.id,
                            'origin_int_id': self.id})


class Origin(models.Model):
    _name = 'model.origin'

    def verify_model(self, model):
        menu = ''
        action = ''
        print(model.id)
        action = self.env['ir.actions.act_window'].search(
            [('res_model', '=', model.model)], limit=1, order='id asc')
        if action:
            menu = self.env['ir.ui.menu'].search(
                [('action', '=', ('ir.actions.act_window', action.id))], limit=1, order='id asc')

        return [menu, action]

    def open_origin(self, model, id):
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        id = int(id)
        res = self.verify_model(model)
        menu = res[0].id if res[0] else None
        action = res[1].id if res[1] else None
        model = model.model
        record_url = base_url + "/web#id=" + \
            str(id) + "&view_type=form&model=%s&menu_id=%s&action=%s" % (model, menu, action)
        client_action = {
            'type': 'ir.actions.act_url',
            'name': "Origen",
            'target': 'new',
            'url': record_url,
        }

        return client_action
        # h = {
        #     'name': model.name,
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'res_model': model.model,
        #     'res_id': id,
        #     'type': 'ir.actions.act_window',
        #     'target': '_blank'
        # }

        # return h

    def open_origin_record(self):
        for record in self:
            if record.origin_model_id and record.origin_int_id:
                return self.open_origin(record.origin_model_id, record.origin_int_id)
            else:
                return None


class OpportunityOrigin(models.Model):
    _name = "matrix.block.line.origin"
    _inherit = 'model.origin'
    _description = "Origen"

    line_id = fields.Many2one(
        string='Oportunidad/Riesgo',
        comodel_name='matrix.block.line',
        ondelete='cascade',
    )
    origin_model_id = fields.Many2one(
        'ir.model', string='Modelo origen', required=True, ondelete='cascade') #ADDING ondelete='cascade' que causa errores al instalar modulo "soycalidad_fast_validation"
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
    _inherit = 'matrix.block.line'

    origin_model_id = fields.Many2one('ir.model', string='Modelo de origen')
    origin_int_id = fields.Integer(string='ID Origen')

    def create_origin(self, origin_model_id, origin_int_id):
        print("-- CREANDO ORIGEN --")
        return self.env['matrix.block.line.origin'].create({
            'line_id': self.id,
            'origin_model_id': origin_model_id,
            'origin_int_id': origin_int_id,
        })

    origin_ids = fields.One2many(
        string='Origenes',
        comodel_name='matrix.block.line.origin',
        inverse_name='line_id',
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


class MgmtsystemActionOrigin(models.Model):
    _name = "mgmtsystem.action.origin"
    _inherit = 'model.origin'
    _description = "Origen de acción"

    action_id = fields.Many2one(
        string='Acción',
        comodel_name='mgmtsystem.action',
        ondelete='cascade',
    )
    origin_model_id = fields.Many2one(
        'ir.model', string='Modelo origen', required=True, ondelete='cascade') #ADDING ondelete='cascade' que causa errores al instalar modulo "soycalidad_fast_validation"
    origin_int_id = fields.Integer(string='ID origen')
    origin_link = fields.Html(string='Link de origen',
                              compute='_compute_origin_link')

    @api.depends('origin_model_id', 'origin_int_id')
    def _compute_origin_link(self):
        for record in self:
            if record.origin_model_id and record.origin_int_id:
                record.origin_link = _("<a data-oe-id=%s data-oe-model='%s' href=#id=%s&model=%s>Ir al origen →</a>") % (
                    record.origin_int_id, record.origin_model_id.model, record.origin_int_id, record.origin_model_id.model)
            else:
                record.origin_link = ""


class MgmtsystemAction(models.Model):
    _inherit = "mgmtsystem.action"

    origin_model_id = fields.Many2one('ir.model', string='Modelo de origen')
    origin_int_id = fields.Integer(string='ID Origen')

    def create_origin(self, origin_model_id, origin_int_id):
        print("-- CREANDO ORIGEN --")
        return self.env['mgmtsystem.action.origin'].create({
            'action_id': self.id,
            'origin_model_id': origin_model_id,
            'origin_int_id': origin_int_id,
        })

    origin_ids = fields.One2many(
        string='Origenes',
        comodel_name='mgmtsystem.action.origin',
        inverse_name='action_id',
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

        action = super(MgmtsystemAction, self).create(values)

        if origin_model_id and origin_int_id:
            action.create_origin(origin_model_id, origin_int_id)

        return action

    def write(self, values):
        if values.get('origin_model_id', False) and values.get('origin_int_id', False):
            self.create_origin(values.get('origin_model_id'),
                               values.get('origin_int_id'))
            values['origin_model_id'] = False
            values['origin_int_id'] = None
        result = super(MgmtsystemAction, self).write(values)
        return result


class MgmtsystemNonconformityOrigin(models.Model):
    _name = "mgmtsystem.nonconformity.origin"
    _inherit = 'model.origin'
    _description = "Origen de No conformidad"

    nc_id = fields.Many2one(
        string='No conformidad',
        comodel_name='mgmtsystem.nonconformity',
        ondelete='cascade',
    )
    origin_model_id = fields.Many2one(
        'ir.model', string='Modelo origen', required=True, ondelete='cascade') #ADDING ondelete='cascade' que causa errores al instalar modulo "soycalidad_fast_validation"
    origin_int_id = fields.Integer(string='ID origen')
    origin_link = fields.Html(string='Link de origen',
                              compute='_compute_origin_link')

    @api.depends('origin_model_id', 'origin_int_id')
    def _compute_origin_link(self):
        for record in self:
            if record.origin_model_id and record.origin_int_id:
                record.origin_link = _("<a data-oe-id=%s data-oe-model='%s' href=#id=%s&model=%s>Ir al origen →</a>") % (
                    record.origin_int_id, record.origin_model_id.model, record.origin_int_id, record.origin_model_id.model)
            else:
                record.origin_link = ""


class MgmtsystemNonconformity(models.Model):
    _inherit = "mgmtsystem.nonconformity"

    origin_model_id = fields.Many2one('ir.model', string='Modelo de origen')
    origin_int_id = fields.Integer(string='ID Origen')

    def create_origin(self, origin_model_id, origin_int_id):
        print("-- CREANDO ORIGEN --")
        return self.env['mgmtsystem.nonconformity.origin'].create({
            'nc_id': self.id,
            'origin_model_id': origin_model_id,
            'origin_int_id': origin_int_id,
        })

    origin_ids = fields.One2many(
        string='Origenes',
        comodel_name='mgmtsystem.nonconformity.origin',
        inverse_name='nc_id',
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
        nc = super(MgmtsystemNonconformity, self).create(values)
        if origin_model_id and origin_int_id:
            nc.create_origin(origin_model_id, origin_int_id)
        return nc

    def write(self, values):
        if values.get('origin_model_id', False) and values.get('origin_int_id', False):
            self.create_origin(values.get('origin_model_id'),
                               values.get('origin_int_id'))
            values['origin_model_id'] = False
            values['origin_int_id'] = None
        result = super(MgmtsystemNonconformity, self).write(values)
        return result


class TargetOrigin(models.Model):
    _name = "mgmtsystem.target.origin"
    _inherit = 'model.origin'
    _description = "Origen de objetivo"

    target_id = fields.Many2one(
        string='Objetivo',
        comodel_name='mgmtsystem.target',
        ondelete='cascade',
    )
    origin_model_id = fields.Many2one(
        'ir.model', string='Modelo origen', required=True, ondelete='cascade') #ADDING ondelete='cascade' que causa errores al instalar modulo "soycalidad_fast_validation"
    origin_int_id = fields.Integer(string='ID origen')
    origin_link = fields.Html(string='Link de origen',
                              compute='_compute_origin_link')

    @api.depends('origin_model_id', 'origin_int_id')
    def _compute_origin_link(self):
        for record in self:
            if record.origin_model_id and record.origin_int_id:
                record.origin_link = _("<a data-oe-id=%s data-oe-model='%s' href=#id=%s&model=%s>Ir al origen →</a>") % (
                    record.origin_int_id, record.origin_model_id.model, record.origin_int_id, record.origin_model_id.model)
            else:
                record.origin_link = ""


class Target(models.Model):
    _inherit = 'mgmtsystem.target'

    origin_model_id = fields.Many2one('ir.model', string='Modelo de origen')
    origin_int_id = fields.Integer(string='ID Origen')

    def create_origin(self, origin_model_id, origin_int_id):
        print("-- CREANDO ORIGEN --")
        return self.env['mgmtsystem.target.origin'].create({
            'target_id': self.id,
            'origin_model_id': origin_model_id,
            'origin_int_id': origin_int_id,
        })

    origin_ids = fields.One2many(
        string='Origenes',
        comodel_name='mgmtsystem.target.origin',
        inverse_name='target_id',
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
        res = super().create(values)
        if origin_model_id and origin_int_id:
            res.create_origin(origin_model_id, origin_int_id)
        return res

    def write(self, values):
        if values.get('origin_model_id', False) and values.get('origin_int_id', False):
            self.create_origin(values.get('origin_model_id'),
                               values.get('origin_int_id'))
            values['origin_model_id'] = False
            values['origin_int_id'] = None
        return super().write(values)
