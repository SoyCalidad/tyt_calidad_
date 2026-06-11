/** @odoo-module */

import { Component, useState, onWillStart, useRef } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";

import { MONTHS } from "../../utils";

export class CarriedOutReport extends Component {
    static template = 'tyt_risk_management.RPECarriedOut';

    static components = {
        Layout,
    };

    nivelStyle(nivel) {
        const MAP = {
            0:   "background-color: #e53935; color: #fff; font-weight: bold; font-size: 14px;",
            25:  " background-color: rgb(217,123,0); color: #fff; font-weight: bold; font-size: 14px;",
            50:  "background-color: rgb(255,215,0); color: #222; font-weight: bold; font-size: 14px;",
            75: "background-color: rgb(0,191,255); color: #222; font-weight: bold; font-size: 14px;",
            100: "background-color: rgb(154,205,50); color: #222; font-weight: bold; font-size: 14px;",
        };
        return MAP[nivel] ?? '';
    }

    setup() {

        const today = new Date()

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
            console.error("Error cargando domains:", error);
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
        this.state.loading = true;
        try {
            const data = await this.orm.call(
                "tyt.risk.mitigation",     
                "rpe_carried_out_report", 
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
            console.error("Error cargando procesos:", error);
        }
        this.state.loading = false;
        
    }
}

registry.category("actions").add("tyt_risk_management.carried_out_report", CarriedOutReport);
