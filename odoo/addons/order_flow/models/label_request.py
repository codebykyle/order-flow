import os

from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)


class OrderFlowLabelRequest(models.Model):
    _name = 'order_flow.label_request'
    _description = 'Label Request'
    _order = 'id'

    item_id = fields.Many2one('order_flow.item', string="Item", required=True)

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

    ###############################
    ## Page Details ###############
    ###############################
    page_name = fields.Char(string="Label on page")
    sticker_x = fields.Char(string="Col")
    sticker_y = fields.Char(string="Row")

    ###############################
    ## Calculated Fields ##########
    ###############################
    sticker_position = fields.Char(
        string="Sticker Position",
        compute="_calculate_sticker_position"
    )

    sticker_name = fields.Char(
        string="Sticker Name",
        compute="_calculate_sticker_name"
    )

    item_name = fields.Char(
        string='Item Name',
        related='item_id.name',
        readonly=True
    )

    item_label_name = fields.Char(
        string='Item Label Name',
        related='item_id.label_name',
        readonly=True
    )

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

    @api.onchange('status')
    def _recompute_parent(self):
        for record in self:
            record.item_id._compute_pending_labels()

    @api.depends('sticker_y', 'sticker_x', 'page_name')
    def _calculate_sticker_position(self):
        for record in self:
            if not  record.page_name:
                record.sticker_position = 'Not Printed'
                continue

            record.sticker_position = '%s: Row: %s Col: %s' % (
                record.page_name,
                record.sticker_y,
                record.sticker_x
            )


    @api.depends('item_label_name')
    def _calculate_sticker_name(self):
        for record in self:
            _logger.info("Calculating sticker name for ID %s", record.id)
            new_name = record.item_label_name

            if not new_name:
                new_name = record.item_barcode

            if not new_name and record.id:
                new_name = "{:08d}".format(int(record.id))

            record.sticker_name = new_name

    def default_label_type(self):
        field_set_context = self._context.get('item_label_type_id')

        if field_set_context:
            return field_set_context

        default_id = self.env.get('order_flow.label_type').search([
            ('is_default', '=', True)
        ]).id

        _logger.info('Using default id: %s', default_id)

        return default_id

    @api.model
    def _group_expand_status(self, states, domain, order):
        return [key for key, val in type(self).status.selection]
