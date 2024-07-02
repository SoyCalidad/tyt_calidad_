from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class MeasurementPeriod(models.Model):
    _name = "mgmtsystem.frequency"
    _description = "Periodo de tiempo"

    name = fields.Char(string='Nombre',
                       translate=True, required=True)
    active = fields.Boolean(string="Activo", default=True)
    note = fields.Text(string='Descripción', translate=True)
    company_id = fields.Many2one('res.company', string='Compañia',
                                 required=True, default=lambda self: self.env.user.company_id)
    years = fields.Integer(string='Número de Años', required=True, default=0)
    months = fields.Integer(string='Número de Meses', required=True, default=0)
    weeks = fields.Integer(string='Número de Semanas',
                           required=True, default=0)
    days = fields.Integer(string='Número de Días', required=True, default=0)
    type = fields.Selection([
        ('term', 'Periodo'),
        ('freq', 'Frecuencia'),
    ], string='Tipo')

    def get(self):
        "Return the relativedelta"
        return relativedelta(
            years=self.years,
            days=self.days,
            weeks=self.weeks,
            months=self.months,
        )

    def compute(self, value, date_ref=False):
        date_ref = date_ref or fields.Date.today()
