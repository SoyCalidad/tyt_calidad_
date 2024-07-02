from odoo import api, fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    def get_and_update_onbarding_state(self, onboarding_state, steps_states):
            """ Needed to display onboarding animations only one time. """
            old_values = {}
            all_done = True
            for step_state in steps_states:
                old_values[step_state] = self[step_state]
                if self[step_state] == 'just_done':
                    self[step_state] = 'done'
                all_done = all_done and self[step_state] == 'done'

            if all_done:
                if self[onboarding_state] == 'not_done':
                    # string `onboarding_state` instead of variable name is not an error
                    old_values['onboarding_state'] = 'not_done'
                else:
                    old_values['onboarding_state'] = 'not_done'
                self[onboarding_state] = 'not_done'
            return old_values