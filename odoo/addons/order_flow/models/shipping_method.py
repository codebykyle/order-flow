from odoo import models, fields, _


class OrderFlowShippingMethod(models.Model):
    _name = 'order_flow.shipping_method'
    _description = 'Planned Shipping Method'
    _order = 'id'

    name = fields.Char('Shipping Method Name', required=True)

    item_ids = fields.One2many(
        comodel_name='order_flow.item',
        inverse_name='shipping_method_id',
        string="Items"
    )
