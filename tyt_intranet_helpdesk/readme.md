## tyt_intranet_helpdesk 

This module need of fields and models of odoo studio.

### List of dependencies by file

- The mailbox.py needs the model x_sitios and the fields: x_studio_sitio.x_studio_sitios in res_user.
- The mail_template_data.xml need the field x_name in object.site_id.
- The mailbox.py needs the x_sitios model and res_users.x_studio_numero fields.
- The notification_matrix.py needs the x_sitios model.
- The mailbox_portal_templates.xml needs the record.site_id.x_name, entry.site_id.x_name fields.
- The mailbox_templates.xml needs the rec.x_name field.