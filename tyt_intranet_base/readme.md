## tyt_intranet_base 

This module require fields and models of odoo studio.

### List of studio dependences

- In the hr_employee.py , the field intranet_user_ids need x_studio_empleado fields of hr_employee
- In the intranet_groups.py, the field sitio_id has a many2one with department_id.x_studio_sitio .

- In the view intranet_groups_views.xml, the view of employee need the fields: x_studio_numero, x_studio_sitio.
