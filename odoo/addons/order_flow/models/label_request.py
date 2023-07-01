from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)


class OrderFlowLabelRequest(models.Model):
    _name = 'order_flow.label_request'
    _description = 'Label Request'
    _order = 'id'

    item_id = fields.Many2one('order_flow.item', string="Item", required=True)

    item_barcode = fields.Char(
        string='Image',
        related='item_id.barcode',
        readonly=True
    )

    item_image = fields.Binary(
        string='Image',
        related='item_id.image_128',
        readonly=True
    )

    label_type_id = fields.Many2one(
        comodel_name='order_flow.label_type',
        string='Label Type',
        required=True,
        default=lambda self: self.default_label_type()
    )

    status = fields.Selection([
        ('pending', 'Pending'),
        ('printed', 'Printed'),
        ('finished', 'Finished'),
    ],
        string='Sticker Status',
        default='pending',
        required=True,
        group_expand='_group_expand_status'
    )

    def default_label_type(self):
        default_id = self.env.get('order_flow.label_type').search([
            ('is_default', '=', True)
        ]).id

        _logger.info('Using default id: %s', default_id)

        return default_id

    @api.model
    def _group_expand_status(self, states, domain, order):
        return [key for key, val in type(self).status.selection]
