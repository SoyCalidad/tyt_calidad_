from odoo import _, api, fields, models


class ApprovalDummy(models.Model):
    _name = 'mgmtsystem.context.approval_process'
    _description = 'dummy'


class PolicySystem(models.Model):
    _name = 'mgmtsystem.context.system'
    _description = 'Identificador de sistema'

    name = fields.Char(string='Descripción')


class Version(models.Model):
    """La edición permite tener un control de versiones para los distintos modelos
    del sistema
    """

    _name = 'mgmtsystem.version'
    _description = 'Version'
    _inherit = 'iso_base.email_basic'

    code = fields.Char('Código',)
    company_id = fields.Many2one(
        'res.company', string='Compañia', default=lambda self: self.env.user.company_id.id)

    #################################################################

    version = fields.Integer(
        string='Número de versión', default=1, readonly=True, copy=False)
    deactivate_date = fields.Date(string='Fecha de expiración', readonly=True)
    unrevisioned_name = fields.Char(
        string='Nombre de la edición', copy=True, readonly=True)

    ### IMPORTANT ###
    # Overwrite this in the inherited class with comodel_name = class_name

    parent_edition = fields.Many2one(
        comodel_name='mgmtsystem.version', string='Padre', copy=False)
    old_versions = fields.One2many(
        comodel_name='mgmtsystem.version', string='Versiones antiguas',
        inverse_name='parent_edition', context={'active_version': False})

    def _copy_edition(self):
        new_edition = self.copy({
            'version': self.version,
            'deactivate_date': fields.Date.today(),
            'parent_edition': self.id,
        })
        return new_edition

    def action_open_older_versions(self):
        result = self.env.ref(
            'mgmtsystem_context.context_internal_issue_cancel_action').read()[0]
        result['domain'] = [('id', 'in', self.old_versions.ids)]
        result['context'] = {'active_version': False}
        return result

    def button_new_version(self):
        self.ensure_one()
        self._copy_edition()
        revno = self.version
        self.write({
            'version': revno + 1,
            'name': self.name
        })

    #####################################################################

    @api.model
    def create(self, values):
        res = super(Version, self).create(values)
        try:
            if 'unrevisioned_name' not in values:
                values['unrevisioned_name'] = values['name']
        except:
            pass
        return res

    def write(self, values):
        try:
            for edition in self:
                if 'name' in values and not values.get('version', edition.version):
                    values['unrevisioned_name'] = values['name']
        except:
            pass
        return super().write(values)
