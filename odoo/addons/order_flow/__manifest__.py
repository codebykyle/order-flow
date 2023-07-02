# -*- coding: utf-8 -*-
{
    'name': 'Order Flow',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Orders and shipment tracking for third party companies such as Amazon and Shopee',
    'description': """Orders and shipment tracking for third party companies such as Amazon and Shopee""",
    'depends': [
        'base',
        'web'
    ],
    'data': [
        'data/label_type.xml',
        'wizard/create_label_request_views.xml',
        'wizard/print_label_views.xml',
        'views/order_flow_label_request_views.xml',
        'views/order_flow_shipping_method_views.xml',
        'views/order_flow_shipping_label_type_views.xml',
        'views/order_flow_order_item_views.xml',
        'views/order_flow_item_content_views.xml',
        'views/order_flow_adjustment_views.xml',
        'views/order_flow_item_views.xml',
        'views/order_flow_order_views.xml',
        'views/res_partner_views.xml',
        'security/ir.model.access.csv',
        'views/order_flow_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'order_flow/static/src/**/*',
        ]
    },
    'installable': True,
    'auto_install': False,
    'application': True
}
