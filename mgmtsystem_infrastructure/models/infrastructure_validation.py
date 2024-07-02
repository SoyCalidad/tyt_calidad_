from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class MaintenancePlan(models.Model):
    _inherit = 'mgmtsystem.maintenance.plan'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'maintenance_plan_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'maintenance_plan_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'maintenance_plan_validation_id', string='Validación')

    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])

    def update_child_state(self, state):
        self.plan_to_maintenace_validation_users()
        for child in self.maintenance_ids:
            child.state = state

    def plan_to_maintenace_validation_users(self):
        for m in self.maintenance_ids:
            if not m.elaboration_step and self.elaboration_step:
                m.elaboration_step = [(6, 0, self.elaboration_step.ids)]
            if not m.review_step and self.review_step:
                m.review_step = [(6, 0, self.review_step.ids)]
            if not m.validation_step and self.validation_step:
                m.validation_step = [(6, 0, self.validation_step.ids)]

    def send_elaborate(self):
        super().send_elaborate()
        self.create_child_validation_users(self.maintenance_ids)
        for line in self.maintenance_ids:
            try:
                line.send_elaborate()
            except:
                pass


    def send_review(self):
        super().send_review()
        self.create_child_validation_users(self.maintenance_ids)
        for line in self.maintenance_ids:
            try:
                line.send_review(notify=False)
            except:
                pass


    def send_validate(self):
        super().send_validate()
        self.create_child_validation_users(self.maintenance_ids)
        for line in self.maintenance_ids:
            try:
                line.send_validate(notify=False)
            except:
                pass

    def send_validate_ok(self):
        super().send_validate_ok()
        self.create_child_validation_users(self.maintenance_ids)
        for line in self.maintenance_ids:
            try:
                line.send_validate_ok()
            except:
                pass

    def send_cancel(self):
        super().send_cancel()
        for line in self.maintenance_ids:
            try:
                line.send_cancel()
            except:
                pass


class MaintenancePlanValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    maintenance_plan_elaboration_id = fields.Many2one(
        'mgmtsystem.maintenance.plan', string='Padre')
    maintenance_plan_review_id = fields.Many2one(
        'mgmtsystem.maintenance.plan', string='Padre')
    maintenance_plan_validation_id = fields.Many2one(
        'mgmtsystem.maintenance.plan', string='Padre')


class MaintenanceMaintenance(models.Model):
    _inherit = 'mgmtsystem.maintenance'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'maintenance_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'maintenance_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'maintenance_validation_id', string='Validación')

    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])


class MaintenanceMaintenanceValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    maintenance_elaboration_id = fields.Many2one(
        'mgmtsystem.maintenance', string='Padre')
    maintenance_review_id = fields.Many2one(
        'mgmtsystem.maintenance', string='Padre')
    maintenance_validation_id = fields.Many2one(
        'mgmtsystem.maintenance', string='Padre')


class CalibrationPlan(models.Model):
    _inherit = 'mgmtsystem.calibration.plan'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'calibration_plan_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'calibration_plan_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'calibration_plan_validation_id', string='Validación')

    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])


class CalibrationPlanValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    calibration_plan_elaboration_id = fields.Many2one(
        'mgmtsystem.calibration.plan', string='Padre')
    calibration_plan_review_id = fields.Many2one(
        'mgmtsystem.calibration.plan', string='Padre')
    calibration_plan_validation_id = fields.Many2one(
        'mgmtsystem.calibration.plan', string='Padre')


class Calibration(models.Model):
    _inherit = 'mgmtsystem.calibration'

    elaboration_step = fields.One2many(
        'mgmtsystem.validation.step', 'calibration_elaboration_id', string='Elaboración')
    review_step = fields.One2many(
        'mgmtsystem.validation.step', 'calibration_review_id', string='Revisión')
    validation_step = fields.One2many(
        'mgmtsystem.validation.step', 'calibration_validation_id', string='Validación')

    process_id = fields.Many2one(
        'process.edition', string='Procedimiento', domain=[('active','=',True)])


class CalibrationValidation(models.Model):
    _inherit = 'mgmtsystem.validation.step'

    calibration_elaboration_id = fields.Many2one(
        'mgmtsystem.calibration', string='Padre')
    calibration_review_id = fields.Many2one(
        'mgmtsystem.calibration', string='Padre')
    calibration_validation_id = fields.Many2one(
        'mgmtsystem.calibration', string='Padre')
