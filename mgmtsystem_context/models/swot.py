from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError


class SWOT(models.Model):
    """Añade campos para el análisis swot
    """
    _name = 'mgmtsystem.context.swot'
    _inherit = ['mgmtsystem.validation.mail', 'mgmtsystem.code']
    _description = 'FODA'

    def _default_company(self):
        return self.env.user.company_id

    def _get_process_default(self):
        sequence = self.env['mgmt.process'].search([('code', '=', 'E-PE-1-')])
        code = sequence[0].code
        return sequence[0].id

    process_id = fields.Many2one(
        'mgmt.process', string='Proceso', domain=[('active','=',True)])

    name = fields.Char(string='Nombre', required=True)
    date = fields.Date(string='Fecha de Análisis')
    company_id = fields.Many2one(
        'res.company',
        'Compañia',
        default=_default_company,
    )
    fortalezas = fields.One2many(
        'mgmtsystem.context.swot.fortaleza',
        'swot_id',
        string='Fortalezas',
        copy=True)
    debilidades = fields.One2many(
        'mgmtsystem.context.swot.debilidad',
        'swot_id',
        string='Debilidades',
        copy=True)
    oportunidades = fields.One2many(
        'mgmtsystem.context.swot.oportunidad',
        'swot_id',
        string='Oportunidades',
        copy=True)
    amenazas = fields.One2many(
        'mgmtsystem.context.swot.amenaza',
        'swot_id',
        string='Amenazas',
        copy=True)
    item = fields.One2many(
        'mgmtsystem.context.swot.item',
        'swot_id',
        string='Item')
    cross_swot_id = fields.Many2one(
        'mgmtsystem.context.cross.swot', string='FODA Cruzado')
    parent_edition = fields.Many2one(
        comodel_name='mgmtsystem.context.swot', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='mgmtsystem.context.swot', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})
    active = fields.Boolean('Active', default=True)

    internal_total = fields.Float(
        compute='_compute_internal_total', string='Índice Total Factores Internos', digits=(16, 2))
    internal_interpretation = fields.Text(
        string='Interpretación (Factores internos)')

    external_total = fields.Float(
        compute='_compute_external_total', string='Índice Total Factores Externos', digits=(16, 2))
    external_interpretation = fields.Text(
        string='Interpretación (Factores externos)')

    @api.depends('oportunidades', 'amenazas')
    def _compute_external_total(self):
        opp_sum = sum([x.weighted_rating for x in self.oportunidades])
        ame_sum = sum([x.weighted_rating for x in self.amenazas])
        self.external_total = opp_sum + ame_sum

    @api.depends('fortalezas', 'debilidades')
    def _compute_internal_total(self):
        for_sum = sum([x.weighted_rating for x in self.fortalezas])
        deb_sum = sum([x.weighted_rating for x in self.debilidades])
        self.internal_total = for_sum + deb_sum

    internal_weight_sum = fields.Float(
        compute='_compute_internal_weight_sum', string='Suma pesos factores internos')
    internal_weight_rest = fields.Float(
        compute='_compute_internal_weight_sum', string='Faltante')

    @api.depends('fortalezas', 'debilidades')
    def _compute_internal_weight_sum(self):
        for_sum = sum([x.weight for x in self.fortalezas])
        deb_sum = sum([x.weight for x in self.debilidades])
        self.internal_weight_sum = for_sum + deb_sum
        self.internal_weight_rest = 1 - (for_sum + deb_sum)

    external_weight_sum = fields.Float(
        compute='_compute_external_weight_sum', string='Suma pesos factores externos')
    external_weight_rest = fields.Float(
        compute='_compute_external_weight_sum', string='Faltante')

    @api.depends('fortalezas', 'debilidades')
    def _compute_external_weight_sum(self):
        opp_sum = sum([x.weight for x in self.oportunidades])
        ame_sum = sum([x.weight for x in self.amenazas])
        self.external_weight_sum = opp_sum + ame_sum
        self.external_weight_rest = 1 - (opp_sum + ame_sum)

    @api.constrains('amenazas', 'oportunidades', 'fortalezas', 'debilidades')
    def _constrains_amenazas(self):
        if int(self.internal_weight_sum*100) > 100:
            raise ValidationError(
                'La sumatoria de fortalezas y debilidades no debe sobrepasar 1')
        if int(self.external_weight_sum*100) > 100:
            raise ValidationError(
                'La sumatoria de oportunidades y amenazas no debe sobrepasar 1')

    def open_cross_swot(self):
        result = self.env.ref(
            'mgmtsystem_context.cross_swot_action').read()[0]
        result['domain'] = [('swot_id', '=', self.id)]
        result['context'] = {'default_swot_id': self.id}
        return result

    def create_cross_swot(self):
        if self.state != 'validate_ok':
            raise UserError(
                'No puede crear estrategia para un FODA no validado')

    

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_context.context_swot_cancel_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result


