from odoo import api, fields, models


class TrainingPlan(models.Model):
    _inherit = 'mgmtsystem.plan'

    def set_root_directory(self):
        directory = 'soycalidad_dms.directory_cap'
        return directory


class TrainingPlanLine(models.Model):
    _inherit = 'mgmtsystem.plan.training'

    def set_root_directory(self):
        directory = 'soycalidad_dms.directory_cap'
        return directory

class MgmtsystemContextOrganizationChart(models.Model):
    _inherit = 'mgmtsystem.context.organization_chart'
    
    def set_root_directory(self):
        directory = 'soycalidad_dms.directory_cap'
        return directory
    