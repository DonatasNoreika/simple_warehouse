# -*- coding: utf-8 -*-
{
    'name': "simple_warehouse",
    'version': '1.00',
    'summary': """
        Simple Warehouse""",

    'description': """
    
This module is simple solution for Inventory organization in several Warehouses. Simple Warehouse does not interfere with main Odoo Inventory functionality.  
With simple_warehouse you can:

1. Add Tools with Serial Numbers, Category, Notes and attach Photos and related Documents.
2. Add Categories for Tools and print all Tools in selected Category.
3. Add Warehouses and print all Tools in selected Warehouse.
4. Transfer selected Quantity of Tools from one Warehouse to another.
5. Reserve selected Quantity of Tools in Warehouse.
          
    """,

    'price': 150.00,
    'currency': 'EUR',
    'license': 'OPL-1',

    'support': 'programosjusuverslui@gmail.com',
    'author': "Žilvinas Vitkevičius, Donatas Noreika",
    'website': "http://programosverslui.wordpress.com",
    'images': ['static/images/main_screenshot.png'],

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Inventory',

    # any module necessary for this one to work correctly
    'depends': ['base','report'],

    # always loaded
        'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'report/warehouse_tools_report.xml',
        'report/category_tools_report.xml',
        'views/storage.xml',
        'views/transfer_workflow.xml',
    ],
}
