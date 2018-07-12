import { HorizontalBar } from "vue-chartjs"

export default {
    extends: HorizontalBar,
    mounted() {
        this.renderChart({
            labels: ["Today", "Quarter", "Year"],
            datasets: [
                {
                    backgroundColor: ["#0DC654", "#2DEF77", "#67fCA0"],
                    data: [1173, 23564, 24737]
                }
            ]
        }, {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: "Revenue ($)"
            },
            legend: {
                display: false
            }
        })
    }
}