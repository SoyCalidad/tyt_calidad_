from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

from dateutil.relativedelta import relativedelta
import logging 

_logger = logging.getLogger(__name__)

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
    level = fields.Integer(string="Nivel", compute='_compute_level', store=True, recursive=True)
    

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
            'context': {
                'default_parent_id': self.id,
                'default_owner_id': self.owner_id.id,
                'default_department_id': self.department_id.id,    
            },
            'target': 'current',
            'views': [(vista_lista_id, 'list'), (False, 'form')], 

        }

    @api.model
    def data_status_report(self, department_id=0, domain_id=0, process_id=0, anio=0, month=0 ):
        domain_mitigation = [
            ('mitigation_date', '<=', (fields.Datetime.today() + relativedelta(months=1, day=1)))
        ]
        if department_id and int(department_id):
            domain_mitigation.append(('risk_id_department_id', '=', int(department_id)))
        if domain_id and int(domain_id):
            domain_mitigation.append(('risk_id_pdomain_id', '=', int(domain_id)))
        if process_id and int(process_id):
            domain_mitigation.append(('risk_id_process_id', '=', int(process_id)))
        if anio and int(anio):
            domain_mitigation.append(('year', '=', int(anio)))
        if month and int(month):
            domain_mitigation.append(('month', '=', str(int(month))))

        mitigations = self.env['tyt.risk.mitigation'].read_group(
            domain_mitigation, 
            ['risk_id_process_id'],
            ['risk_id_process_id']
        )
        process_ids = [
            m['risk_id_process_id'][0]
            for m in mitigations
            if m['risk_id_process_id']
        ]
        processes = self.env['tyt.business.process'].browse(process_ids)
        data = []
        for process in processes:
            mitigation_process = self.env['tyt.risk.mitigation'].search(domain_mitigation + [('risk_id_process_id', '=', process.id)])
            data_process = {
                "process_id": process.id,
                "process_short_name": process.short_name,
                "process_name": process.display_name,
                "total": len(mitigation_process),
                "registros_total": mitigation_process.ids,
                "is_not_scope": 0,
                "registros_is_not_scope": [],
                "is_open": len(mitigation_process.filtered(lambda m: m.status == 'unmitigated')),
                "registros_is_open": mitigation_process.filtered(lambda m: m.status == 'unmitigated').ids,
                "is_review": len( mitigation_process.filtered(lambda m: m.status == 'under_review' and m.mr_status_mitigation != 'mitigated')),
                "registros_is_review": mitigation_process.filtered(lambda m: m.status == 'under_review' and m.mr_status_mitigation != 'mitigated').ids,
                "is_remediation": len( mitigation_process.filtered(lambda m: m.status == 'partially_mitigated')),
                "registros_is_remediation":mitigation_process.filtered(lambda m: m.status == 'partially_mitigated').ids,
                "is_audit": len(mitigation_process.filtered(lambda m:  m.mr_status_mitigation == 'mitigated')),
                "registros_is_audit": mitigation_process.filtered(lambda m: m.mr_status_mitigation == 'mitigated').ids,
                "is_completed": len(mitigation_process.filtered(lambda m: m.status == 'complete' or (m.mr_status_mitigation=='mitigated') and not m.risk_id_auditor_id)),
                "registros_is_completed": mitigation_process.filtered(lambda m: m.status == 'complete' or (m.mr_status_mitigation=='mitigated') and not m.risk_id_auditor_id).ids,
                "is_completed_percentage": 0,
                "no_completed": len(mitigation_process.filtered(lambda m: not(m.status == 'complete' or (m.mr_status_mitigation=='mitigated') and not m.risk_id_auditor_id))),
                "subProcesos": []
                   
            }
            if data_process["total"]:
                data_process["is_completed_percentage"] = int((data_process["is_completed"] / data_process["total"]) * 100)

            subprocesses = self.env['tyt.business.process']
            for m in mitigation_process:
                subprocesses |= m.risk_id_subprocess_id
            data_subprocesses = []
            for subprocess in subprocesses:
                mitigation_subprocess = mitigation_process.filtered(lambda m: m.risk_id_subprocess_id.id==subprocess.id)
                data_subprocess = {
                    "sub_process_id": subprocess.id,
                    "process_short_name": process.short_name,
                    "sub_process_name": subprocess.display_name,
                    "total": len(mitigation_subprocess),
                    "registros_total": mitigation_subprocess.ids,
                    "is_not_scope": 0,
                    "registros_is_not_scope": [],
                    "is_open": len(mitigation_subprocess.filtered(lambda m: m.status == 'unmitigated')),
                    "registros_is_open": mitigation_subprocess.filtered(lambda m: m.status == 'unmitigated').ids,
                    "is_review": len(mitigation_subprocess.filtered(lambda m: m.status == 'under_review' and m.mr_status_mitigation != 'mitigated')),
                    "registros_is_review": mitigation_subprocess.filtered(lambda m: m.status == 'under_review' and m.mr_status_mitigation != 'mitigated').ids,
                    "is_remediation": len( mitigation_subprocess.filtered(lambda m: m.status == 'partially_mitigated')),
                    "registros_is_remediation": mitigation_subprocess.filtered(lambda m: m.status == 'partially_mitigated').ids,

                    "is_audit": len(mitigation_subprocess.filtered(lambda m: m.mr_status_mitigation == 'mitigated')),
                    "registros_is_audit": mitigation_subprocess.filtered(lambda m: m.mr_status_mitigation == 'mitigated').ids,
                    "is_completed": len(mitigation_subprocess.filtered(lambda m: m.status == 'complete' or (m.mr_status_mitigation=='mitigated') and not m.risk_id_auditor_id)),
                    "registros_is_completed": mitigation_subprocess.filtered(lambda m: m.status == 'complete' or (m.mr_status_mitigation=='mitigated') and not m.risk_id_auditor_id).ids,
                    "is_completed_percentage": 0,
                }
                if data_subprocess["total"]:
                    data_subprocess["is_completed_percentage"] = int((data_subprocess["is_completed"] / data_subprocess["total"]) * 100)

                data_subprocesses.append(data_subprocess)

            data_process["subProcesos"] = data_subprocesses

            data.append(data_process)
        return data
