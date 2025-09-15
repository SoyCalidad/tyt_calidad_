from odoo import models, fields, api


class Ano(models.Model):
    _name = "tyt_studio.ano"
    _description = "año"
    
    name = fields.Char(string="Descripción", translate=True, required=True)
    
    
class PeriodType(models.Model):
    _name = "tyt_studio.period_type"
    _description = "Tipo periodo"
    
    name = fields.Char(string="Descripción", translate=True, required=True)		
    code = fields.Char(string="code")
    
    
class GNNNN(models.Model):
    _name = "tyt_studio.gnnnn"
    _description = "GNNNN"
    
    name = fields.Char(string="Descripción", required=True, translate=True)
    
    
class Mes(models.Model):
    _name = "tyt_studio.mes"
    _description = "Mes"
    
    name = fields.Char(string="Descripción", required=True, translate=True)
    numero = fields.Integer(string="Numero")
    

class Period(models.Model):
    _name = "tyt_studio.period"
    _description = "periodo"
    
    name = fields.Char(string="Descripción", required=True, translate=True)
    amc	= fields.Integer(string="amc")	
    ano = fields.Many2one('tyt_studio.ano', string="ano", ondelete="set null")
    anoc = fields.Integer(string="anoc")
    asc = fields.Integer(string="asc")
    diaac = fields.Integer(string="diaac")	
    diac = fields.Integer(string="diac")
    diamc = fields.Integer(string="diamc")
    diasc = fields.Integer(string="diasc")	
    f1 = fields.Date(string="f1")	
    f2 = fields.Date(string="f2")
    g = fields.Boolean(string="g")	
    gg = fields.Boolean(string="gg", readonly=True)	
    gnnnn = fields.Many2one(comodel_name="tyt_studio.gnnnn", string="GNNNN", readonly=True, ondelete="set null")
    mes	= fields.Many2one(comodel_name="tyt_studio.period", string="mes", ondelete="set null")
    mes0 = fields.Many2one(comodel_name="tyt_studio.period", string="mes0", ondelete="set null")
    mes00 = fields.Many2one(comodel_name="tyt_studio.mes", string="Mes00", ondelete="set null")
    mesac = fields.Integer(string="mesac")	
    mesc = fields.Integer(string="mesc")
    mesm00	= fields.Many2one(comodel_name="tyt_studio.mes", string="mesm00", ondelete="set null")
    semana = fields.Many2one(comodel_name="tyt_studio.period", string="Semana", ondelete="set null")
    semanac = fields.Integer(string="semanac")
    tipo_periodo = fields.Many2one('tyt_studio.period_type', string="Tipo periodo", ondelete="set null")
    tpid = fields.Integer(string="tpid")	

    @api.onchange("g")
    def _onchange_g(self):
        for record in self:
            a=record.anoc
            s=record.semanac
            anosemc=a*100+s
            record['asc']=anosemc
            
    @api.onchange("semanac")
    def _on_change_semanac(self):
        for record in self:
            anio = str(record.anoc)[-2:]
            semact = record.semanac
            if semact > 1:
                semant = str(semact - 1).zfill(2)
                semact_str = str(semact).zfill(2)
                grupo = f'G{semant}{semact_str}{anio}'
                grupo_id = self.env['tyt_studio.gnnnn'].search([('name', '=', grupo)], limit=1)
                if not grupo_id:
                    grupo_id = self.env['tyt_studio.gnnnn'].create({'name': grupo})
                record['gnnnn'] = grupo_id.id
                
    
	