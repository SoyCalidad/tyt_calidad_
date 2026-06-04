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
            "report": [
                {
                    "company_name": "Subsidiaria 1",
                    "company_id": "92e5d90a-d25d-4a39-84ca-9f37dd8265e3",
                    "items": [
                        {
                            "titulo": "sys_sox1_nivel_0",
                            "nivel": 0,
                            "periodos": [
                                {
                                    "periodo": "1",
                                    "valor": 87
                                },
                                {
                                    "periodo": "2",
                                    "valor": 86
                                },
                                {
                                    "periodo": "3",
                                    "valor": 0
                                },
                                {
                                    "periodo": "4",
                                    "valor": 0
                                }
                            ],
                            "total": 173,
                            "porcentaje": 97.74
                        },
                        {
                            "titulo": "sys_sox1_nivel_25",
                            "nivel": 25,
                            "periodos": [
                                {
                                    "periodo": "1",
                                    "valor": 1
                                },
                                {
                                    "periodo": "2",
                                    "valor": 0
                                },
                                {
                                    "periodo": "3",
                                    "valor": 0
                                },
                                {
                                    "periodo": "4",
                                    "valor": 0
                                }
                            ],
                            "total": 1,
                            "porcentaje": 0.56
                        },
                        {
                            "titulo": "sys_sox1_nivel_50",
                            "nivel": 50,
                            "periodos": [
                                {
                                    "periodo": "1",
                                    "valor": 0
                                },
                                {
                                    "periodo": "2",
                                    "valor": 0
                                },
                                {
                                    "periodo": "3",
                                    "valor": 0
                                },
                                {
                                    "periodo": "4",
                                    "valor": 0
                                }
                            ],
                            "total": 0,
                            "porcentaje": 0
                        },
                        {
                            "titulo": "sys_sox1_nivel_75",
                            "nivel": 75,
                            "periodos": [
                                {
                                    "periodo": "1",
                                    "valor": 1
                                },
                                {
                                    "periodo": "2",
                                    "valor": 0
                                },
                                {
                                    "periodo": "3",
                                    "valor": 0
                                },
                                {
                                    "periodo": "4",
                                    "valor": 0
                                }
                            ],
                            "total": 1,
                            "porcentaje": 0.56
                        },
                        {
                            "titulo": "sys_sox1_nivel_100",
                            "nivel": 100,
                            "periodos": [
                                {
                                    "periodo": "1",
                                    "valor": 1
                                },
                                {
                                    "periodo": "2",
                                    "valor": 1
                                },
                                {
                                    "periodo": "3",
                                    "valor": 0
                                },
                                {
                                    "periodo": "4",
                                    "valor": 0
                                }
                            ],
                            "total": 2,
                            "porcentaje": 1.13
                        }
                    ],
                    "totales": {
                        "titulo": "sys_sox1_nivel_total",
                        "nivel": 0,
                        "periodos": [
                            {
                                "periodo": "1",
                                "valor": 90
                            },
                            {
                                "periodo": "2",
                                "valor": 87
                            },
                            {
                                "periodo": "3",
                                "valor": 0
                            },
                            {
                                "periodo": "4",
                                "valor": 0
                            }
                        ],
                        "total": 177,
                        "porcentaje": 100
                    }
                },
            ],
    "totals": {
            "company_name": "sys_report_sox_1",
            "company_id": "sys_report_sox_1",
            "items": [
                {
                    "titulo": "sys_sox1_nivel_0",
                    "nivel": 0,
                    "periodos": [
                        {
                            "periodo": "1",
                            "valor": 87
                        },
                        {
                            "periodo": "2",
                            "valor": 86
                        },
                        {
                            "periodo": "3",
                            "valor": 0
                        },
                        {
                            "periodo": "4",
                            "valor": 0
                        }
                    ],
                    "total": 173,
                    "porcentaje": 97.74
                },
                {
                    "titulo": "sys_sox1_nivel_25",
                    "nivel": 25,
                    "periodos": [
                        {
                            "periodo": "1",
                            "valor": 1
                        },
                        {
                            "periodo": "2",
                            "valor": 0
                        },
                        {
                            "periodo": "3",
                            "valor": 0
                        },
                        {
                            "periodo": "4",
                            "valor": 0
                        }
                    ],
                    "total": 1,
                    "porcentaje": 0.56
                },
                {
                    "titulo": "sys_sox1_nivel_50",
                    "nivel": 50,
                    "periodos": [
                        {
                            "periodo": "1",
                            "valor": 0
                        },
                        {
                            "periodo": "2",
                            "valor": 0
                        },
                        {
                            "periodo": "3",
                            "valor": 0
                        },
                        {
                            "periodo": "4",
                            "valor": 0
                        }
                    ],
                    "total": 0,
                    "porcentaje": 0
                },
                {
                    "titulo": "sys_sox1_nivel_75",
                    "nivel": 75,
                    "periodos": [
                        {
                            "periodo": "1",
                            "valor": 1
                        },
                        {
                            "periodo": "2",
                            "valor": 0
                        },
                        {
                            "periodo": "3",
                            "valor": 0
                        },
                        {
                            "periodo": "4",
                            "valor": 0
                        }
                    ],
                    "total": 1,
                    "porcentaje": 0.56
                },
                {
                    "titulo": "sys_sox1_nivel_100",
                    "nivel": 100,
                    "periodos": [
                        {
                            "periodo": "1",
                            "valor": 1
                        },
                        {
                            "periodo": "2",
                            "valor": 1
                        },
                        {
                            "periodo": "3",
                            "valor": 0
                        },
                        {
                            "periodo": "4",
                            "valor": 0
                        }
                    ],
                    "total": 2,
                    "porcentaje": 1.13
                }
            ],
            "totales": {
                "titulo": "sys_sox1_nivel_total",
                "nivel": 0,
                "periodos": [
                    {
                        "periodo": "1",
                        "valor": 90
                    },
                    {
                        "periodo": "2",
                        "valor": 87
                    },
                    {
                        "periodo": "3",
                        "valor": 0
                    },
                    {
                        "periodo": "4",
                        "valor": 0
                    }
                ],
                "total": 177,
                "porcentaje": 100
            }
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

registry.category("actions").add("tyt_risk_management.carried_out_report", CarriedOutReport);
