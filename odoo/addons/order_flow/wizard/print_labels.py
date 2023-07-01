from odoo import models, fields, api


class PrintLabels(models.TransientModel):
    _name = 'order_flow.label_request.print'
    _description = 'Print a sheet of labels'

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
                'item_id': self.item_id.id,
                'label_type_id': self.label_type_id.id
            })

        return self.env.get('order_flow.label_request').create(copies)
