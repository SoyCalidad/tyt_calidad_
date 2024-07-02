# -*- coding: utf-8 -*-

from odoo import _, api, fields, models, tools
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from odoo.tools import float_compare


class MaintenanceEquipmentCategory(models.Model):
    _inherit = 'maintenance.equipment.category'

    type = fields.Selection(
        string=u'',
        selection=[('tangible', 'Tangible'), ('intangible', 'Intangible')]
    )


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    barcode = fields.Char('Código de barras')
    default_code = fields.Char('Referencia interna', store=True)
    account_id = fields.Many2one(
        string=u'Cuenta contable',
        comodel_name='account.account',
        ondelete='cascade',
    )
    calibration_needed = fields.Boolean(string='Requiere calibración')

    def name_get(self):
        return [(template.id, '%s%s' % (template.default_code and '[%s] ' % template.default_code or '', template.name))
                for template in self]

    state = fields.Selection(
        string='Estado',
        selection=[('active', 'Activo'), ('inactive', 'Inactivo')],
        compute='_compute_state'
    )

    @api.depends('scrap_date')
    def _compute_state(self):
        for record in self:
            if record.scrap_date:
                if record.scrap_date < fields.Date.today():
                    record.state = 'inactive'
                else:
                    record.state = 'active'
            else:
                record.state = 'active'

    # Images

    # all image fields are base64 encoded and PIL-supported

    # all image_variant fields are technical and should not be displayed to the user
    image_variant_1920 = fields.Image(
        "Variant Image", max_width=1920, max_height=1920)

    # resized fields stored (as attachment) for performance
    image_variant_1024 = fields.Image(
        "Variant Image 1024", related="image_variant_1920", max_width=1024, max_height=1024, store=True)
    image_variant_512 = fields.Image(
        "Variant Image 512", related="image_variant_1920", max_width=512, max_height=512, store=True)
    image_variant_256 = fields.Image(
        "Variant Image 256", related="image_variant_1920", max_width=256, max_height=256, store=True)
    image_variant_128 = fields.Image(
        "Variant Image 128", related="image_variant_1920", max_width=128, max_height=128, store=True)
