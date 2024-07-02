# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    documents_communications_settings = fields.Boolean(related='company_id.documents_communications_settings', readonly=False,
                                                string="Comunicaciones")
    documents_communications_folder = fields.Many2one('documents.folder', related='company_id.documents_communications_folder', readonly=False,
                                     string="communications default workspace")
    #communications_tags = fields.Many2many('documents.tag', 'communications_tags_table',
                                    #related='company_id.communications_tags', readonly=False,
                                    #string="communications Tags")

    @api.onchange('documents_communications_folder')
    def on_documents_communications_folder_change(self):
        #if self.documents_communications_folder != self.communications_tags.mapped('folder_id'):
            #self.communications_tags = False
        pass

    documents_training_settings = fields.Boolean(related='company_id.documents_training_settings', readonly=False,
                                                string="Capacitaciones")
    documents_training_folder = fields.Many2one('documents.folder', related='company_id.documents_training_folder', readonly=False,
                                     string="communications default workspace")

    @api.onchange('documents_training_folder')
    def on_documents_training_folder_change(self):
        pass


    documents_process_settings = fields.Boolean(related='company_id.documents_process_settings', readonly=False,
                                                string="Procesos")
    documents_process_folder = fields.Many2one('documents.folder', related='company_id.documents_process_folder', readonly=False,
                                     string="communications default workspace")

    @api.onchange('documents_process_folder')
    def on_documents_process_folder_change(self):
        pass


    documents_context_settings = fields.Boolean(related='company_id.documents_context_settings', readonly=False,
                                                string="Contexto")
    documents_context_folder = fields.Many2one('documents.folder', related='company_id.documents_context_folder', readonly=False,
                                     string="communications default workspace")

    @api.onchange('documents_context_folder')
    def on_documents_context_folder_change(self):
        pass


    documents_risk_op_settings = fields.Boolean(related='company_id.documents_risk_op_settings', readonly=False,
                                                string="Riesgos y Oportunidades")
    documents_risk_op_folder = fields.Many2one('documents.folder', related='company_id.documents_risk_op_folder', readonly=False,
                                     string="communications default workspace")

    @api.onchange('documents_risk_op_folder')
    def on_documents_risk_op_folder_change(self):
        pass


    documents_legal_requirements_settings = fields.Boolean(related='company_id.documents_legal_requirements_settings', readonly=False,
                                                string="Requisitos legales")
    documents_legal_requirements_folder = fields.Many2one('documents.folder', related='company_id.documents_legal_requirements_folder', readonly=False,
                                     string="communications default workspace")

    @api.onchange('documents_legal_requirements_folder')
    def on_documents_legal_requirements_folder_change(self):
        pass


    documents_requirements_settings = fields.Boolean(related='company_id.documents_requirements_settings', readonly=False,
                                                string="Requisitos")
    documents_requirements_folder = fields.Many2one('documents.folder', related='company_id.documents_requirements_folder', readonly=False,
                                     string="communications default workspace")

    @api.onchange('documents_requirements_folder')
    def on_documents_requirements_folder_change(self):
        pass


    documents_surveys_settings = fields.Boolean(related='company_id.documents_surveys_settings', readonly=False,
                                                string="Encuestas")
    documents_surveys_folder = fields.Many2one('documents.folder', related='company_id.documents_surveys_folder', readonly=False,
                                     string="communications default workspace")

    @api.onchange('documents_surveys_folder')
    def on_documents_surveys_folder_change(self):
        pass


    documents_target_settings = fields.Boolean(related='company_id.documents_target_settings', readonly=False,
                                                string="Objetivos y Medición")
    documents_target_folder = fields.Many2one('documents.folder', related='company_id.documents_target_folder', readonly=False,
                                     string="communications default workspace")

    @api.onchange('documents_target_folder')
    def on_documents_target_folder_change(self):
        pass


    documents_indicators_settings = fields.Boolean(related='company_id.documents_indicators_settings', readonly=False,
                                                string="Indicadores")
    documents_indicators_folder = fields.Many2one('documents.folder', related='company_id.documents_indicators_folder', readonly=False,
                                     string="communications default workspace")

    @api.onchange('documents_indicators_folder')
    def on_documents_indicators_folder_change(self):
        pass


    documents_maintenance_settings = fields.Boolean(related='company_id.documents_maintenance_settings', readonly=False,
                                                string="Mantenimiento y Calibración")
    documents_maintenance_folder = fields.Many2one('documents.folder', related='company_id.documents_maintenance_folder', readonly=False,
                                     string="communications default workspace")

    @api.onchange('documents_maintenance_folder')
    def on_documents_maintenance_folder_change(self):
        pass


    documents_management_review_settings = fields.Boolean(related='company_id.documents_management_review_settings', readonly=False,
                                                string="Revisión por la Dirección")
    documents_management_review_folder = fields.Many2one('documents.folder', related='company_id.documents_management_review_folder', readonly=False,
                                     string="communications default workspace")

    @api.onchange('documents_management_review_folder')
    def on_documents_management_review_folder_change(self):
        pass


    documents_nonconformities_settings = fields.Boolean(related='company_id.documents_nonconformities_settings', readonly=False,
                                                string="No conformidades")
    documents_nonconformities_folder = fields.Many2one('documents.folder', related='company_id.documents_nonconformities_folder', readonly=False,
                                     string="communications default workspace")

    @api.onchange('documents_nonconformities_folder')
    def on_documents_nonconformities_folder_change(self):
        pass


    documents_actions_settings = fields.Boolean(related='company_id.documents_actions_settings', readonly=False,
                                                string="Acciones")
    documents_actions_folder = fields.Many2one('documents.folder', related='company_id.documents_actions_folder', readonly=False,
                                     string="communications default workspace")

    @api.onchange('documents_actions_folder')
    def on_documents_actions_folder_change(self):
        pass


    documents_audits_settings = fields.Boolean(related='company_id.documents_audits_settings', readonly=False,
                                                string="Auditorías")
    documents_audits_folder = fields.Many2one('documents.folder', related='company_id.documents_audits_folder', readonly=False,
                                     string="communications default workspace")

    @api.onchange('documents_audits_folder')
    def on_documents_audits_folder_change(self):
        pass