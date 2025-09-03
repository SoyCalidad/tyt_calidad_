from odoo import models, fields 


class Ano(models.Model):
    _name = "tyt_studio.ano"
    _description = "año"
    
    name = fields.Char(string="Descripción")
    
    
class PeriodType(models.Model):
    _name = "tyt_studio.period_type"
    _description = "Tipo periodo"
    
    name = fields.Char(string="Descripción	Carácter")		
    code = fields.Char(string="code")
    

class Period(models.Model):
    _name = "tyt_studio.period"
    _description = "periodo"
    
    name = fields.Char(string="Descripción	Carácter")		
	
	
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
	
	
# x_studio_gg	gg	booleano	

	
# x_studio_gnnnn	GNNNN	many2one	
	
	
# x_studio_mes	mes	many2one	
	
	
# x_studio_mes0	mes0	many2one	
	
	
# 	Campo personalizado	
# x_studio_mes00	Mes00	many2one	
	
	
# 	Campo personalizado	
# x_studio_mesac	mesac	entero	
	
	
# 	Campo personalizado	
# x_studio_mesc	mesc	entero	
	
	
# 	Campo personalizado	
# x_studio_mesm00	mesm00	many2one	
	
	
# 	Campo personalizado	
# x_studio_semana	Semana	many2one	
	
	
# 	Campo personalizado	
# x_studio_semanac	semanac	entero	
	
	
# 	Campo personalizado	
    tipo_periodo = fields.Many2one('tyt_studio.period_type', string="Tipo periodo")	

# x_studio_tpid	tpid	entero	
	