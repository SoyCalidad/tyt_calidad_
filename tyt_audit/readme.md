## tyt_audit 

This module depends of fields and models of odoo studio.

### Odoo studio in files

- In audit_plan_tyt_auditor.py tyt_sites_id field is a many2one with x_sitios .
- In audit_report.py site_id field is a many2one with x_sitios .
- In audit.py tyt_sites_related_id field is a many2one with x_sitios .
- In plan.py sites_id field is a many2one with x_sitios .
- In plan.py available_site_ids field is a many2many with x_sitios .
- In plan.py sites_id field is a many2one with x_sitios .
- In plan.py _compute_available_site_ids method use x_sitios in its logic.
- In start_process_method.py start_process method use x_sitios in its logic.
- 