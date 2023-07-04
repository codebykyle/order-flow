import logging
import os

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class OrderFlowItem(models.Model):
    _name = 'order_flow.item'
    _description = 'Item'
    _order = 'create_date DESC, id'

    _inherit = [
        'image.mixin'
    ]

    @api.model
    def _get_random_token(self):
        return str(int.from_bytes(os.urandom(4), 'little'))


    name = fields.Char(required=True)
    label_name = fields.Char(string="Label Name")
    name_vietnamese = fields.Char(string="Vietnamese Name")

    description = fields.Html(string="Description")
    description_vietnamese = fields.Html(string="Vietnamese Description")

    label_type_id = fields.Many2one(
        comodel_name='order_flow.label_type',
        string='Label Type'
    )

    item_type = fields.Selection([
        ('object', 'Object'),
        ('box', 'Box'),
        ('part', 'Part'),
        ('project', 'Project')
    ],
        string='Item Type',
        default='object',
        required=True
    )

    size_height = fields.Float(string='Height in cm')
    size_width = fields.Float(string='Width in cm')
    size_depth = fields.Float(string='Depth in cm')
    weight = fields.Float(string='Weight in grams')

    integration_code = fields.Char(string="Integration Code")
    barcode = fields.Char(help="Use a barcode to identify this order", default=_get_random_token)

    shipping_method_id = fields.Many2one(
        "order_flow.shipping_method",
        string="Shipping method"
    )

    status = fields.Selection([
        ('draft', 'Draft'),
        ('acknowledged', 'Acknowledged'),
        ('goes_in_container', 'Goes in Container'),
        ('has_a_parent', 'Has a parent'),
        ('packing', 'Packing'),
        ('sealed', 'Sealed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('for_sale', 'For Sale'),
        ('sold', 'Sold'),
        ('trashed', 'Trashed'),
    ],
        string='Status',
        default='draft',
        required=True,
        group_expand='_group_expand_status'
    )

    asking_price = fields.Float(string="Asking Price")

    pending_label_request_ids = fields.One2many(
        comodel_name='order_flow.label_request',
        inverse_name='item_id',
        string='Pending Label Requests'
    )

    sub_item_ids = fields.One2many(
        comodel_name='order_flow.item_contents',
        inverse_name='parent_item_id',
        string='Sub-Items'
    )

    storage_ids = fields.One2many(
        'order_flow.item_contents',
        'child_item_id',
        string='Stored location of items'
    )

    order_item_ids = fields.One2many(
        'order_flow.order_item',
        'item_id',
        string='Incoming order items'
    )

    adjustment_ids = fields.One2many(
        comodel_name='order_flow.item_adjustment',
        inverse_name='item_id',
        string='Adjustments'
    )

    item_meta_ids = fields.One2many(
        'order_flow.item_meta',
        'item_id',
        string="Metadata"
    )

    item_tag_ids = fields.Many2many(
        comodel_name='order_flow.item_tag',
        string='Tags'
    )

    ###############################
    ## Aggregates #################
    ###############################

    average_price = fields.Float(
        string="Average Purchase Price",
        compute="_compute_average_price",
        store=True
    )

    count_remaining_inventory = fields.Integer(
        string="Remaining Inventory",
        compute="_compute_count_remaining_inventory",
        store=True
    )

    count_pending_label_requests = fields.Integer(
        string="Pending Label Requests",
        compute="_compute_pending_labels",
        store=True
    )

    _sql_constraints = [
        ('barcode_event_uniq', 'unique(barcode)', "Barcode should be unique")
    ]

    def click_pending_labels(self):
        pass

    @api.depends('pending_label_request_ids', 'pending_label_request_ids.status')
    def _compute_pending_labels(self):
        for record in self:
            label_sum_query = self.env['order_flow.label_request'].search(
                [
                    ('item_id', '=', record.id),
                    ('status', '=', 'pending')
                ]
            )

            label_sum = len(label_sum_query)
            record.count_pending_label_requests = label_sum

    def click_count_remaining_inventory(self):
        pass

    @api.depends(
        'order_item_ids',
        'storage_ids',
        'adjustment_ids',
        'order_item_ids.quantity',
        'storage_ids.quantity',
        'adjustment_ids.quantity'
    )
    def _compute_count_remaining_inventory(self):
        for record in self:
            order_sum_result = self.env['order_flow.order_item'].read_group(
                [('item_id', '=', record.id)],
                ['item_id', 'quantity:sum'],
                ['item_id'],
            )

            stored_sum_result = self.env['order_flow.item_contents'].read_group(
                [('child_item_id', '=', record.id)],
                ['child_item_id', 'quantity:sum'],
                ['child_item_id'],
            )

            adjustment_sum_result = self.env['order_flow.item_adjustment'].read_group(
                [('item_id', '=', record.id)],
                ['item_id', 'quantity:sum'],
                ['item_id'],
            )

            order_sum = order_sum_result[0]['quantity'] if len(order_sum_result) > 0 else 0
            stored_sum = stored_sum_result[0]['quantity'] if len(stored_sum_result) > 0 else 0
            adjustment_sum = adjustment_sum_result[0]['quantity'] if len(adjustment_sum_result) > 0 else 0

            record.count_remaining_inventory = order_sum - stored_sum - adjustment_sum

    def click_average_price(self):
        pass

    @api.depends('order_item_ids.per_item_cost')
    def _compute_average_price(self):
        for record in self:
            order_sum = self.env['order_flow.order_item'].read_group(
                [('item_id', '=', record.id)],
                ['item_id', 'per_item_cost:avg'],
                ['item_id'],
            )

            _logger.info(order_sum)

            record.average_price = order_sum[0]['per_item_cost'] if len(order_sum) > 0 else 0

    @api.model
    def _name_search(
            self,
            name='',
            args=None,
            operator='ilike',
            limit=100,
            name_get_uid=None
    ):
        args = list(args or [])

        if name:
            args += [
                '|',
                ('barcode', operator, name),
                ('name', operator, name)
            ]

        return self._search(
            args,
            limit=limit,
            access_rights_uid=name_get_uid
        )

    @api.model
    def _group_expand_status(self, states, domain, order):
        field_set_context = self._context.get('field_set')

        if field_set_context == 'initial':
            return [
                'draft',
                'goes_in_container',
                'has_a_parent',
                'for_sale',
                'sold',
                'trashed',
                'acknowledged',
            ]

        return [key for key, val in type(self).status.selection]
