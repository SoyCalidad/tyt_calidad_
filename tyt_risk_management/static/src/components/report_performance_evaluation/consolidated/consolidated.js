/** @odoo-module */

import { Component, useState, onWillStart, useRef } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";

import { MONTHS } from "../../utils";

class RPEConsolidatedReport extends Component {
    static template = 'tyt_risk_management.RPEConsolidated';

    static components = {
        Layout,
    };

    setup() {

        this.orm = useService("orm");
        this.state = useState({
            filters: {
                departmentIds: "0",
                selectedYear: "0",
                selectedPeriod: "0",
            },

            //data filters 
            loading: false,
            years: [],
            departments: [],
        });

        this.reportData = useState({
            "reporte": [
                {
                    "titulo": null,
                    "company_name": "Subsidiaria 1",
                    "company_id": "92e5d90a-d25d-4a39-84ca-9f37dd8265e3",
                    "t1": null,
                    "t2": null,
                    "t3": null,
                    "t4": null,
                    "total": 177,
                    "porcentaje": 100,
                    "periodos": [
                        {
                            "periodo": 1,
                            "mitigado": 1,
                            "parcial": 2,
                            "no": 87,
                            "total": 90
                        },
                        {
                            "periodo": 2,
                            "mitigado": 1,
                            "parcial": 0,
                            "no": 86,
                            "total": 87
                        },
                        {
                            "periodo": 3,
                            "mitigado": 0,
                            "parcial": 0,
                            "no": 0,
                            "total": 0
                        },
                        {
                            "periodo": 4,
                            "mitigado": 0,
                            "parcial": 0,
                            "no": 0,
                            "total": 0
                        }
                    ]
                }
            ],
            "totales": {
                "titulo": "sys_sox1_nivel_total",
                "company_name": null,
                "company_id": null,
                "t1": null,
                "t2": null,
                "t3": null,
                "t4": null,
                "total": 177,
                "porcentaje": 100,
                "periodos": [
                    {
                        "periodo": 1,
                        "mitigado": 1,
                        "parcial": 2,
                        "no": 87,
                        "total": 90
                    },
                    {
                        "periodo": 2,
                        "mitigado": 1,
                        "parcial": 0,
                        "no": 86,
                        "total": 87
                    },
                    {
                        "periodo": 3,
                        "mitigado": 0,
                        "parcial": 0,
                        "no": 0,
                        "total": 0
                    },
                    {
                        "periodo": 4,
                        "mitigado": 0,
                        "parcial": 0,
                        "no": 0,
                        "total": 0
                    }
                ]
            }
        });

        this.dialog = useService("dialog");
        onWillStart(async () => {
            await this.loadFilters();

            await this.onSearch()
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
        // try {
        //     const data = await this.orm.call(
        //         "tyt.business.process",     
        //         "data_status_report", 
        //         [
        //             this.state.filters.department_id,
        //             this.state.filters.domain_id,
        //             this.state.filters.process_id,
        //             this.state.filters.year,
        //             this.state.filters.month,
        //         ]
        //     );
        //     this.state.reportData = data;

        // } catch (error) {
        //     console.error("Error cargando procesos:", error);
        // }
        setTimeout(() => {
            this.state.loading = false;
        }, 500);
    }
}

registry.category("actions").add("tyt_risk_management.rpe_consolidated_report", RPEConsolidatedReport);
