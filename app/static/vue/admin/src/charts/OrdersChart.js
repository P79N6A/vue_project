import { Line } from "vue-chartjs"

export default {
    extends: Line,
    mounted() {
        this.renderChart({
            labels: ["Mon", "Tue", "Wed", "Thu", "Fri"],
            datasets: [
                {
                    borderColor: "#555555",
                    lineTension: 0,
                    data: [63, 85, 55, 70, 113]
                }
            ]
        }, {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: "New Orders"
            },
            legend: {
                display: false
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        })
    }
}