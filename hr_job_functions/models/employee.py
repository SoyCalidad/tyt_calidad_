from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime

class Workplace(models.Model):
    _name = 'hr.workplace'
    
    name = fields.Char(string='Nombre')


class Applicant(models.Model):
    _inherit = 'hr.applicant'
    
    workplace = fields.Many2one('hr.workplace', string='Lugar de trabajo')
    approval_date = fields.Date(string='Fecha de contratación')
    
    @api.model
    def send_mail_for_interview(self, force_send=True):
        template = self.env.ref(
            'hr_recruitment.email_template_data_applicant_interest')
        template.send_mail(self.id, force_send=force_send)
        return True
    
    @api.model
    def send_mail_for_rejection(self, force_send=True):
        template = self.env.ref(
            'hr_recruitment.email_template_data_applicant_refuse')
        template.send_mail(self.id, force_send=force_send)
        return True
    
    @api.model
    def send_mail_for_accomplished(self, force_send=True):
        template = self.env.ref(
            'hr_recruitment.email_template_data_applicant_employee')
        template.send_mail(self.id, force_send=force_send)
        return True

    
    def create_employee_from_applicant(self):
        """ Create an hr.employee from the hr.applicants """
        self.approval_date = datetime.today()
        employee = False
        for applicant in self:
            contact_name = False
            if applicant.partner_id:
                address_id = applicant.partner_id.address_get(['contact'])['contact']
                contact_name = applicant.partner_id.name_get()[0][1]
            else :
                new_partner_id = self.env['res.partner'].create({
                    'is_company': False,
                    'name': applicant.partner_name,
                    'email': applicant.email_from,
                    'phone': applicant.partner_phone,
                    'mobile': applicant.partner_mobile
                })
                address_id = new_partner_id.address_get(['contact'])['contact']
            if applicant.job_id and (applicant.partner_name or contact_name):
                applicant.job_id.write({'no_of_hired_employee': applicant.job_id.no_of_hired_employee + 1})
                employee = self.env['hr.employee'].create({
                    'name': applicant.partner_name or contact_name,
                    'job_id': applicant.job_id.id,
                    'address_home_id': address_id,
                    'workplace': applicant.workplace.id,
                    'department_id': applicant.department_id.id or False,
                    'address_id': applicant.company_id and applicant.company_id.partner_id
                            and applicant.company_id.partner_id.id or False,
                    'work_email': applicant.department_id and applicant.department_id.company_id
                            and applicant.department_id.company_id.email or False,
                    'work_phone': applicant.department_id and applicant.department_id.company_id
                            and applicant.department_id.company_id.phone or False,})
                applicant.write({'emp_id': employee.id})
                applicant.job_id.message_post(
                    body=_('New Employee %s Hired') % applicant.partner_name if applicant.partner_name else applicant.name,
                    subtype="hr_recruitment.mt_job_applicant_hired")
                attach_ids = [x.copy() for x in self.attachment_ids]
                
                for each in attach_ids:
                    each.res_model = employee._name
                    each.res_id = employee.id
                # ids = [x.id for x in attach_ids]
                # employee.attachment_ids = [(6, 0, ids)]
                # employee._broadcast_welcome()
            else:
                raise UserError(_('You must define an Applied Job and a Contact Name for this applicant.'))

        employee_action = self.env.ref('hr.open_view_employee_list')
        dict_act_window = employee_action.read([])[0]
        if employee:
            dict_act_window['res_id'] = employee.id
        dict_act_window['view_mode'] = 'form,tree'
        return dict_act_window

class Employee(models.Model):
    _inherit = 'hr.employee'

    code = fields.Char(string='Código')
    workplace = fields.Many2one('hr.workplace', string='Lugar de trabajo')
    attachment_ids = fields.One2many('ir.attachment', 'res_id', domain=[
                                     ('res_model', '=', 'hr.employee')], string='Adjuntos')
    attachment_number = fields.Integer(
        compute='_get_attachment_number', string="Number of Attachments")

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code(
            'employee.sequence')
        return super().create(vals)

    def _get_attachment_number(self):
        """
        read_group_res = self.env['ir.attachment'].read_group(
            [('res_model', '=', 'hr.employee'), ('res_id', 'in', self.ids)],
            ['res_id'], ['res_id'])
        attach_data = dict((res['res_id'], res['res_id_count'])
                           for res in read_group_res)
        """
        for record in self:
            record.attachment_number = len(record.attachment_ids)

    def action_get_attachment_tree_view(self):
        attachment_action = self.env.ref('base.action_attachment')
        action = attachment_action.read()[0]
        action['context'] = {'default_res_model': self._name, 'default_res_id': self.ids[0]}
        action['domain'] = str(['&', ('res_model', '=', self._name), ('res_id', 'in', self.ids)])
        action['search_view_id'] = (self.env.ref('hr_job_functions.ir_attachment_view_search_inherit_hr_employee').id, )
        return action
