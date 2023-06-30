import time

from odoo import models, fields, api


class OrderFlowOrderItemAdjustment(models.Model):
    _name = 'order_flow.item_adjustment'
    _description = 'Item Adjustment'

    name = fields.Char(
        string='Name',
        required=True
    )

    adjustment_type = fields.Selection([
        ('sold', 'Sold'),
        ('thrown_away', 'Thrown Away'),
        ('given_away', 'Given Away'),
    ],
        string='Adjustment Type',
        default='sold',
        required=True
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Given/Sold To',
        index=True
    )

    item_id = fields.Many2one(
        'order_flow.item',
        string='Item'
    )

    currency_id = fields.Many2one(
        'res.currency',
        'Currency',
        default=lambda self: self.env.company.currency_id.id,
        required=True
    )

    adjustment_date = fields.Datetime(
        string="Order Date",
        default=lambda *a: time.strftime('%Y-%m-%d %H:%M:%S')
    )

    quantity = fields.Float(string='Quantity', default=1)

    amount_subtotal = fields.Float(string='Sub-Total', default=0)
    amount_shipping = fields.Float(string='Shipping', default=0)
    amount_vat = fields.Float(string='VAT', default=0)
    amount_tax = fields.Float(string='Tax', default=0)
    amount_discount = fields.Float(string='Discount', default=0)
    amount_final_total = fields.Float(string='Total', default=0)

    integration_code = fields.Char(string="Integration Code")

