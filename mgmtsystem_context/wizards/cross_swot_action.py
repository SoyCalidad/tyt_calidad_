from odoo import models, fields, api, _


class CrossSwotFOWizardAction(models.TransientModel):
    _name = 'mgmtsystem.context.cross.swot.fo.action_wizard'

    action_ids = fields.Many2many(
        'mgmtsystem.action',
        'mgmtsystem_fo_action_wizard_rel',
        'fo_id',
        'action_id',
        'Acciones',
    )

    def create_action(self):
        fo = self.env['mgmtsystem.context.cross.swot.fo'].browse(self._context.get('active_id'))
        fo.write({
            'action_ids': [(6, 0, self.action_ids.ids)]
        })


class CrossSwotDOWizardAction(models.TransientModel):
    _name = 'mgmtsystem.context.cross.swot.do.action_wizard'

    action_ids = fields.Many2many(
        'mgmtsystem.action',
        'mgmtsystem_do_action_wizard_rel',
        'do_id',
        'action_id',
        'Acciones',
    )
    
    def create_action(self):
        fo = self.env['mgmtsystem.context.cross.swot.do'].browse(self._context.get('active_id'))
        fo.write({
            'action_ids': [(6, 0, self.action_ids.ids)]
        })


class CrossSwotFAWizardAction(models.TransientModel):
    _name = 'mgmtsystem.context.cross.swot.fa.action_wizard'

    action_ids = fields.Many2many(
        'mgmtsystem.action',
        'mgmtsystem_fa_action_wizard_rel',
        'fa_id',
        'action_id',
        'Acciones',
    )
    
    def create_action(self):
        fo = self.env['mgmtsystem.context.cross.swot.fa'].browse(self._context.get('active_id'))
        fo.write({
            'action_ids': [(6, 0, self.action_ids.ids)]
        })


class CrossSwotDAWizardAction(models.TransientModel):
    _name = 'mgmtsystem.context.cross.swot.da.action_wizard'

    action_ids = fields.Many2many(
        'mgmtsystem.action',
        'mgmtsystem_da_action_wizard_rel',
        'da_id',
        'action_id',
        'Acciones',
    )
    
    def create_action(self):
        fo = self.env['mgmtsystem.context.cross.swot.da'].browse(self._context.get('active_id'))
        fo.write({
            'action_ids': [(6, 0, self.action_ids.ids)]
        })
