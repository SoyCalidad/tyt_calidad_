from odoo import fields, models ,api 


class CatalogFrequency(models.Model):
    _name = "tyt.catalog.frequency"
    _description = "Catalogo frecuencia"

    name = fields.Char(string="Nombre")
    active = fields.Boolean(default=True, )

    