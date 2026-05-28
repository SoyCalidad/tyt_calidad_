/** @odoo-module **/

import {
    Component,
    onMounted,
    onWillStart,
    onWillUnmount,
    useRef,
    useState
} from "@odoo/owl";

import { PieChart } from "../../pie_chart/pie_chart";


export class Subprocess extends Component {

    static template = "tyt_risk_management.RCSubprocess";

    static props = {
        process: Object,
    };

    static components = {
        PieChart,
    }

    setup() {
        this.barChartRef = useRef("barChart");
        onMounted(() => {
           this.renderBarChart();
        });
    }

    renderBarChart() {
        const ctx = this.barChartRef.el.getContext("2d");

        this.barChart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: [
                    "No mitigado",
                    "Parcialmente Mitigado",
                    "Mitigado",
                ],
                datasets: [{
                    data: this.props.data_status_risk || [0,0,0],

                    backgroundColor: [
                        "#ef4444",
                        "#f59e0b",
                        "#22c55e",
                    ],

                    borderRadius: 8,
                    maxBarThickness: 80,
                }],
            },

            options: {
                responsive: true,
                plugins: {
                    legend: {

                        position: "bottom",

                        labels: {

                            usePointStyle: true,
                            pointStyle: "circle",

                            generateLabels: (chart) => {

                                const dataset = chart.data.datasets[0];

                                return chart.data.labels.map((label, index) => ({
                                    text: `${dataset.data[index]} ${label}`,
                                    fillStyle: dataset.backgroundColor[index],
                                    strokeStyle: dataset.backgroundColor[index],
                                    hidden: false,
                                    index,
                                }));
                            },
                        },
                    },
                },
                scales: {
                    x: {
                        grid: {
                            display: false,
                        },
                    },
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 5,
                        },
                    },
                },
            },
        });
    }

}