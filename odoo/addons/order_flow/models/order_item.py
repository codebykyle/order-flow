from odoo import models, fields, api


class OrderFlowOrderItem(models.Model):
    _name = 'order_flow.order_item'
    _description = 'Order Item'

    _inherit = [
    ]

    name = fields.Char(
        string='Name',
        related='item_id.name',
        store=True,
        readonly=False
    )

    currency_id = fields.Many2one(
        'res.currency',
        'Currency',
        default=lambda self: self.env.company.currency_id.id,
        required=True
    )

    order_id = fields.Many2one(
        'order_flow.order',
        string='Order'
    )

    item_id = fields.Many2one(
        'order_flow.item',
        string='Item'
    )

    quantity = fields.Integer(string='Quantity', default=1)

    amount_subtotal = fields.Float(string='Sub-Total', default=0)
    amount_shipping = fields.Float(string='Shipping', default=0)
    amount_vat = fields.Float(string='VAT', default=0)
    amount_tax = fields.Float(string='Tax', default=0)
    amount_discount = fields.Float(string='Discount', default=0)
    amount_final_total = fields.Float(string='Total', default=0)

    integration_code = fields.Char(string="Integration Code")

    per_item_cost = fields.Float(
        string="Per Item Cost",
        compute="_compute_per_item_cost",
        store=True
    )

    @api.depends('amount_subtotal', 'quantity')
    def _compute_per_item_cost(self):
        for record in self:
            record.per_item_cost = record.amount_subtotal / record.quantity