from odoo import models, fields, api


class CreateLabelRequests(models.TransientModel):
    _name = 'order_flow.label_request.bulk_create'
    _description = 'Create label requests for this product'

    item_id = fields.Many2one('order_flow.item', string="Item", required=True)

    label_type_id = fields.Many2one(
        comodel_name='order_flow.label_type',
        string='Label Type',
        required=True
    )

    quantity = fields.Integer(
        string='Quantity',
        default=1
    )


    def create_label_request(self):
        self.ensure_one()
        copies = []

        for number in range(0, self.quantity):
            copies.append({
                'item_id': self.item_id,
                'label_type_id': self.label_type_id
            })

        return self.env.get('order_flow.label_request').create(copies)
