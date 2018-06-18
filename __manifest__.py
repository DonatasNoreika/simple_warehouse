# -*- coding: utf-8 -*-
{
    'name': "Simple Warehouse",
    'version': '1.0',
    'summary': """
        Simple Warehouse""",

    'description': """
        Simple Warehouse Module
    """,

    'author': "Donatas Noreika",
    'website': "https://programosverslui.wordpress.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Warehouse',

    # any module necessary for this one to work correctly
    'depends': ['base'],
    # 'depends': ['base','hr', 'web_tree_image','report', 'web_one2many_kanban'],

    # always loaded
        'data': [
        # 'security/security.xml',
        # 'security/ir.model.__init__.pyaccess.csv',
        # 'report/check_template_report.xml',
        'report/warehouse_tools_report.xml',
        'report/category_tools_report.xml',
        # 'views/mail_templates.xml',
        # 'views/project.xml',
        # 'views/transport.xml',
        'views/storage.xml',
        'views/transfer_workflow.xml',
        # 'views/employee.xml',
        # 'views/templates.xml',
        # 'views/notifications.xml',
    ],
}