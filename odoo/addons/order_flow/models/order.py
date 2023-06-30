from odoo import models, fields, _


class OrderFlowOrder(models.Model):
    _name = 'order_flow.order'
    _description = 'Order'
    _order = 'delivery_date, id'

    _inherit = [
        'documents.mixin'
    ]

    name = fields.Char(required=True)

    vendor_id = fields.Many2one(
        'res.partner',
        string='Vendor',
        index=True
    )

    currency_id = fields.Many2one(
        'res.currency',
        'Currency',
        default=lambda self: self.env.company.currency_id.id,
        required=True
    )

    invoice = fields.Binary(string="Invoice", attachment=True)

    order_date = fields.Datetime(string="Order Date")
    delivery_date = fields.Datetime(string="Delivery Date")

    amount_subtotal = fields.Float(string='Sub-Total')
    amount_shipping = fields.Float(string='Shipping')
    amount_vat = fields.Float(string='VAT')
    amount_tax = fields.Float(string='Tax')
    amount_discount = fields.Float(string='Discount')
    amount_final_total = fields.Float(string='Total')

    integration_code = fields.Char(string="Integration Code")
    barcode = fields.Char(help="Use a barcode to identify this order")

    order_items = fields.One2many(
        comodel_name='order_flow.order_item',
        inverse_name='order_id',
        string='Items'
    )