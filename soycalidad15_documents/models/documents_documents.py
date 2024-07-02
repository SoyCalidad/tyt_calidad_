from odoo import fields, models

class Document(models.Model):
    #_name = 'soycalidad15.documents.documents'
    _inherit = 'documents.document'

    #COMMUNICATIONS MODEL
    communication_plan_id = fields.Many2one('comunication.plan', string="Communication Plan", tracking=True, store=True )

    communication_plan_line_id = fields.Many2one('comunication.plan.line', string="Communication Plan line", tracking=True, store=True )

    record_meeting_id = fields.Many2one('record.meeting', string="Communication Plan line", tracking=True, store=True )

    # ... Otras definiciones de campos ...

    # Crear la relación Many2one con el modelo de "plan de comunicaciones"
    #communication_plan_id = fields.Many2one(
        #'com_plan_related_document_ids',  # Reemplazar con el nombre real de tu modelo de empleados
        #string='Plan de comunicaciones ID',)
    #para BOTON COUNT
    #campo 'partner_id' y 'owner_id' en modelo 'documents' que sirvan de estructura para tu nuevo campo
    #partner_id = fields.Many2one('res.partner', string="Contact", tracking=True)
    #owner_id = fields.Many2one('res.users', default=lambda self: self.env.user.id, string="Owner", tracking=True)
    
    #TRAINING MODELS
    