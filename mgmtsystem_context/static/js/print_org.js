odoo.define('mgmtsystem_context.org_chart', function (require) {
    "use strict";

    var form_widget = require('web.form_widgets');
    var core = require('web.core');
    var _t = core._t;
    var QWeb = core.qweb;

    form_widget.WidgetButton.include({
        on_click: function () {
            // var chartWidth = document.querySelector('tbody').offsetWidth}
            var self = this;
            var org_chart = QWeb.render('org_chart_employee.org_chart_template', {
                widget: self,
            });
            // var printContents = document.getElementById('chart-container').innerHTML;
            // var originalContents = document.body.innerHTML;
            // document.body.innerHTML = printContents;
            // document.body.style.zoom = '0.6'
            // window.print();
            // document.body.innerHTML = originalContents;

            return;

            this._super();
        },
    });
});