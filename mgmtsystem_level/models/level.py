from odoo import api, fields, models
from odoo.exceptions import Warning


class EditionLevel(models.Model):
    """La nivel de la edición proporciona las características exigidas en la norma de calidad peruana

    Raises:
        Warning: Cuando ya se ha alcanzado el máximo nivel
        Warning: Cuando no se han cumplido los requisitos del nivel 2 pero se intentan llegar a él
        Warning: Cuando no se han cumplido los requisitos del nivel 3 pero se intentan llegar a él
    """
    _name = 'mgmtsystem.level'
    _description = 'Nivel'

    current_level = fields.Selection([
        ('na', 'Sin nivel'),
        ('1', 'Nivel 1'),
        ('2', 'Nivel 2'),
        ('3', 'Nivel 3'),
    ], string='Nivel', default="na", copy=False)
    description = fields.Text(string='Descripción')
    checklist_item_ids = fields.One2many(
        'checklist.item', 'level_id', string='Items', copy=True)

    def verify_checklist(self, level):
        current_level = 'items_level_%s' % level
        for item in getattr(self, current_level):
            if not item.checked:
                raise Warning('No se han completado todos los campos')
        return True

    def write(self, values):
        result = super(EditionLevel, self).write(values)
        if not self.verify_required(self.current_level):
            raise Warning(
                'No ha cumplido con los requerimientos mínimos del nivel')
        return result

    def verify_required(self, current_level):
        """Sobreescribir en cada módulo según los campos obligatorios
        """
        return True

    def proceed_next_level(self):
        for each in self:
            level = each.current_level
            if level == '3':
                each.verify_checklist('3')
                each.verify_checklist('2')
                each.verify_checklist('1')
            if level == '2':
                each.verify_checklist('2')
                each.verify_checklist('1')
            if level == '1':
                each.verify_checklist('1')
            if level == '3':
                raise Warning('Ya alcanzó el máximo nivel')
            elif level == '2':
                each.current_level = '3'
            elif level == '1':
                each.current_level = '2'

    def set_level(self, level):
        for each in self:
            each.current_level = level
