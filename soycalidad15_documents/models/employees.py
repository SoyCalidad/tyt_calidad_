from odoo import models, fields, api
from odoo.osv import expression

class TrainingPlan(models.Model):
    _name = 'mgmtsystem.plan'
    _inherit = ['mgmtsystem.plan', 'documents.mixin']

    document_count = fields.Integer(compute='_compute_document_count')


    def _get_document_folder(self):
        return self.company_id.documents_training_folder if self.company_id.documents_training_settings else False

    def _check_create_documents(self):
        return self.company_id.documents_training_settings and super()._check_create_documents()

    def _get_each_cplan_domain(self):
        self.ensure_one()
        user_domain = [('res_model', '=', 'mgmtsystem.plan'),('res_id', '=', self.id)]
        final_domain = expression.AND([user_domain])
        return final_domain

    def _compute_document_count(self):   
        for record in self:
            domain = record._get_each_cplan_domain()
            record.document_count = self.env['documents.document'].search_count(domain)

    def set_root_model(self):
        root_model = 'mgmtsystem.plan'
        return root_model

    def action_open_documents(self):
        self.ensure_one()
        get_com_folder = self._get_document_folder()
        root_model = 'mgmtsystem.plan'
        action = self.env['ir.actions.act_window']._for_xml_id('documents.document_action')
        action['context'] = {
            #'default_partner_id': self.address_home_id.id,
            'searchpanel_default_folder_id':    get_com_folder and get_com_folder.id,
            #'preaction_res_model': self.set_root_model() ,
        }
        action['domain'] = self._get_each_cplan_domain()
        return action



class TrainingPlanLine(models.Model):
    _name = 'mgmtsystem.plan.training'
    _inherit = ['mgmtsystem.plan.training', 'documents.mixin']

    document_count = fields.Integer(compute='_compute_document_count')


    def _get_document_folder(self):
        return self.company_id.documents_training_folder if self.company_id.documents_training_settings else False

    def _check_create_documents(self):
        return self.company_id.documents_training_settings and super()._check_create_documents()

    def _get_each_cplan_domain(self):
        self.ensure_one()
        user_domain = [('res_model', '=', 'mgmtsystem.plan.training'),('res_id', '=', self.id)]
        final_domain = expression.AND([user_domain])
        return final_domain

    def _compute_document_count(self):   
        for record in self:
            domain = record._get_each_cplan_domain()
            record.document_count = self.env['documents.document'].search_count(domain)


    def set_root_model(self):
        root_model = 'mgmtsystem.plan.training'
        return root_model

    def action_open_documents(self):
        self.ensure_one()
        get_com_folder = self._get_document_folder()
        root_model = 'mgmtsystem.plan.training'
        action = self.env['ir.actions.act_window']._for_xml_id('documents.document_action')
        action['context'] = {
            #'default_partner_id': self.address_home_id.id,
            'searchpanel_default_folder_id':    get_com_folder and get_com_folder.id,
            #'preaction_res_model': self.set_root_model() ,
        }
        action['domain'] = self._get_each_cplan_domain()
        return action


class MgmtsystemContextOrganizationChart(models.Model):
    _name = 'mgmtsystem.context.organization_chart'
    _inherit = ['mgmtsystem.context.organization_chart', 'documents.mixin']

    document_count = fields.Integer(compute='_compute_document_count')


    def _get_document_folder(self):
        return self.company_id.documents_training_folder if self.company_id.documents_training_settings else False

    def _check_create_documents(self):
        return self.company_id.documents_training_settings and super()._check_create_documents()

    def _get_each_cplan_domain(self):
        self.ensure_one()
        user_domain = [('res_model', '=', 'mgmtsystem.context.organization_chart'),('res_id', '=', self.id)]
        final_domain = expression.AND([user_domain])
        return final_domain

    def _compute_document_count(self):   
        for record in self:
            domain = record._get_each_cplan_domain()
            record.document_count = self.env['documents.document'].search_count(domain)


    def set_root_model(self):
        root_model = 'mgmtsystem.context.organization_chart'
        return root_model

    def action_open_documents(self):
        self.ensure_one()
        get_com_folder = self._get_document_folder()
        root_model = 'mgmtsystem.context.organization_chart'
        action = self.env['ir.actions.act_window']._for_xml_id('documents.document_action')
        action['context'] = {
            #'default_partner_id': self.address_home_id.id,
            'searchpanel_default_folder_id':    get_com_folder and get_com_folder.id,
            #'preaction_res_model': self.set_root_model() ,
        }
        action['domain'] = self._get_each_cplan_domain()
        return action