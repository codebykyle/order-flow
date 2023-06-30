from odoo import models, fields, _


class OrderFlowShippingMethod(models.Model):
    _name = 'order_flow.shipping_method'
    _description = 'Planned Shipping Method'
    _order = 'id'

    name = fields.Char('Tag Name', required=True)

    item_ids = fields.One2many(
        comodel_name='order_flow.item',
        inverse_name='shipping_method_id',
        string="Items"
    )

    def action_open_shipping_method_attachments(self):
        self.ensure_one()

        return {
            'name': _("%(shipping_method_name)s's Documents", shipping_method_name=self.name),
            'type': 'ir.actions.act_window',
            'res_model': 'documents.document',
            'domain': [
                ('res_model', '=', self._name),
                ('res_id', '=', self.id)
            ],
            'view_mode': 'kanban,tree,form',
            'context': {
                'default_res_model': self._name,
                'default_res_id': self.id
            },
        }

    def _get_shipping_method_document_data(self):
        documents_data = self.env['documents.document']._read_group(
            domain=[
                ('res_model', '=', self._name),
                ('res_id', 'in', self.ids)
            ],
            fields=[
                'res_id'
            ],
            groupby=[
                'res_id'
            ]
        )

        return {
            document_data['res_id']: document_data['res_id_count'] for document_data in documents_data
        }
