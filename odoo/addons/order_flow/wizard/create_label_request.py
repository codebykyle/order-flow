from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)


class CreateLabelRequests(models.TransientModel):
    _name = 'order_flow.label_request.bulk_create'
    _description = 'Create label requests for this product'

    item_id = fields.Many2one(
        'order_flow.item',
        string="Item",
        required=True
    )

    label_type_id = fields.Many2one(
        comodel_name='order_flow.label_type',
        string='Label Type',
        required=True,
        default=lambda self: self.default_label_type()
    )

    record_set = fields.Selection([
        ('this', 'Only this item'),
        ('non_labeled', 'Non-labeled contents'),
        ('all', 'All Contents')
    ], default='this',
        string="Record set")

    quantity = fields.Integer(
        string='Quantity',
        default=1
    )

    def default_label_type(self):
        field_set_context = self._context.get('item_label_type_id')

        if field_set_context:
            return field_set_context

        default_id = self.env.get('order_flow.label_type').search([
            ('is_default', '=', True)
        ]).id

        return default_id

    def traverse_items(self, item, copies, only_unprinted):
        if len(item.sub_item_ids) > 0:
            for sub_item_id in item.sub_item_ids:
                _logger.info('Looking up: %s' % sub_item_id.child_item_id)
                self.traverse_items(sub_item_id.child_item_id, copies, only_unprinted)

        should_add = True

        if only_unprinted:
            has_print_request = self.env['order_flow.label_request'].search([
                ['item_id', '=', item.id]
            ])

            if len(has_print_request) > 0:
                should_add = False

        if should_add:
            copies.append({
                'item_id': item['id'],
                'label_type_id': self.label_type_id.id
            })

        return copies

    def create_label_request(self):
        self.ensure_one()
        copies = []

        if self.record_set == 'this':
            for number in range(0, self.quantity):
                copies.append({
                    'item_id': self.item_id.id,
                    'label_type_id': self.label_type_id.id
                })
        else:
            self.traverse_items(self.item_id, copies, self.record_set == 'non_labeled')

        self.env.get('order_flow.label_request').create(copies)

        params = self.env.context
        _logger.info('context %s', params)

        if 'redirect' in self.env.context and self.env.context['redirect']:
            redirect_action = self.env.ref(self.env.context['redirect']).read()[0]
            redirect_action['target'] = 'main'

            return redirect_action
