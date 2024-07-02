from odoo import api, fields, models


class Validation(models.Model):
    _inherit = 'mgmtsystem.validation'

    def fast_validation(self):
        """Validación rápida para el registro actual"""
        child_fields = ['audit_ids', 'line_ids',
                        'training_ids', 'maintenance_ids']
        for val in self:
            steps = [(5, 0, 0)]
            current_user_id = self.env.user.id
            val.state = 'validate_ok'
            data = {
                'user_id': current_user_id,
                'check': True,
            }
            steps.append((0, 0, data))
            val.cancel_other_versions()
            val.elaboration_step = steps
            val.review_step = steps
            val.validation_step = steps
            val.date_review = fields.Date.today()
            val.date_validate = fields.Date.today()
            for child in child_fields:
                if hasattr(val, child):
                    lines = getattr(val, child)
                    for current in lines:
                        try:
                            current.state = 'validate_ok'
                        except:
                            pass
                        try:
                            current.elaboration_step = steps
                            current.review_step = steps
                            current.validation_step = steps
                            current.cancel_other_versions()
                        except:
                            pass


class PlanInfrastructure(models.Model):
    _inherit = 'mgmtsystem.infrastructure'

    def fast_validation(self):
        """Validación rápida para el registro actual"""
        child_fields = ['audit_ids', 'line_ids',
                        'training_ids', 'maintenance_ids']
        for val in self:
            steps = [(5, 0, 0)]
            current_user_id = self.env.user.id
            val.state = 'validate_ok'
            data = {
                'user_id': current_user_id,
                'check': True,
            }
            steps.append((0, 0, data))
            val.cancel_other_versions()
            val.elaboration_step = steps
            val.review_step = steps
            val.validation_step = steps
            val.date_review = fields.Date.today()
            val.date_validate = fields.Date.today()
            for child in child_fields:
                if hasattr(val, child):
                    lines = getattr(val, child)
                    for current in lines:
                        try:
                            current.state = 'validate_ok'
                        except:
                            pass
                        try:
                            current.elaboration_step = steps
                            current.review_step = steps
                            current.validation_step = steps
                            current.cancel_other_versions()
                        except:
                            pass
