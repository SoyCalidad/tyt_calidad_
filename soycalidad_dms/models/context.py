from odoo import api, fields, models


class InternalIssue(models.Model):
    _inherit = 'mgmtsystem.context.internal_issue'

    def set_root_directory(self):
        directory = 'soycalidad_dms.directory_context'
        return directory


class ExternalIssue(models.Model):
    _inherit = 'mgmtsystem.context.external_issue'

    def set_root_directory(self):
        directory = 'soycalidad_dms.directory_context'
        return directory


class SWOT(models.Model):
    _inherit = 'mgmtsystem.context.swot'

    def set_root_directory(self):
        directory = 'soycalidad_dms.directory_context'
        return directory


class PEST(models.Model):
    _inherit = 'mgmtsystem.context.pest'

    def set_root_directory(self):
        directory = 'soycalidad_dms.directory_context'
        return directory


class Stakeholders(models.Model):
    _inherit = 'mgmtsystem.stakeholders'

    def set_root_directory(self):
        directory = 'soycalidad_dms.directory_context'
        return directory


class Policy(models.Model):
    _inherit = 'mgmtsystem.context.policy'

    def set_root_directory(self):
        directory = 'soycalidad_dms.directory_context'
        return directory
