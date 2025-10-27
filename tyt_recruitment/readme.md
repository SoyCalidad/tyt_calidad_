## tyt_recruitment 

This module need of fields and models of odoo studio.

### List of dependencies by file

- The models/descriptive_letter.py needs the x_sitios model.
- The models/requisition.py needs the x_sitio, x_periodo models, x_studio_sitio field in res_users.
- The models/wizard_attendance.py needs self.requisition_id.periodo_id.x_name field.