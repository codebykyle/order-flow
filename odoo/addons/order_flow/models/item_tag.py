from odoo import models, fields, _

class OrderFlowItemTag(models.Model):
    _name = 'order_flow.item_tag'
    _description = 'Item Tag'
    _order = 'id'

    item_id = fields.Many2one('order_flow.item')

    name = fields.Char('Tag Name', required=True)
    color = fields.Integer('Color Index')

    integration_code = fields.Char(string='Integration Code')
