# -*- coding: utf-8 -*-
{
    'name': "simple_warehouse",
    'version': '1.00',
    'summary': """
        This is a simple solution for the inventory organization in a several warehouses""",

    'description': """
    
This module is a simple solution for the inventory organization in a several warehouses. Simple warehouse does not interfere with a main Odoo inventory functionality.  
With this module you can:

1. Add tools with a serial numbers, categories, notes and attach the photos and related documents.
2. Add categories for a tools and print all the tools from the selected category.
3. Add warehouses and print all the tools from the selected warehouse.
4. Transfer selected quantity of the tools from one warehouse to another.
5. Reserve selected quantity of the tools in a warehouse.
6. Print list of tools from selected category or warehouse.
          
    """,

    'price': 30.00,
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
