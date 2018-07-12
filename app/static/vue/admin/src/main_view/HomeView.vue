<template>
    <div class="home-view">
        <div class="chart-row">
            <customers-chart class="chart"></customers-chart>
            <orders-chart class="chart"></orders-chart>
            <revenue-chart class="chart"></revenue-chart>
        </div>
        <div class="table-row">
            <h1 class="table-row__header">Recent Reviews</h1>
            <table class="table-row__table">
                <thead>
                    <tr>
                        <th class="table-row__table-header">ID</th>
                        <th class="table-row__table-header">Product</th>
                        <th class="table-row__table-header">Customer</th>
                        <th class="table-row__table-header">Rating</th>
                        <th class="table-row__table-header">Review</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="row in this.reviewData">
                        <td class="table-row__table-data">{{ row.id }}</td>
                        <td class="table-row__table-data">{{ row.product_name }}</td>
                        <td class="table-row__table-data">{{ row.customer_email }}</td>
                        <td class="table-row__table-data">{{ row.rating }}</td>
                        <td class="table-row__table-data">{{ row.review_truncated }}</td>
                    </tr>
                </tbody>
            </table>
            <button @click="changeView('Part')" class="table-row__button">
                View Products
            </button>
        </div>
        <div class="table-row">
            <h1 class="table-row__header">New Sales</h1>
            <table class="table-row__table">
                <thead>
                    <tr>
                        <th class="table-row__table-header">ID</th>
                        <th class="table-row__table-header">Product</th>
                        <th class="table-row__table-header">Price</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="row in this.saleData">
                        <td class="table-row__table-data">{{ row.id }}</td>
                        <td class="table-row__table-data">{{ row.product_name }}</td>
                        <td class="table-row__table-data">{{ row.price }}</td>
                    </tr>
                </tbody>
            </table>
            <button @click="changeView('Sales')" class="table-row__button">
                View Sales
            </button>
        </div>
        <!--
        <div>
            <button @click="showReports">Generate Reports</button>
        </div>
        <div v-if="reportsPopup" class="reports-popup">
            <iframe :src="preview" class="report-preview" />
            <div class="reports-popup__options">
                <h1>Reports</h1>
                <span @click="hideReports" class="reports-popup__close">X</span>
                <button 
                    class="reports-popup__button" 
                    @click="setReport('transactions')" 
                    :class="{ 'active': 'transactions' === currentReport }"
                >Transactions</button>
                <button 
                    class="reports-popup__button" 
                    @click="setReport('sales')" 
                    :class="{ 'active': 'sales' === currentReport }"
                >Sales</button>
                <button 
                    class="reports-popup__button" 
                    @click="generateReport"
                >Generate</button>
            </div>
        </div>
        -->
    </div>
</template>

<script>
import axios from "../../node_modules/axios"
//import html2canvas from "html2canvas"
//import jsPDF from "jspdf"

import { bus } from "../main"

import CustomersChart from "../charts/CustomersChart.js"
import OrdersChart from "../charts/OrdersChart.js"
import RevenueChart from "../charts/RevenueChart.js"

//window.html2canvas = html2canvas;

