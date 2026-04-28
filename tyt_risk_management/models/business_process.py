from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class BusinessProcessFiles(models.Model):
    _name = "tyt.business.process.file"
    _description = "Control de documentos"

    name = fields.Char(string="Nombre", related="file_id.name", store=True)
    file_id = fields.Many2one(
        comodel_name='documents.document',
        domain=[('type', '=', 'binary')],
    )
    description = fields.Char(string="Descripción")
    business_process_id = fields.Many2one(
        comodel_name='tyt.business.process',
        string="Proceso",
    )

class BusinessProcessLink(models.Model):
    _name = "tyt.business.process.link"
    _description = "Control de documentos"

    name = fields.Char(string="Enlace", store=True)
 
    description = fields.Char(string="Descripción")
    business_process_id = fields.Many2one(
        comodel_name='tyt.business.process',
        string="Proceso",
    )

class BusinessProcessUser(models.Model):
    _name = "tyt.business.process.user"
    _description = "Carga inicial de archivos" #ask

    name = fields.Char(string="Nombre", related="user_id.display_name", store=True)
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Usuario"
    )
    hr_job = fields.Char(
        related='user_id.employee_id.job_id.name',
        string="Puesto en la empresa",
        store=True,
    )
    email = fields.Char(
        related='user_id.email',
    )
 
    business_process_id = fields.Many2one(
        comodel_name='tyt.business.process',
        string="Proceso",
    )


class BusinessProcess(models.Model):
    _name = 'tyt.business.process'
    _description = 'Proceso de Negocio'
    _order = 'name'
    _inherit = ['image.mixin', 'mail.thread']

    name = fields.Char(string='Nombre del Proceso', required=True, copy=False)
    active = fields.Boolean(string='Activo', default=True)
    short_name = fields.Char(string="Nombre corto")
    owner_id = fields.Many2one(
        comodel_name='res.users',
        string="Dueño",
        default= lambda self: self.env.user,
    )
    
    company_id = fields.Many2one('res.company', string='Compañía',  )
    parent_id = fields.Many2one(
        'tyt.business.process', 
        string='Proceso Padre', 
        ondelete='cascade',
        index=True
    )
    child_ids = fields.One2many(
        'tyt.business.process', 
        'parent_id', 
        string='Subprocesos/Actividades'
    )
    control_document_ids = fields.One2many(
        comodel_name='tyt.business.process.file',
        inverse_name='business_process_id',
        string="Control de documentos"
    )
    link_related_ids = fields.One2many(
        comodel_name='tyt.business.process.link',
        inverse_name='business_process_id',
        string="Enlaces relacionados"
    )
    load_initial_user = fields.One2many(
        comodel_name='tyt.business.process.user',
        inverse_name='business_process_id',
        string="Carga inicial de archivos",
    )

    @api.constrains('parent_id')
    def _check_hierarchy_level(self):
        for record in self:
            if record.level > 3:
                raise ValidationError(_('No se permiten más de 3 niveles jerárquicos (Proceso > Subproceso > Actividad).'))
            
            # Evitar recursividad infinita (que un proceso sea padre de sí mismo)
            if record.parent_id == record:
                raise ValidationError(_('Un proceso no puede ser su propio padre.'))

    _sql_constraints = [
        ('name_unique', 'unique(name, parent_id)', '¡El nombre ya existe en este nivel jerárquico!')
    ]
    level = fields.Integer(string="Nivel", compute='_compute_level', store=True)
    

    @api.depends('parent_id', 'parent_id.level')
    def _compute_level(self):
        for record in self:
            if not record.parent_id:
                record.level = 1
            else:
                record.level = record.parent_id.level + 1
                
                
    risk_ids = fields.One2many(
        'tyt.risk.management', 
        'process_id', 
        string='Riesgos Asociados'
    )
    risk_count = fields.Integer(compute='_compute_risk_count', string='Nº Riesgos')
    department_id = fields.Many2one(
        comodel_name='hr.department',
        string="Sitio"
    )

    @api.depends('risk_ids')
    def _compute_risk_count(self):
        for record in self:
            record.risk_count = len(record.risk_ids)
            
            
    def action_view_risks(self):
        self.ensure_one()
        return {
            'name': 'Riesgos del Proceso',
            'type': 'ir.actions.act_window',
            'res_model': 'tyt.risk.management',
            'view_mode': 'list,form',
            'domain': [('process_id', '=', self.id)],
            'context': {'default_process_id': self.id},
            'target': 'current',
        }

    def action_view_subprocess(self):
        self.ensure_one()
        vista_lista_id = self.env.ref('tyt_risk_management.view_business_subprocess_list').id

        return {
            'name': f'Subprocesos de {self.display_name}',
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'list',
            'domain': [('id', 'in', self.child_ids.ids)],
            'context': {'default_parent_id': self.id},
            'target': 'current',
            'views': [(vista_lista_id, 'list'), (False, 'form')], 

        }
                