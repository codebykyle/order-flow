from odoo import models, fields, api


class OrderFlowItem(models.Model):
    _name = 'order_flow.item'
    _description = 'Item'
    _order = 'id'

    _inherit = [
        'documents.mixin',
        'image.mixin'
    ]

    name = fields.Char(required=True)
    name_vietnamese = fields.Char(string="Vietnamese Name")

    description = fields.Html(string="Description")
    description_vietnamese = fields.Html(string="Vietnamese Description")

    item_type = fields.Selection([
        ('object', 'Object'),
        ('box', 'Box'),
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
    barcode = fields.Char(help="Use a barcode to identify this order")

    shipping_method_id = fields.Many2one(
        "order_flow.shipping_method",
        string="Shipping method"
    )

    status = fields.Selection([
        ('draft', 'Draft'),
        ('acknowledged', 'Acknowledged'),
        ('goes_in_container', 'Goes in Container'),
        ('labeled', 'Labeled'),
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

    @api.model
    def _group_expand_status(self, states, domain, order):
        field_set_context = self._context.get('field_set')

        if field_set_context == 'initial':
            return [
                'draft',
                'goes_in_container',
                'for_sale',
                'sold',
                'trashed',
                'acknowledged',
            ]

        return [key for key, val in type(self).status.selection]