class SWOTItem(models.Model):
    _name = 'mgmtsystem.context.swot.item'
    _description = 'Entrada de FODA'

    swot_id = fields.Many2one('mgmtsystem.context.swot', string='FODA')
    code = fields.Char(string='Código')
    name = fields.Text(string='Descripción', required=True)
    context_type = fields.Selection([
        ('internal', 'Factor Interno'),
        ('external', 'Factor externo')
    ], string='Tipo de Factor')
    type = fields.Selection([
        ('str', 'Fortaleza'),
        ('wea', 'Debilidad'),
        ('dan', 'Amenaza'),
        ('opp', 'Oportunidad')
    ], string='Tipo')

    weight = fields.Float(string='Peso', digits=(16, 2), required=True)
    rating = fields.Selection([
        ('1', '1 (Respuesta mala)'),
        ('2', '2 (Respuesta media)'),
        ('3', '3 (Respuesta superior a la media)'),
        ('4', '4 (Respuesta superior)'),
    ], string='Calificación')

    weighted_rating = fields.Float(
        compute='_compute_weighted_rating', string='Calificación Ponderada', digits=(16, 2))

    weigth_html_warning = fields.Boolean(string='Advertencia de peso')

    internal_weight_sum = fields.Float(
        related='swot_id.internal_weight_sum', string='Suma pesos factores internos')
    internal_weight_rest = fields.Float(
        related='swot_id.internal_weight_rest', string='Faltante')
    external_weight_sum = fields.Float(
        related='swot_id.external_weight_sum', string='Suma pesos factores externos')
    external_weight_rest = fields.Float(
        related='swot_id.external_weight_rest', string='Faltante')

    @api.depends('rating', 'weight')
    def _compute_weighted_rating(self):
        res = 0.0
        for each in self:
            if each.weight and each.rating:
                res = each.weight*float(each.rating)
            each.weighted_rating = res


class Fortalezas(models.Model):
    _inherit = 'mgmtsystem.context.swot.item'
    _name = 'mgmtsystem.context.swot.fortaleza'
    _description = 'Fortalezas FODA'

    context_type = fields.Selection([
        ('internal', 'Factor Interno'),
        ('external', 'Factor externo')
    ], string='Tipo de Factor', default='internal')

    rating = fields.Selection([
        ('3', '3 (Fortaleza Menor)'),
        ('4', '4 (Fortaleza Mayor)'),
    ], string='Calificación')

    # @api.onchange('weight')
    # def _onchange_weight(self):
    #     sum_t = sum([x.weight for x in self.swot_id.fortalezas])
    #     if sum_t > 0.5:
    #         self.weight = 0.0
    #         self.weigth_html_warning = True
    #     else:
    #         self.weigth_html_warning = False


class Debilidades(models.Model):
    _inherit = 'mgmtsystem.context.swot.item'
    _name = 'mgmtsystem.context.swot.debilidad'
    _description = 'Debilidades FODA'

    context_type = fields.Selection([
        ('internal', 'Factor Interno'),
        ('external', 'Factor externo')
    ], string='Tipo de Factor', default='internal')

    rating = fields.Selection([
        ('1', '1 (Debilidad Menor)'),
        ('2', '2 (Debilidad Mayor)'),
    ], string='Calificación')

    # @api.onchange('weight')
    # def _onchange_weight(self):
    #     sum_t = sum([x.weight for x in self.swot_id.debilidades])
    #     if sum_t > 0.5:
    #         self.weight = 0.0
    #         self.weigth_html_warning = True
    #     else:
    #         self.weigth_html_warning = False


class Oportunidades(models.Model):
    _inherit = 'mgmtsystem.context.swot.item'
    _name = 'mgmtsystem.context.swot.oportunidad'
    _description = 'Oportunidades FODA'

    context_type = fields.Selection([
        ('internal', 'Factor Interno'),
        ('external', 'Factor externo')
    ], string='Tipo de Factor', default='external')

    rating = fields.Selection([
        ('1', '1 (Respuesta mala)'),
        ('2', '2 (Respuesta media)'),
        ('3', '3 (Respuesta superior a la media)'),
        ('4', '4 (Respuesta superior)'),
    ], string='Calificación', help='Se asigna la calificación del factor, entre 1 y 4, para definir si las estrategias de la empresa están respondiendo con eficacia al factor')

    # @api.onchange('weight')
    # def _onchange_weight(self):
    #     sum_t = sum([x.weight for x in self.swot_id.oportunidades]
    #                 )
    #     if sum_t > 0.5:
    #         self.weight = 0.0
    #         self.weigth_html_warning = True
    #     else:
    #         self.weigth_html_warning = False


