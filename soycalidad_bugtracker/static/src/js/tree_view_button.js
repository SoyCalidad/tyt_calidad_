odoo.define('soycalidad_bugtracker.tree_view_button', function (require) {
    "use strict";

    var core = require('web.core');
    var ListView = require('web.ListView');
    var ListController = require("web.ListController");

    var IncludeListView = {

        buttons_template: 'ListView.buttons',
        events: _.extend({}, ListController.prototype.events, {
            'click .o_list_bug_report': 'crete_leave_from_summary',
        }),
        crete_leave_from_summary: function () {
            var self = this;
            var action = {
                type: 'ir.actions.act_url',
                target: "new",
                url: "https://forms.gle/EjwLyPoFtcM5WojY8",
            };
            return this.do_action(action);
        },

    };
    ListController.include(IncludeListView);
});