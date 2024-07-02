from odoo import models, fields, api
from odoo.osv import expression


class ComunicationPlan(models.Model):
    _name = 'comunication.plan'
    _inherit = ['comunication.plan', 'documents.mixin']


    document_count = fields.Integer(compute='_compute_document_count')

    # al ser un mixin, nos permite añadir metadatos a nuestros archivos adjuntos
    def _get_document_vals(self, attachment):
        """
        Return values used to create a `documents.document`
        """
        self.ensure_one()
        document_vals = {}
        if self._check_create_documents():
            document_vals = {
                'attachment_id': attachment.id,
                'name': attachment.name or self.display_name,
                'folder_id': self._get_document_folder().id,
                'owner_id': self._get_document_owner().id,
                'partner_id': self._get_document_partner().id,
                'tag_ids': [(6, 0, self._get_document_tags().ids)],

            }
        return document_vals


    # Crear la relación One2many con los documentos asociados al plan_de_comunicaciones_id
    #com_plan_related_document_ids = fields.One2many(
        #'documents.document',  # Reemplazar con el nombre de tu modelo de documentos
        #'communication_plan_id',  # Campo Many2one en el modelo de documentos que apunta a este modelo
        #string='Employee Documents'
    #)


    #def unlink(self):
        # unlink documents.document directly so mail.activity.mixin().unlink is called
        #self.env['documents.document'].sudo().search([('attachment_id', 'in', self.attachment_ids.ids)]).unlink()
        #return super(ComunicationPlan, self).unlink()
    
    def _get_document_folder(self):
        return self.company_id.documents_communications_folder if self.company_id.documents_communications_settings else False

    # para añadir esta función es necesario que el modelo_de_calidad tenga el campo user_id
    #def _get_document_owner(self):
        #return self.user_id

    def _check_create_documents(self):
        return self.company_id.documents_communications_settings and super()._check_create_documents()

    #DEFINIENDO ACCIONES DE BOTON (CONTAR DOCUMENTOS y ABRIR DOCUMENTOS)
        #falta definir el DOMINIO  "def _get_employee_document_domain"

    def _get_each_cplan_domain(self):
        self.ensure_one()
        user_domain = [('res_model', '=', 'comunication.plan'),
                        ('res_id', '=', self.id)]
        final_domain = expression.AND([user_domain])
        return final_domain
    
        #debemos mejorar a que apunte a 'docs_comunicationplan.id'='comunication.plan.id'
        #[('docs_comunicationplan.id', '=', self.id)] , [('newfield_in_docs','=',self.id )] 
        # DOMINIO MODELO [('documents_model_field', '=', 'comunication_plan_model_field')]
        
        
    def _compute_document_count(self):
        # Method not optimized for batches since it is only used in the form view.
        # self = "comunication.plan" or "documents.mixin" (modelo dónde se llama la función)        
        for record in self:
            domain = record._get_each_cplan_domain()
            record.document_count = self.env['documents.document'].search_count(domain)


    def set_root_model(self):
        root_model = 'comunication.plan'
        return root_model


    #@api.model # llamar a la acción sin necesidad de ser activada por la vista
    def action_open_documents(self):
        self.ensure_one()
        get_com_folder = self._get_document_folder()
        root_model = 'comunication.plan'
        action = self.env['ir.actions.act_window']._for_xml_id('documents.document_action')
        # Documents created within that action will be 'assigned' to the employee
        # Also makes sure that the views starts on the  get_com_folder
        
        action['context'] = {
            #'default_partner_id': self.address_home_id.id,
            'searchpanel_default_folder_id':    get_com_folder and get_com_folder.id,
            #'preaction_res_model': self.set_root_model() ,
        }
        action['domain'] = self._get_each_cplan_domain()
        return action
    

class ComunicationComunication(models.Model):
    _name = 'comunication.plan.line'
    _inherit = ['comunication.plan.line', 'documents.mixin']


    document_count = fields.Integer(compute='_compute_document_count')


    def _get_document_folder(self):
        return self.company_id.documents_communications_folder if self.company_id.documents_communications_settings else False

    def _check_create_documents(self):
        return self.company_id.documents_communications_settings and super()._check_create_documents()

    def _get_each_cplan_domain(self):
        self.ensure_one()
        user_domain = [('res_model', '=', 'comunication.plan.line'),('res_id', '=', self.id)]
        final_domain = expression.AND([user_domain])
        return final_domain

    def _compute_document_count(self):   
        for record in self:
            domain = record._get_each_cplan_domain()
            record.document_count = self.env['documents.document'].search_count(domain)


    def set_root_model(self):
        root_model = 'comunication.plan.line'
        return root_model

    def action_open_documents(self):
        self.ensure_one()
        get_com_folder = self._get_document_folder()
        root_model = 'comunication.plan.line'
        action = self.env['ir.actions.act_window']._for_xml_id('documents.document_action')
        action['context'] = {
            #'default_partner_id': self.address_home_id.id,
            'searchpanel_default_folder_id':    get_com_folder and get_com_folder.id,
            #'preaction_res_model': self.set_root_model() ,
        }
        action['domain'] = self._get_each_cplan_domain()
        return action
    

class RecordMeeting(models.Model):
    _name = 'record.meeting'
    _inherit = ['record.meeting', 'documents.mixin']

    document_count = fields.Integer(compute='_compute_document_count')
    
    #"company_id" did not exist and is necessary to activate the function "action_open_documents()"
    company_id = fields.Many2one('res.company', string='Compañia', default=lambda self: self.env.user.company_id)
    

    def _get_document_folder(self):
        return self.company_id.documents_communications_folder if self.company_id.documents_communications_settings else False

    def _check_create_documents(self):
        return self.company_id.documents_communications_settings and super()._check_create_documents()

    def _get_each_cplan_domain(self):
        self.ensure_one()
        user_domain = [('res_model', '=', 'record.meeting'),('res_id', '=', self.id)]
        final_domain = expression.AND([user_domain])
        return final_domain

    def _compute_document_count(self):   
        for record in self:
            domain = record._get_each_cplan_domain()
            record.document_count = self.env['documents.document'].search_count(domain)


    def set_root_model(self):
        root_model = 'record.meeting'
        return root_model

    def action_open_documents(self):
        self.ensure_one()
        get_com_folder = self._get_document_folder()
        root_model = 'record.meeting'
        action = self.env['ir.actions.act_window']._for_xml_id('documents.document_action')
        action['context'] = {
            #'default_partner_id': self.address_home_id.id,
            'searchpanel_default_folder_id':    get_com_folder and get_com_folder.id,
            #'preaction_res_model': self.set_root_model() ,
        }
        action['domain'] = self._get_each_cplan_domain()
        return action