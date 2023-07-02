import base64
import math

from odoo import http
from odoo.http import request, Response, content_disposition
import json
import requests

import logging

_logger = logging.getLogger(__name__)


class PrintLabelController(http.Controller):
    @http.route('/web/binary/download_pending_labels', type='http', auth="user")
    def downloading_pending_labels(self, label_type_id, new_sheet, **kw):
        """ Download link for files stored as binary fields.
        :param int label_type: name of the model to fetch the binary from
        :param bool new_sheet: to start at index 0 or not
        :returns: :class:`werkzeug.wrappers.Response`
        """
        cr, uid, context = request.cr, request.uid, request.context

        res = request.env['order_flow.label_type'].browse([
            int(label_type_id)
        ])

        # Use the first record
        res = res[0]

        _logger.info("Res ID: %s", str(res.id))
        _logger.info('Sticker Count  %s', res.sticker_count)
        _logger.info('Last used sheet sticker: %s', res.last_used_position)
        _logger.info('Query limit: %s',res.sticker_count - res.last_used_position)

        open_label_requests = request.env['order_flow.label_request'].search(
            domain=[
                ['status', '=', 'pending'],
                ['label_type_id', '=', int(res['id'])]
            ],
            limit=res.sticker_count - res.last_used_position
        )

        base_url = http.request.env['ir.config_parameter'].get_param('web.base.url')  # BASE URL
        action_id = http.request.env.ref('order_flow.order_flow_item_action').id

        _logger.info('Open label request result: %s', len(open_label_requests))

        labels_to_generate = []
        start_position = 0 if new_sheet == 'True' else res.last_used_position

        _logger.info('Is new sheet: %s', new_sheet == 'True')
        _logger.info('Start position %s', start_position)

        for blank_item in range(0, start_position):
            labels_to_generate.append({})

        res.last_used_sheet_number += 1
        sheet_name = "Sheet %s" % res.last_used_sheet_number

        for item in open_label_requests:
            item.sticker_x = (len(labels_to_generate) % res.sticker_x_count) + 1
            item.sticker_y = (math.floor(len(labels_to_generate) / res.sticker_x_count)) + 1
            item.page_name = sheet_name
            item.status = 'printed'

            labels_to_generate.append({
                'subtitle': 'Tracked by Adomi',
                'title': item.sticker_name,
                'url': '%s/web#id=%s&action=%s&model=%s&view_type=%s' % (
                    base_url,
                    str(item.item_id.id),
                    str(action_id),
                    'order_flow.item',
                    'form'
                ),
                'barcode': item.item_barcode
            })

        if not res.api_endpoint:
            return

        pdf_content = requests.post(res.api_endpoint, json={
            "sheet_name": sheet_name,
            "items": labels_to_generate
        }).content

        # Save the last used position so we can use the whole sheet
        new_last_used_position = len(labels_to_generate) % res.sticker_count

        _logger.info("Setting new last used position: %s", new_last_used_position)

        res.update({
            'last_used_position': new_last_used_position
        })

        return request.make_response(pdf_content, [
            ('Content-Type', 'application/octet-stream'),
            ('Content-Disposition', content_disposition('labels.pdf'))
        ])
