# coding: utf-8
{
    'name': 'Odoo Payment Portal',
    'version': '1.0',
    'summary': 'Payment portal for Odoo',
    'description': 'This module provides a payment portal for Odoo.',
    'author': "Luis Cartaya <luiscartaya653@gmail.com>",
    'category': 'Accounting',
    'depends': ['base', 'account', 'portal', 'web', 'auth_oauth'],
    'data': [
        'data/ir_config_parameter.xml',
        'data/automated_sequence.xml',
        'views/templates/web_layout.xml',
        'views/templates/payment_portal_layout.xml',
        'views/templates/login.xml',
        'views/templates/portal_payment.xml',
        'views/templates/portal_payment_selected_company.xml',
        'views/res_users_view.xml',
        'security/ir.model.access.csv',
        'views/payment_reference_view.xml',
        'views/account_journal_view.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'payment_portal/static/src/scss/**/*.scss',
            'payment_portal/static/src/js/**/*.js',
            'payment_portal/static/src/xml/**/*.xml',
            'payment_portal/static/src/js/libs/ag-grid/*.js',
            'payment_portal/static/src/js/libs/ag-grid/*.css',
            'payment_portal/static/src/js/libs/daterangepicker/*.js',
            'payment_portal/static/src/js/libs/daterangepicker/*.css',
        ],
    },
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}