# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _


class ResCompany(models.Model):
    _inherit = "res.company"

    def _domain_company(self):
        company = self.env.company
        return ['|', ('company_id', '=', False), ('company_id', '=', company.id)]
    
    documents_communications_settings = fields.Boolean() #NUEVO CAMBIAR "project" por modulo "COMUNICACION"
    documents_communications_folder = fields.Many2one('documents.folder', string="Communications Workspace", domain=_domain_company,
                                     default=lambda self: self.env.ref('documents.documents_communications_folder',
                                                                       raise_if_not_found=False))
    #communications_tags = fields.Many2many('documents.tag', 'project_tags_table')

    documents_training_settings = fields.Boolean()
    documents_training_folder = fields.Many2one('documents.folder', string="Communications Workspace", domain=_domain_company,
                                     default=lambda self: self.env.ref('documents.documents_training_folder',
                                                                       raise_if_not_found=False))

    documents_process_settings = fields.Boolean()
    documents_process_folder = fields.Many2one('documents.folder', string="Communications Workspace", domain=_domain_company,
                                     default=lambda self: self.env.ref('documents.documents_process_folder',
                                                                       raise_if_not_found=False))

    documents_context_settings = fields.Boolean()
    documents_context_folder = fields.Many2one('documents.folder', string="Communications Workspace", domain=_domain_company,
                                     default=lambda self: self.env.ref('documents.documents_context_folder',
                                                                       raise_if_not_found=False))

    documents_risk_op_settings = fields.Boolean()
    documents_risk_op_folder = fields.Many2one('documents.folder', string="Communications Workspace", domain=_domain_company,
                                     default=lambda self: self.env.ref('documents.documents_risk_op_folder',
                                                                       raise_if_not_found=False))

    documents_legal_requirements_settings = fields.Boolean()
    documents_legal_requirements_folder = fields.Many2one('documents.folder', string="Communications Workspace", domain=_domain_company,
                                     default=lambda self: self.env.ref('documents.documents_legal_requirements_folder',
                                                                       raise_if_not_found=False))

    documents_requirements_settings = fields.Boolean()
    documents_requirements_folder = fields.Many2one('documents.folder', string="Communications Workspace", domain=_domain_company,
                                     default=lambda self: self.env.ref('documents.documents_requirements_folder',
                                                                       raise_if_not_found=False))

    documents_surveys_settings = fields.Boolean()
    documents_surveys_folder = fields.Many2one('documents.folder', string="Communications Workspace", domain=_domain_company,
                                     default=lambda self: self.env.ref('documents.documents_surveys_folder',
                                                                       raise_if_not_found=False))

    documents_target_settings = fields.Boolean()
    documents_target_folder = fields.Many2one('documents.folder', string="Communications Workspace", domain=_domain_company,
                                     default=lambda self: self.env.ref('documents.documents_target_folder',
                                                                       raise_if_not_found=False))
    
    documents_indicators_settings = fields.Boolean()
    documents_indicators_folder = fields.Many2one('documents.folder', string="Communications Workspace", domain=_domain_company,
                                     default=lambda self: self.env.ref('documents.documents_indicators_folder',
                                                                       raise_if_not_found=False))

    documents_maintenance_settings = fields.Boolean()
    documents_maintenance_folder = fields.Many2one('documents.folder', string="Communications Workspace", domain=_domain_company,
                                     default=lambda self: self.env.ref('documents.documents_maintenance_folder',
                                                                       raise_if_not_found=False))

    documents_management_review_settings = fields.Boolean()
    documents_management_review_folder = fields.Many2one('documents.folder', string="Communications Workspace", domain=_domain_company,
                                     default=lambda self: self.env.ref('documents.documents_management_review_folder',
                                                                       raise_if_not_found=False))
    
    documents_nonconformities_settings = fields.Boolean()
    documents_nonconformities_folder = fields.Many2one('documents.folder', string="Communications Workspace", domain=_domain_company,
                                     default=lambda self: self.env.ref('documents.documents_nonconformities_folder',
                                                                       raise_if_not_found=False))
    
    documents_actions_settings = fields.Boolean()
    documents_actions_folder = fields.Many2one('documents.folder', string="Communications Workspace", domain=_domain_company,
                                     default=lambda self: self.env.ref('documents.documents_actions_folder',
                                                                       raise_if_not_found=False))
    
    documents_audits_settings = fields.Boolean()
    documents_audits_folder = fields.Many2one('documents.folder', string="Communications Workspace", domain=_domain_company,
                                     default=lambda self: self.env.ref('documents.documents_audits_folder',
                                                                       raise_if_not_found=False))