class Amenazas(models.Model):
    _inherit = 'mgmtsystem.context.swot.item'
    _name = 'mgmtsystem.context.swot.amenaza'
    _description = 'Amenazas FODA'

    context_type = fields.Selection([
        ('internal', 'Factor Interno'),
        ('external', 'Factor externo')
    ], string='Tipo de Factor', default='external')


class CrossSWOT(models.Model):
    _name = 'mgmtsystem.context.cross.swot'
    _inherit = 'mgmtsystem.validation.mail'
    _description = 'FODA Cruzado'

    swot_id = fields.Many2one(
        'mgmtsystem.context.swot', string='FODA', domain="[('state','=', 'validate_ok')]")
    name = fields.Char(string='Nombre')
    fo = fields.One2many('mgmtsystem.context.cross.swot.fo',
                         'cross_swot_id', string='FO')
    do = fields.One2many('mgmtsystem.context.cross.swot.do',
                         'cross_swot_id', string='DO')
    fa = fields.One2many('mgmtsystem.context.cross.swot.fa',
                         'cross_swot_id', string='FA')
    da = fields.One2many('mgmtsystem.context.cross.swot.da',
                         'cross_swot_id', string='DA')
    parent_edition = fields.Many2one(
        comodel_name='mgmtsystem.context.cross.swot', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='mgmtsystem.context.cross.swot', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})
    active = fields.Boolean('Active', default=True)

    

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_context.cross_swot_cancel_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result

    def create_action_for_stra(self):
        pass

    def action_see_actions(self):

        domain = ['|', '|', '|', ('fo_ids', 'in', self.fo.ids), ('do_ids', 'in', self.do.ids), (
            'fa_ids', 'in', self.fa.ids), ('da_ids', 'in', self.da.ids)]

        return {
            'type': 'ir.actions.act_window',
            'name': _('Acciones'),
            'res_model': 'mgmtsystem.action',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': domain,
        }


class CrossSWOTItem(models.Model):
    _name = 'mgmtsystem.context.cross.swot.item'

    code = fields.Char(string='Código',)
    cross_swot_id = fields.Many2one(
        'mgmtsystem.context.cross.swot', string='FODA Cruzado')
    swot_id = fields.Many2one(
        'mgmtsystem.context.swot', related='cross_swot_id.swot_id', string='FODA', readonly=True)
    name = fields.Text(string='Estrategia')


class MgmtsystemAction(models.Model):
    _inherit = "mgmtsystem.action"

    fo_ids = fields.Many2many(
        'mgmtsystem.context.cross.swot.fo',
        'mgmtsystem_fo_action_rel',
        'action_id',
        'fo_id',
        'Estrategias FO',
        readonly=True,
    )
    do_ids = fields.Many2many(
        'mgmtsystem.context.cross.swot.do',
        'mgmtsystem_do_action_rel',
        'action_id',
        'do_id',
        'Estrategias DO',
        readonly=True,
    )
    fa_ids = fields.Many2many(
        'mgmtsystem.context.cross.swot.fa',
        'mgmtsystem_fa_action_rel',
        'action_id',
        'fa_id',
        'Estrategias FA',
        readonly=True,
    )
    da_ids = fields.Many2many(
        'mgmtsystem.context.cross.swot.da',
        'mgmtsystem_da_action_rel',
        'action_id',
        'da_id',
        'Estrategias DA',
        readonly=True,
    )

    do_count = fields.Integer(
        string='Estrategias DO', compute='_compute_do_ids')

    @api.depends('do_ids')
    def _compute_do_ids(self):
        for each in self:
            each.do_count = len(each.do_ids)

    fo_count = fields.Integer(
        string='Estrategias FO', compute='_compute_fo_ids')

    @api.depends('fo_ids')
    def _compute_fo_ids(self):
        for each in self:
            each.fo_count = len(each.fo_ids)

    fa_count = fields.Integer(
        string='Estrategias FA', compute='_compute_fa_ids')

    @api.depends('fa_ids')
    def _compute_fa_ids(self):
        for each in self:
            each.fa_count = len(each.fa_ids)

    da_count = fields.Integer(
        string='Estrategias DA', compute='_compute_da_ids')

    @api.depends('da_ids')
    def _compute_da_ids(self):
        for each in self:
            each.da_count = len(each.da_ids)


