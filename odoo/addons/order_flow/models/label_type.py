from odoo import models, fields

class OrderFlowLabelType(models.Model):
    _name = 'order_flow.label_type'
    _description = 'Label Type'
    _order = 'id'

    name = fields.Char('Label Name', required=True)
    generates_label = fields.Boolean(string='Produces a label', default=True)

    api_endpoint = fields.Char(string='API Endpoint')
    sheet_api_name = fields.Char('Sheet API Name')
    label_api_name = fields.Char('Label API Name')

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