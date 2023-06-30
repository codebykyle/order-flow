# -*- coding: utf-8 -*-
{
    'name': 'Order Flow',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Orders and shipment tracking for third party companies such as Amazon and Shopee',
    'description': """Orders and shipment tracking for third party companies such as Amazon and Shopee""",
    'depends': [
        'base',
        'documents'
    ],
    'data': [
        'views/order_flow_order_item_views.xml',
        'views/order_flow_item_content_views.xml',
        'views/order_flow_adjustment_views.xml',
        'views/order_flow_item_views.xml',
        'views/order_flow_order_views.xml',
        'views/res_partner_views.xml',
        'security/ir.model.access.csv',
        'views/order_flow_menus.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True
}
