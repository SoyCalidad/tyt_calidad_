from odoo import models, api, fields
from odoo.exceptions import UserError


class Measurement(models.TransientModel):
    _name = 'mgmtsystem.measurement.wizard'

    name = fields.Char(string='Nombre', required=True)
    date = fields.Datetime(string='Fecha', required=True)
    formula = fields.Char(
        string='Formula', help='Introduzca la formula', required=True)
    success = fields.Boolean(string='Se logró el objetivo', required=True)
    comments = fields.Text(string='Comentarios', required=True)

    def calculate(self):
        result = eval(self.formula)
        goal_id = self.env.context.get('active_id')
        goal = self.env['mgmtsystem.target.goal'].browse(goal_id)

        if self.date > goal.term_date:
            raise UserError('No se puede continuar. Se ha superado el plazo de medición')

        goal_history = self.env['mgmtsystem.target.goal.history']
        goal_history.create({
            'goal_id': goal_id,
            'name': self.name,
            'measurement_date': self.date,
            'success': self.success,
            'comments': self.comments,
            'result': result,
        })
