/** @odoo-module */

import { Component, useState, onWillStart, useRef } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";

import { MONTHS } from "../../utils";

class RPERemediationActionReport extends Component {
    static template = 'tyt_risk_management.RPERemediationAction';

    static components = {
        Layout,
    };

    setup() {

        this.notification = useService("notification");
        this.orm = useService("orm");
        this.state = useState({
            filters: {

                department_id: "0",
                year: "0",
                cr_period: "month",
                revision_type: "0",
            },

            //data filters 
            loading: false,
            years: [],
            departments: [],
        });

        this.reportData = useState({
            "totals": {},
            "report": [],
            "periods": [],
        });

        this.dialog = useService("dialog");
        onWillStart(async () => {
            await this.loadFilters();

            this.onSearch()
        });



    }


    async loadFilters() {
        await this.loadDepartments();
        try {
            const availableYears = await this.orm.call(
                "tyt.risk.mitigation",
                "get_available_years",
                []
            );
            this.state.years = availableYears;
            if (availableYears) {
                this.state.filters.year = availableYears[0];
            }
        } catch (error) {
            this.notification.add(
                "Errror al cargar los años",
                {type: "danger"},
            )
            console.error("Error cargando anos:", error);
        }


    }
    async loadDepartments() {
        try {
            const data = await this.orm.searchRead(
                "hr.department",
                [['x_studio_npp', '=', 1]],
                ["id", "name",]
            );
            this.state.departments = data ;
        } catch (error) {
            console.error("Error cargando domains:", error);
        }
    }


    async openMitigation(mIds = []) {
        console.log("mids", mIds);
        await this.dialog.add(MitigationModal, {
            title: "Lista de riesgos",
            mIds,
            actionId: this.idActionActivity,
            showAction: true,
        });
    }

    async onSearch() {
        try {
            this.state.loading = true;
            const data = await this.orm.call(
                "tyt.risk.mitigation",     
                "rpe_remedition_action", 
                [ 
                    this.state.filters.department_id, 
                    this.state.filters.year,
                    this.state.filters.cr_period,
                    this.state.filters.revision_type,
                ]
            );
            this.reportData.periods = data.periods || [];
            this.reportData.report = data.report || [];
            this.reportData.totals = data.totals || {};

        } catch (error) {
            console.error("Error carga de report:", error);
            this.notification.add(
                "Errror al cargar el reporte",
                {type: "danger"},
            )
        } finally {
            this.state.loading = false;
        }
    }

    nivelStyle(nivel) {
        const MAP = {
            'sys_sox_reme_open':   "background-color: #e53935; color: #fff; font-weight: bold; font-size: 16px;",
            'sys_sox_reme_process':  " background-color: rgb(255,215,0); color: #222; font-weight: bold; font-size: 16px;",
            'sys_sox_reme_complete':  "background-color: rgb(154,205,50); color: #222; font-weight: bold; font-size: 16px;",
        };
        return MAP[nivel] ?? '';
    }
}

registry.category("actions").add("tyt_risk_management.rpe_remediation_action_report", RPERemediationActionReport);
