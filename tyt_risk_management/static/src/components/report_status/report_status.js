/** @odoo-module */

import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { registry } from "@web/core/registry";
import { loadBundle } from "@web/core/assets";

import { PieChart } from "../pie_chart/pie_chart";
import {CollapsibleCard } from "../collapsible_card/collapsible_card";
import { MitigationModal } from "./mitigation_modal/mitigation_modal";


export class Nivel2StatusReport extends Component {
    static template = 'tyt_risk_management.report_nivel2_status';
    static components = { Layout, PieChart, CollapsibleCard, MitigationModal   };

    setup() {
        this.orm = useService("orm");
        this.state = useState({
            filters: {
                department_id: "0",
                domain_id: "0",
                process_id: "0",
                year: '0',
                month: '0',
            },
            processedData: [
                {
                    "process_id": "46e7694e-a647-462d-9421-9955f529998c",
                    "process_short_name": "ASG",
                    "process_name": "Sostenibilidad",
                    "total": 41,
                    "registros_total": [2,3,4],
                    "is_not_scope": 0,
                    "registros_is_not_scope": [],
                    "is_open": 36,
                    "registros_is_open": [ 2  ],
                    "is_review": 2,
                    "registros_is_review": [2,3
                    ],
                    "is_remediation": 2,
                    "registros_is_remediation": [ 2
                    ],
                    "is_audit": 0,
                    "registros_is_audit": [],
                    "is_completed": 1,
                    "registros_is_completed": [ 2
                    ],
                    "is_completed_percentage": 2,
                    
                    "no_completed": 40,
                    "registros_no_completed": [
                        2,6,3,2
                    ],
                    "subProcesos": [
                        {
                            "sub_process_id": "93be569b-d103-4503-8189-1813d202adbb",
                            "sub_process_name": "Ambiental_Social_Gobernanza",
                            "total": 41,
                            "registros_total": [2,3],
                            "is_not_scope": 0,
                            "registros_is_not_scope": [],
                            "is_open": 36,
                            "registros_is_open": [2,3],
                            "is_review": 2,
                            "registros_is_review": [3],
                            "is_remediation": 2,
                            "registros_is_remediation": [2,3],
                            "is_audit": 0,
                            "registros_is_audit": [],
                            "is_completed": 1,
                            "registros_is_completed": [2
                            ],
                            "is_completed_percentage": {
                                "source": "2.00",
                                "parsedValue": 2
                            },
                            "no_completed": 40,
                            "registros_no_completed":  [2,3,4]
                        }
                    ]
                }

            ],

            //data filters 
            processes: [],
            domains: [],
            months: [
                { id: 1, name: 'Enero' },
                { id: 2, name: 'Febrero' },
                { id: 3, name: 'Marzo' },
                { id: 4, name: 'Abril' },
                { id: 5, name: 'Mayo' },
                { id: 6, name: 'Junio' },
                { id: 7, name: 'Julio' },
                { id: 8, name: 'Agosto' },
                { id: 9, name: 'Setiembre' },
                { id: 10, name: 'Octubre' },
                { id: 11, name: 'Noviembre' },
                { id: 12, name: 'Diciembre' },
            ],
            years: [],
            departments: [],
        });

        this.dialog = useService("dialog");

        onWillStart(async () => {
            await loadBundle("web.chartjs_lib")
            await this.loadFilters();
            await this.fetchInitialData();

            await this.onSearch()
        });
    }

    async onChangeDomain() {
        console.log("onchangedomain", this.state.filters.domain_id);
        await this.cargarProcesos();
    }

    async loadFilters() {
        await this.loadDomains();
        await this.cargarProcesos();
        await this.loadDepartments();
        const availableYears = await this.orm.call(
            "tyt.risk.mitigation",     
            "get_available_years", 
            []
        );
        this.state.years = availableYears;

        
    }
    async loadDepartments() {
        try {
            const data = await this.orm.searchRead(
                "hr.department", 
                [['x_studio_npp', '=', 1]], 
                ["id", "name",]
            );
            this.state.departments = data;
        } catch (error) {
            console.error("Error cargando domains:", error);
        }
    }

    async loadDomains() {
        try {
            const data =  await this.orm.searchRead(
                "tyt.business.process", 
                [["level", "=", 1]],
                ["id", "name", "short_name"],
            );
            
            this.state.domains = data;
        } catch (error) {
            console.error("Error cargando domains:", error);
        }
    }

    async cargarProcesos() {
        try {
            const domain = [["level", "=", "2"]];
            const domainValue = this.state.filters.domain_id;
            console.log("domainValue", domainValue)
            if (domainValue && domainValue!="0") {
                domain.push(["parent_id", "=", Number(domainValue)])
            }
            console.log("domain process ", domain)
            const data = await this.orm.searchRead(
                "tyt.business.process", 
                domain,
                ["id", "name", "short_name"]);
            this.state.processes = data;
        } catch (error) {
            console.error("Error cargando procesos:", error);
        }
    }

    async fetchInitialData() {
        // Simulación de carga de datos basada en tu JSON
        // En producción: this.state.data = await this.orm.call(...)
        this.state.processedData = [/* Tu JSON aquí */];

        const actionId = await this.orm.call(
            "tyt.risk.mitigation",
            "get_form_action_id",
            [[]]
        );
        this.idActionActivity = actionId; //actionId
    }


    async openMitigation(mIds = []) {
        console.log("mids", mIds);
        await this.dialog.add(MitigationModal, {
            title: "Lista de riesgos",
            mIds,
            actionId: this.idActionActivity,
        });
    }

    async onSearch() {
        try {
            const data = await this.orm.call(
                "tyt.business.process",     
                "data_status_report", 
                [
                    this.state.filters.department_id,
                    this.state.filters.domain_id,
                    this.state.filters.process_id,
                    this.state.filters.year,
                    this.state.filters.month,
                ]
            );
            this.state.processedData = data;

        } catch (error) {
            console.error("Error cargando procesos:", error);
        }
    }
}

registry.category("actions").add("tyt_risk_management.nivel2statusreport", Nivel2StatusReport);