export default {
    components: {
        CustomersChart,
        OrdersChart,
        RevenueChart
    },
    data() {
        return {
            reviewData: [],
            saleData: [],
            reportsPopup: false,
            preview: null,
            currentReport: "transactions"
        }
    },
    methods: {
        changeView: function(destinationView) {
            bus.$emit("changeSidebarView", destinationView);
        }
        // Everything related to reports is commented out for now.
        // Removing the imports + code reduces file and compilation time by ~50%.
        // Ideally, this will be added back in once I find a solution to correctly
        // displaying HTML or I find a module where the default tables look acceptable.
        /**
        showReports: function() {
            this.reportsPopup = true;
        },
        hideReports: function() {
            this.reportsPopup = false;
        },
        setReport: function(reportName) {
            this.currentReport = reportName;
        },
        generateReport: function() {
            this.preview = null;

            if (this.currentReport === "sales") {
                this.generateSalesReport();
            } else if (this.currentReport === "transactions") {
                this.generateTransactionsReport();
            }
        },
        generateReportHTML: function(reportName, tableRows, headerList, attribList) {
            let source = document.createElement("DIV");
            source.style.height = "700px";
            source.style.width = "500px";
            source.style.backgroundColor = "black";

            let headerDiv = document.createElement("DIV");
            headerDiv.style.backgroundColor = "#00B545";
            headerDiv.style.color = "#FF0000";
            headerDiv.style.padding = "5px";
            headerDiv.style.textAlign = "center";
            headerDiv.style.fontSize = "24";
            headerDiv.style.width = "300px";
            let headerText = document.createTextNode(reportName);
            headerDiv.appendChild(headerText);

            let tableDiv = document.createElement("DIV");
            let table = document.createElement("TABLE");
            let headerRow = document.createElement("TR");
            for (var i=0; i<headerList.length; i++) {
                let currentHeader = headerList[i];
                let textNode = document.createTextNode(currentHeader);
                let headerNode = document.createElement("TH");
                headerNode.appendChild(textNode);
                headerRow.appendChild(headerNode);
            }
            table.appendChild(headerRow);

            for (var i=0; i<tableRows.length; i++) {
                let currentRow = tableRows[i];
                let rowNode = document.createElement("TR");
                for (var j=0; j<attribList.length; j++) {
                    let currentAttrib = attribList[j];
                    let textNode = document.createTextNode(currentRow[currentAttrib]);
                    let tdNode = document.createElement("TD");
                    tdNode.appendChild(textNode);
                    rowNode.appendChild(tdNode);
                }
                table.appendChild(rowNode);
            }

            tableDiv.appendChild(table);

            source.appendChild(headerDiv);
            source.appendChild(tableDiv);

            return source;
        },
        generateSalesReport: function() {
            bus.$emit("showLoading", "Contacting Server");
            axios.post("/query_sales/", {
                query: {
                    "search": "",
                    "sort_by": "date",
                    "offset": "0",
                    "limit": "10",
                    "active": true
                }
            }).then((response) => {
                let tableRows = response["data"]["result"]["query_result"];

                let doc = new jsPDF();

                let source = this.generateReportHTML(
                    "Sales",
                    tableRows,
                    ["ID", "Product", "Price"],
                    ["id", "product_name", "price"]
                );

                doc.addHTML(
                    source,
                    15,
                    15
                )

                this.preview = doc.output("datauristring");
            }).catch((error) => {
                bus.$emit("showWarning", error.response.data);
            }).finally(() => {
                bus.$emit("hideLoading");
            });
        },
        generateTransactionsReport: function() {
            bus.$emit("showLoading", "Contacting Server");
            axios.post("/query_transactions/", {
                query: {
                    "search": "",
                    "sort_by": "date",
                    "offset": "0",
                    "limit": "10",
                    "active": true
                }
            }).then((response) => {
                let tableRows = response["data"]["result"]["query_result"];

                let doc = new jsPDF();

                let source = this.generateReportHTML(
                    "Transactions",
                    tableRows,
                    ["ID", "Sale Product", "Sale Price"],
                    ["id", "sale_product", "sale_price"]
                );

                doc.addHTML(
                    source,
                    15,
                    15
                )

                this.preview = doc.output("datauristring");
            }).catch((error) => {
                bus.$emit("showWarning", error.response.data);
            }).finally(() => {
                bus.$emit("hideLoading");
            });
        }
        **/
    },
    created() {
        bus.$emit("showLoading", "Contacting Server");
        let reviewQuery = axios.post("/query_reviews/", {
            query: {
                "sort_by": "date",
                "offset": "0",
                "limit": "5"
            }
        })
        let salesQuery = axios.post("/query_sales/", {
            query: {
                "search": "",
                "sort_by": "date",
                "offset": "0",
                "limit": "5",
                "active": true
            }
        })
        Promise.all(
            [reviewQuery, salesQuery]
        ).then((response) => {
            this.reviewData = response[0]["data"]["result"]["query_result"];
            this.saleData = response[1]["data"]["result"]["query_result"];
        }).catch((error) => {
            bus.$emit("showWarning", error.response.data);
        }).finally(() => {
            bus.$emit("hideLoading");
        });
}
}
</script>

<style lang="scss">

.chart-row {
    width: 1210px;
    margin-left: auto;
    margin-right: auto;
    padding-top: 30px;

    @media screen and (max-width: 1500px) {
        width: 910px;
    }
}

.chart {
    width: 400px;
    height: 200px;
    display: inline-block;

    @media screen and (max-width: 1500px) {
        width: 300px;
        height: 150px;
    }
}

.table-row:last-of-type {
    @media screen and (max-height: 825px) {
        display: none;
    }
}

.table-row__header {
    text-align: center;
    font-size: 26px;
}

.table-row__table {
    margin-left: auto;
    margin-right: auto;
    border-collapse: collapse;
}

.table-row__button {
    margin-left: auto;
    margin-right: auto;
    display: block;
    margin-top: 8px;
    border: 1px solid #CCCCCC;
    background-color: #00B545;
    padding: 8px;
    width: 700px;
    cursor: pointer;
    color: #EEEEEE;

    &:hover {
        background-color: #2DEF77;
    }
}

.table-row__table-header, .table-row__table-data {
    padding: 4px 8px;

    &:last-child {
        @media screen and (max-width: 1380px) {
            display: none;
        }
    }
}

.table-row__table, .table-row__table-header, .table-row__table-data {
    border: 1px solid #CCCCCC;
}

.reports-popup {
    position: absolute;
    width: 800px;
    height: 600px;
    background-color: #CCCCCC;
    top: 100px;
    left: calc(50% - 400px);
    border: 1px solid #BBBBBB;
}

.report-preview {
    position: absolute;
    top: 0;
    left: 0;
    width: 50%;
    height: 100%;
}

.reports-popup__options {
    position: absolute;
    top: 0;
    right: 0;
    width: 50%;
    height: 100%;
}

.reports-popup__close {
    position: absolute;
    cursor: pointer;
    right: 0;
    top: 0;
    padding: 5px;
}

.reports-popup__button {
    width: 100%;
    height: 50px;
    background-color: white;
    
    &:last-of-type {
        position: absolute;
        bottom: 0;
    }

    &:hover {
        background-color: #EEEEEE;
    }

    &.active {
        background-color: #DDDDDD;
    }
}

</style>