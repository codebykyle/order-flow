from odoo import models, fields, _

class OrderFlowItemMeta(models.Model):
    _name = 'order_flow.item_meta'
    _description = 'Item Meta'
    _order = 'name'

    item_id = fields.Many2one('order_flow.item')

    name = fields.Char(string='Name')
    value = fields.Char(string="Value")