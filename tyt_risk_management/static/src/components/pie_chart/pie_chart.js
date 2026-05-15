/** @odoo-module */

import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";
import { Component, onWillStart, useRef, onMounted, onWillUnmount } from "@odoo/owl";

export class PieChart extends Component {
    static template = "tyt_risk_management.PieChart";
    static props = {
        label: String,
        data: Object,
        dataValues: Array,
        dataLabels: Array,
        dataColors: Array,
        showLegend: {
            type: Boolean,
            optional: true,
        }
    };

    static defaultProps = {
    showLegend: false,
  };

    setup() {
        this.canvasRef = useRef("canvas");
        //onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));
        onMounted(() => {
            this.renderChart();
        });
        onWillUnmount(() => {
            this.chart.destroy();
        });
    }

    renderChart() {
        const labels = this.props.dataLabels;
        const data = this.props.dataValues;
        const color = this.props.dataColors;
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.label,
                        data: data,
                        backgroundColor: color,
                    },
                ],
            },
            options: {
                plugins: {
                    legend: {
                        display: this.props.showLegend || false // Completely hides the legend
                    },
                    // tooltip: {
                    //         enabled: false // Oculta los cuadros de texto al pasar el mouse
                    //     }

                }
                
            }
        });
    }
}