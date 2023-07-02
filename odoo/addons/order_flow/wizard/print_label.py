from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)


class PrintLabel(models.TransientModel):
    _name = 'order_flow.label_request.print_label'
    _description = 'Print a sheet of labels'

    label_type_id = fields.Many2one(
        comodel_name='order_flow.label_type',
        string='Label Type',
        required=True,
        default=lambda self: self.default_label_type()
    )

    new_sheet = fields.Boolean(string="Start a new sheet", default=False)

    def create_label_request(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary/download_pending_labels?label_type_id=%s&new_sheet=%s' % (
                self.label_type_id.id,
                self.new_sheet
            ),
            'target': 'self'
        }

    def default_label_type(self):
        default_id = self.env.get('order_flow.label_type').search([
            ('is_default', '=', True)
        ]).id

        return default_id