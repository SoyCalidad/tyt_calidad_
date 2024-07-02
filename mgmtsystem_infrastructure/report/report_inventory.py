from odoo import fields, models


class MgmtsystemMaintenanceReportWizard(models.TransientModel):
    _name = 'mgmtsystem.maintenance.report_wizard'
    _inherit = 'mgmtsystem.report_wizard'
    _description = 'Mgmtsystem Maintenance Report Wizard'

    maintenance_ids = fields.Many2many(
        'mgmtsystem.maintenance', string='Planes de mantenimiento')

    def action_print(self):
        return self.action_print_parameters(
            'mgmtsystem_infrastructure.action_report_maintenance_plan', self.maintenance_ids)


class MgmtsystemCalibrationReportWizard(models.Model):
    _name = 'mgmtsystem.calibration.report_wizard'
    _inherit = 'mgmtsystem.report_wizard'
    _description = 'Mgmtsystem Calibration Report Wizard'

    calibration_ids = fields.Many2many(
        'mgmtsystem.calibration', string='Planes de calibración')

    def action_print(self):
        return self.action_print_parameters(
            'mgmtsystem_infrastructure.action_report_calibration_plan', self.calibration_ids)
