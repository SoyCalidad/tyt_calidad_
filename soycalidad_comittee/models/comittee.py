from odoo import api, fields, models


class SoyCalidadComitteePosition(models.Model):
    _name = 'soycalidad.comittee.position'
    _description = 'Posición en el comité de calidad'

    name = fields.Char(string='Nombre')
    description = fields.Text(string='Descripción')


class SoyCalidadComitteeFunction(models.Model):
    _name = 'soycalidad.comittee.function'
    _description = 'Función en el comité de calidad'

    name = fields.Char(string='Nombre')
    description = fields.Text(string='Descripción')
    member_id = fields.Many2one(
        comodel_name='soycalidad.comittee.member', string='Comité')


class SoyCalidadComitteeMember(models.Model):
    _name = 'soycalidad.comittee.member'
    _description = 'Miembro del comité de calidad'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one(
        comodel_name='hr.employee', string='Empleado')

    name = fields.Char(string='Nombres')
    job_id = fields.Many2one(comodel_name='hr.job',
                             string='Puesto', related='employee_id.job_id')
    position_id = fields.Many2one(
        comodel_name='soycalidad.comittee.position', string='Posición en el comité')
    function_ids = fields.One2many(
        comodel_name='soycalidad.comittee.function', inverse_name='member_id', string='Funciones')
    comittee_id = fields.Many2one(
        comodel_name='soycalidad.comittee', string='Comité')


class SoyCalidadComittee(models.Model):
    _name = 'soycalidad.comittee'
    _description = 'Comité de calidad'

    name = fields.Char(string='Nombre')
    member_ids = fields.One2many(comodel_name='soycalidad.comittee.member',
                                 inverse_name='comittee_id', string='Miembros del comité')
