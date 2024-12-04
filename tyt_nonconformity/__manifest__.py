# -*- coding: utf-8 -*-
{
    'name': 'TYT No Conformidad',
    'version': '1.0',
    'summary': 'Gestión de No Conformidades',
    'description': 'Este módulo gestiona las No Conformidades en Odoo.',
    'author': 'Soy Calidad',
    'website': 'www.soycalidad.com',
    'license': '',
    'category': 'soycalidad',
    'depends': [
        'mgmtsystem_nonconformity',
        'mgmtsystem_audit',
        'soycalidad_improve',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/create_nc.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}
