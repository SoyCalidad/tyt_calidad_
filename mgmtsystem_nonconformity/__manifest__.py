# Copyright (C) 2010 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Management System - Nonconformity",
    "version": "11.0.1.1.0",
    "license": "AGPL-3",
    "category": "Management System",
    "depends": [
        'mgmtsystem_action',
        'mgmtsystem_audit',
        'hola_calidad',
        'report_xlsx',
        'mgmtsystem_documentary_control',
    ],
    "data": [
        'security/mgmtsystem_nonconformity_security.xml',
        'security/ir.model.access.csv',
        'views/mgmtsystem_nonconformity.xml',
        'views/mgmtsystem_cause.xml',
        'views/mgmtsystem_action.xml',
        'views/nonconformity_onboarding_templates.xml',
        'data/sequence.xml',
        'data/mgmtsystem_nonconformity_cause.xml',
        'data/mail_message_subtype.xml',
        'data/cause.xml',
        'reports/nonconformity.xml',
        'reports/nonconformity_why.xml',
        'reports/nonconformity_output.xml',
        'views/menus.xml',
        'wizards/nonconformity_output.xml',
        'wizards/menus.xml',
    ],
    'installable': True,
}
