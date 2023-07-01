from odoo import models, fields, _

class OrderFlowLabelRequest(models.Model):
    _name = 'order_flow.label_request'
    _description = 'Label Request'
    _order = 'id'

    item_id = fields.Many2one('order_flow.item', string="Item", required=True)

    label_type_id = fields.Many2one(
        comodel_name='order_flow.label_type',
        string='Label Type',
        required=True
    )

    sticker_status = fields.Selection([
        ('pending', 'Pending'),
        ('printed', 'Printed'),
        ('finished', 'Finished'),
    ],
        string='Sticker Status',
        default='pending',
        required=True
    )