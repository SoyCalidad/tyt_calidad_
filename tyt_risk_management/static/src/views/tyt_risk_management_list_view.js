import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";

//import { AccountMoveListController } from "./account_move_list_controller";
import { RiskQuantificationListRenderer } from "./tyt_risk_management_renderer";

export const riskQuantificationListView = {
    ...listView,
    Renderer: RiskQuantificationListRenderer,
    // buttonTemplate: "account.AccountMoveListView.Buttons",
};

registry.category("views").add("risk_quantification_list", riskQuantificationListView);

