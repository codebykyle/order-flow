from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    integration_code = fields.Char()
