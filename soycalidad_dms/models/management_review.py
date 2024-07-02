from odoo import api, fields, models


class ManagementReviewPlan(models.Model):
    _inherit = 'management.review.plan'

    def set_root_directory(self):
        directory = 'soycalidad_dms.directory_review'
        return directory


class ManagementReview(models.Model):
    _inherit = 'management.review'

    def set_root_directory(self):
        directory = 'soycalidad_dms.directory_review'
        return directory
