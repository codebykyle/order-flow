// noinspection JSVoidFunctionReturnValueUsed

odoo.define('order_flow.print_label_button', function (require) {
    "use strict";
    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var viewRegistry = require('web.view_registry');

    var TreeButton = ListController.extend({
        buttons_template: 'order_flow.print_label.buttons',

        events: _.extend({}, ListController.prototype.events, {
            'click .open_wizard_action': '_OpenWizard',
        }),

        _OpenWizard: function () {
            var self = this;

            this.do_action({
                type: 'ir.actions.act_window',
                res_model: 'order_flow.label_request.print_label',
                name: 'Print Label Sheet',
                view_mode: 'form',
                views: [[false, 'form']],
                view_id: 'order_flow_label_request_print_form',
                target: 'new',
                res_id: false,
            });
        }
    });

    var SaleOrderListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: TreeButton,
        }),
    });

    viewRegistry.add('print_label_button', SaleOrderListView);
});