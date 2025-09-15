from odoo import models, fields, api 

class Noms(models.Model):
    _name="tyt_studio.noms"
    _description = "noms"
    
    name = fields.Char(string="Descripción", translate=True, required=True)


class TypeSite(models.Model):
    _name = "tyt_studio.type_site"
    _description = "Tipo sitio"
    _order = "sequence asc, id asc"
    
    active = fields.Boolean(default=True, )
    name = fields.Char(string="Descripción", translate=True, required=True)
    sequence = fields.Integer(string="Secuencia")
    

class Sitio(models.Model):
    _name = 'tyt_studio.site'
    _description = 'Sitio'
    _order = "sequence asc, id asc"
    _inherit = ['mail.thread', 'mail.activity.mixin'] 

    active = fields.Boolean(string='Activo', default=True)
    name = fields.Char(string='Nombre', required=True, translate=True)
    codigo = fields.Char(string='Codigo')
    cuan = fields.Many2one('account.analytic.account', string='CUAN', ondelete='set null')
    cuenta_analitica = fields.Many2one('account.analytic.account', string='Cuenta Analitica', ondelete='set null')
    departamento = fields.Many2one('hr.department', string='Departamento', ondelete='set null')
    id0 = fields.Integer(string='id0')
    many2one_field_7AsCR = fields.Many2one('tyt_studio.sites', string='zzzzSitios', ondelete='set null')
    nombre2 = fields.Char(string='Nombre2')
    noms = fields.Many2many('tyt_studio.noms', string='noms')
    sequence = fields.Integer(string='Secuencia')
    sitio1 = fields.Char(string='Sitio1')
    sitios = fields.Many2one('tyt_studio.sites', string='Nombre largo', ondelete='set null')
    sitios0 = fields.Many2one('tyt_studio.sites', string='Sitios', ondelete='set null')
    tipo_sitio = fields.Many2one('tyt_studio.type_site', string='Tipo sitio', ondelete='set null')


        
class Sitios(models.Model):
    _name = 'tyt_studio.sites'
    _description = 'Sitios'
    
    name = fields.Char(string="Nombre del sitio", required=True, translate=True)
    numero = fields.Integer(string="ID Nombre feo", readonly=True, related="site_id.id" )
    site_id = fields.Many2one('tyt_studio.site', ondelete='cascade', string="Sitio")
