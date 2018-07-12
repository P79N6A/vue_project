import { Line } from "vue-chartjs"

export default {
    extends: Line,
    mounted() {
        this.renderChart({
            labels: ["Mon", "Tue", "Wed", "Thu", "Fri"],
            datasets: [
                {
                    borderColor: "#00B545",
                    lineTension: 0,
                    data: [17, 23, 32, 24, 27]
                }
            ],
        }, {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: "New Customers"
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