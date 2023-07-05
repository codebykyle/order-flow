from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class OrderFlowContainerContents(models.Model):
    _name = 'order_flow.item_contents'
    _description = "Container Contents"
    _order = 'id'

    name = fields.Char(
        string='Name',
        compute="_calculate_name",
        store=True,
        readonly=False
    )

    parent_image = fields.Image(
        related='parent_item_id.image_1920',
        string="Location Photo"
    )

    child_image = fields.Image(
        related='child_item_id.image_1920',
        string="Item Photo"
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

    def _calculate_name(self):
        for record in self:
            record.name = ' - '.join([
                record.parent_item_id.name,
                record.child_item_id.name
            ])

    @api.constrains('parent_item_id', 'child_item_id')
    def validate_placement(self):
        for record in self:
            if record.parent_item_id.id == record.child_item_id.id:
                raise ValidationError("Item cannot be put into itself")