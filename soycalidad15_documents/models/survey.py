from odoo import models, fields, api
from odoo.osv import expression


class SurveySurvey(models.Model):
    _name = 'survey.survey'
    _inherit = ['survey.survey', 'documents.mixin']

    document_count = fields.Integer(compute='_compute_document_count')


    def _get_document_folder(self):
        return self.company_id.documents_surveys_folder if self.company_id.documents_surveys_settings else False

    def _check_create_documents(self):
        return self.company_id.documents_surveys_settings and super()._check_create_documents()

    def _get_each_cplan_domain(self):
        self.ensure_one()
        user_domain = [('res_model', '=', 'survey.survey'),('res_id', '=', self.id)]
        final_domain = expression.AND([user_domain])
        return final_domain

    def _compute_document_count(self):   
        for record in self:
            domain = record._get_each_cplan_domain()
            record.document_count = self.env['documents.document'].search_count(domain)

    def set_root_model(self):
        root_model = 'survey.survey'
        return root_model

    def action_open_documents(self):
        self.ensure_one()
        get_com_folder = self._get_document_folder()
        root_model = 'survey.survey'
        action = self.env['ir.actions.act_window']._for_xml_id('documents.document_action')
        action['context'] = {
            #'default_partner_id': self.address_home_id.id,
            'searchpanel_default_folder_id':    get_com_folder and get_com_folder.id,
            #'preaction_res_model': self.set_root_model() ,
        }
        action['domain'] = self._get_each_cplan_domain()
        return action