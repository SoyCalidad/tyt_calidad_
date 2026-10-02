# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

MODULE_NAME = 'tyt_risk_management'


# Roles de la categoría "Roles Principales", ordenados de menor a mayor
# privilegio. Ajusta los xmlids si los renombraste.
ROLE_GROUPS = [
    ('usuario', 'group_usuario', 'Usuario'),
    ('consulta', 'group_consulta', 'Consulta'),
    ('admin', 'group_admin', 'Admin'),
]


class ResUsersRiskPermissionWizard(models.TransientModel):
    _name = 'risk_management.user_permission_wizard'
    _description = 'Editar permisos de Gestión de Riesgos de un usuario'

    user_id = fields.Many2one(
        'res.users', string='Usuario', required=True, readonly=True,
    )

    # --- Roles Principales: selection/radio, igual que en res.users -------
    role = fields.Selection(
        selection=lambda self: self._selection_role(),
        string='Rol',
    )

    # --- Permisos Específicos: checkboxes, igual que en res.users --------
    permission_ids = fields.Many2many(
        'res.groups',
        string='Permisos específicos',
        domain=lambda self: [('id', 'in', self._get_allowed_permission_group_ids())],
        help="Los permisos que ya vengan implícitos por el Rol seleccionado "
             "se aplicarán aunque aquí no estén marcados (no se pueden quitar "
             "sin bajar de Rol), igual que en el formulario nativo de Odoo.",
    )
    
    process_ids = fields.Many2many(
        comodel_name='tyt.business.process',
        relation='risk_user_perm_wizard_process_rel',
        column1='wizard_id',
        column2='process_id',
        string='Acceso a Procesos',
    )


    # ------------------------------------------------------------------
    # Helpers de selección/roles
    # ------------------------------------------------------------------
    def _selection_role(self):
        return [] + \
               [(key, label) for key, _xmlid, label in ROLE_GROUPS]

    def _role_group(self, key):
        # 'none' (o cualquier valor no reconocido) -> sin grupo de rol.
        for k, xmlid, _label in ROLE_GROUPS:
            if k == key:
                return self.env.ref(f'{MODULE_NAME}.{xmlid}', raise_if_not_found=False)
        return self.env['res.groups']

    # ------------------------------------------------------------------
    # Listas blancas: siempre recalculadas contra la BD.
    # ------------------------------------------------------------------
    def _get_allowed_role_group_ids(self):
        category = self.env.ref(
            f'{MODULE_NAME}.module_category_roles', raise_if_not_found=False
        )
        if not category:
            return []
        return self.env['res.groups'].search(
            [('category_id', '=', category.id)]
        ).ids

    def _get_allowed_permission_group_ids(self):
        category = self.env.ref(
            f'{MODULE_NAME}.module_category_permisos', raise_if_not_found=False
        )
        if not category:
            return []
        categories = self.env['ir.module.category'].search(
            [('id', 'child_of', category.id)]
        )
        return self.env['res.groups'].search(
            [('category_id', 'in', categories.ids)]
        ).ids

    def _get_all_allowed_group_ids(self):
        return set(self._get_allowed_role_group_ids()) | \
               set(self._get_allowed_permission_group_ids())

    # ------------------------------------------------------------------
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        user_id = res.get('user_id') or self.env.context.get('default_user_id')
        if not user_id:
            return res
        user = self.env['res.users'].browse(user_id)
        user_group_ids = set(user.groups_id.ids)

        # Rol actual = el más alto de los 3 que el usuario ya tenga.
        # Si no tiene ninguno, el default correcto es 'none' (antes esto
        # caía por error en 'usuario' aunque el usuario no tuviera rol).
        chosen_role = False
        for key, xmlid, _label in reversed(ROLE_GROUPS):
            g = self.env.ref(f'{MODULE_NAME}.{xmlid}', raise_if_not_found=False)
            if g and g.id in user_group_ids:
                chosen_role = key
                break
        res['role'] = chosen_role

        perm_ids = set(self._get_allowed_permission_group_ids())
        res['permission_ids'] = [(6, 0, list(user_group_ids & perm_ids))]
        
        visible_process_ids = set(self.env['tyt.business.process'].search([('level', '=', 1)]).ids)
        current_process_ids = set(user.sudo().process_ids.ids)
        res['process_ids'] = [(6, 0, list(current_process_ids & visible_process_ids))]

        return res

    def action_apply(self):
        self.ensure_one()
 

 
        allowed_all = self._get_all_allowed_group_ids()
 
        # Cierre transitivo del rol elegido: el grupo del rol + TODO lo que
        # ese rol implica (otros roles inferiores y permisos específicos
        # que el rol trae consigo), tal como hace el widget nativo.
        role_group = self._role_group(self.role)
        role_closure_ids = set()
        if role_group:
            role_closure_ids = {role_group.id} | set(role_group.trans_implied_ids.ids)
        # Filtro de seguridad: nunca aceptar nada fuera de la lista blanca,
        # aunque trans_implied_ids trajera algo inesperado.
        role_closure_ids &= allowed_all
 
        perm_allowed = set(self._get_allowed_permission_group_ids())
        if self.role == False:
            # Sin rol = sin ningún permiso del módulo, ni siquiera los que
            # estuvieran marcados manualmente como checkbox.
            selected_perm_ids = set()
        else:
            selected_perm_ids = set(self.permission_ids.ids) & perm_allowed
 
        final_module_ids = role_closure_ids | selected_perm_ids
        current_other_ids = set(self.user_id.groups_id.ids) - allowed_all
        final_ids = list(current_other_ids | final_module_ids)
 
        visible_process_ids = set(self.env['tyt.business.process'].search([('level', '=', 1)]).ids)
        hidden_current_ids = set(self.user_id.sudo().process_ids.ids) - visible_process_ids
        if self.role in [ False]:
            selected_process_ids = set()
        else:
            selected_process_ids = set(self.process_ids.ids) & visible_process_ids
        final_process_ids = list(hidden_current_ids | selected_process_ids)
 
        self.user_id.sudo().write({
            'groups_id': [(6, 0, final_ids)],
            'process_ids': [(6, 0, final_process_ids)],
        })

        return {'type': 'ir.actions.act_window_close'}
    
    
    @api.onchange('role')
    def _onchange_role(self):
        # Refleja en la UI, al instante, que "Sin rol" también vacía los
        # permisos específicos (la regla real se aplica igual en el
        # servidor dentro de action_apply, esto es solo para que el
        # usuario vea el checkbox destildado antes de guardar).
        if self.role == False:
            self.permission_ids = [(5, 0, 0)]


    
    