## tyt_instranet_survey 

This module require fields and models of odoo studio

### List of dependencies by file:
- In models/survey_question.py need x_area_encuesta, x_tipo_encuesta models.
- In models/survey_survey.py need the field x_studio_job in res.groups
- In models/survey_user_input.py need the fields: record.partner_id.x_studio_empleado.x_studio_numero , record.partner_id.x_studio_usuario.x_studio_numero
- In views/survey_survey_views.xml need the models: x_area_encuesta, x_tipo_encuesta
- In views/survey_templates.xml need the field: user.x_studio_empleado