class CrossSWOTFO(models.Model):
    _name = 'mgmtsystem.context.cross.swot.fo'
    _inherit = 'mgmtsystem.context.cross.swot.item'
    _description = 'Fortalezas-Oportunidade FODA Cruzado'

    fortaleza = fields.Many2one(
        'mgmtsystem.context.swot.fortaleza',
        string='Fortaleza Fuente',
        domain="[('swot_id','=', swot_id)]", required=True)
    fortaleza_code = fields.Char(string='Fortaleza', related='fortaleza.code')
    oportunidad = fields.Many2one(
        'mgmtsystem.context.swot.oportunidad',
        string='Oportunidad Fuente',
        domain="[('swot_id','=', swot_id)]", required=True)
    oportunidad_code = fields.Char(
        string='Oportunidad', related='oportunidad.code')
    action_ids = fields.Many2many(
        'mgmtsystem.action',
        'mgmtsystem_fo_action_rel',
        'fo_id',
        'action_id',
        'Acciones',
    )
    action_count = fields.Integer(
        string='Acciones', compute='_compute_action_ids')

    @api.depends('action_ids')
    def _compute_action_ids(self):
        for each in self:
            each.action_count = len(each.action_ids)

    def write(self, values):
        result = super(CrossSWOTFO, self).write(values)
        return result


class CrossSWOTDO(models.Model):
    _name = 'mgmtsystem.context.cross.swot.do'
    _inherit = 'mgmtsystem.context.cross.swot.item'
    _description = 'Debilidades-Oportunidades FODA Cruzado'

    debilidad = fields.Many2one(
        'mgmtsystem.context.swot.debilidad',
        string='Debilidad Fuente',
        domain="[('swot_id','=', swot_id)]")
    debilidad_code = fields.Char(string='Debilidad', related='debilidad.code')
    oportunidad = fields.Many2one(
        'mgmtsystem.context.swot.oportunidad',
        string='Oportunidad Fuente',
        domain="[('swot_id','=', swot_id)]")
    oportunidad_code = fields.Char(
        string='Oportunidad', related='oportunidad.code')
    action_ids = fields.Many2many(
        'mgmtsystem.action',
        'mgmtsystem_do_action_rel',
        'do_id',
        'action_id',
        'Acciones',
    )
    action_count = fields.Integer(
        string='Acciones', compute='_compute_action_ids')

    @api.depends('action_ids')
    def _compute_action_ids(self):
        for each in self:
            each.action_count = len(each.action_ids)


class CrossSWOTFA(models.Model):
    _name = 'mgmtsystem.context.cross.swot.fa'
    _inherit = 'mgmtsystem.context.cross.swot.item'
    _description = 'Fortalezas-Amenazas FODA Cruzado'

    fortaleza = fields.Many2one(
        'mgmtsystem.context.swot.fortaleza',
        string='Fortaleza Fuente',
        domain="[('swot_id','=', swot_id)]")
    fortaleza_code = fields.Char(string='Fortaleza', related='fortaleza.code')
    amenaza = fields.Many2one(
        'mgmtsystem.context.swot.amenaza',
        string='Amenaza Fuente',
        domain="[('swot_id','=', swot_id)]")
    amenaza_code = fields.Char(string='Amenaza', related='amenaza.code')
    action_ids = fields.Many2many(
        'mgmtsystem.action',
        'mgmtsystem_fa_action_rel',
        'fa_id',
        'action_id',
        'Acciones',
    )
    action_count = fields.Integer(
        string='Acciones', compute='_compute_action_ids')

    @api.depends('action_ids')
    def _compute_action_ids(self):
        for each in self:
            each.action_count = len(each.action_ids)


class CrossSWOTDA(models.Model):
    _name = 'mgmtsystem.context.cross.swot.da'
    _inherit = 'mgmtsystem.context.cross.swot.item'
    _description = 'Debilidades-Amenazas FODA Cruzado'

    debilidad = fields.Many2one(
        'mgmtsystem.context.swot.debilidad',
        string='Debilidad Fuente',
        domain="[('swot_id','=', swot_id)]")
    debilidad_code = fields.Char(string='Debilidad', related='debilidad.code')
    amenaza = fields.Many2one(
        'mgmtsystem.context.swot.amenaza',
        string='Amenaza Fuente',
        domain="[('swot_id','=', swot_id)]")
    amenaza_code = fields.Char(string='Amenaza', related='amenaza.code')
    action_ids = fields.Many2many(
        'mgmtsystem.action',
        'mgmtsystem_da_action_rel',
        'da_id',
        'action_id',
        'Acciones',
    )
    action_count = fields.Integer(
        string='Acciones', compute='_compute_action_ids')

    @api.depends('action_ids')
    def _compute_action_ids(self):
        for each in self:
            each.action_count = len(each.action_ids)
