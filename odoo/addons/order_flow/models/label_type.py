from odoo import models, fields, api

class OrderFlowLabelType(models.Model):
    _name = 'order_flow.label_type'
    _description = 'Label Type'
    _order = 'id'

    name = fields.Char('Label Name', required=True)
    generates_label = fields.Boolean(string='Produces a label', default=True)

    api_endpoint = fields.Char(string='API Endpoint')
    sheet_api_name = fields.Char('Sheet API Name')
    label_api_name = fields.Char('Label API Name')

    sticker_x_count = fields.Integer('Stickers X', default=1)
    sticker_y_count = fields.Integer('Stickers Y', default=1)
    sticker_count = fields.Integer("Sticker Count", compute="_calculate_sticker_count")

    last_used_sheet_number = fields.Integer("Last Used Sheet")
    last_used_position = fields.Integer("Last Used Position", default=0)

    is_default = fields.Boolean(string='Is Default')

    item_ids = fields.One2many(
        comodel_name='order_flow.item',
        inverse_name='label_type_id',
        string='Items'
    )

    pending_label_ids = fields.One2many(
        comodel_name='order_flow.label_request',
        inverse_name='label_type_id',
        string='Pending Labels'
    )

    @api.depends('sticker_x_count', 'sticker_y_count')
    def _calculate_sticker_count(self):
        for item in self:
            item.sticker_count = item.sticker_x_count * item.sticker_y_count