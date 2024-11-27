odoo.define('tyt_intranet_messaging.mark_as_read', function (require) {
    "use strict";

    const ajax = require('web.ajax');

    $(document).ready(function () {
        $('body').on('click', '.mark-as-read', function () {
            const messageId = $(this).data('id');
            if (messageId) {
                ajax.jsonRpc('/mark_as_read', 'call', { message_id: messageId })
                    .then(function (result) {
                        if (result.success) {
                            $(`[data-id="${messageId}"] span`).removeClass('fw-bold');
                            $(`[data-id="${messageId}"]`).removeClass('fw-bold');
                        }
                    });
            }
        });
    });
});
