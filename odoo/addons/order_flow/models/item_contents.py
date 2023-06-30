from odoo import models, fields, _


class OrderFlowContainerContents(models.Model):
    _name = 'order_flow.item_contents'
    _description = "Container Contents"
    _order = 'id'

    name = fields.Char(
        string='Name',
        related='child_item_id.name',
        store=True,
        readonly=False
    )

    parent_item_id = fields.Many2one(
        'order_flow.item',
        string='Location'
    )

    child_item_id = fields.Many2one(
        'order_flow.item',
        string='Item'
    )

    quantity = fields.Integer(string='Quantity')
