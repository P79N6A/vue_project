<template>
    <div>
        <top-nav></top-nav>
        <div class="app-view">
            <side-nav></side-nav>
            <div class="main-view">
                <div v-show="isCommonView === true">
                    <query-view></query-view>
                    <results-table :resultsData="resultsData"></results-table>
                    <crud-popup 
                        v-show="showCrud" 
                        :crudData="crudData" 
                        :reviewData="reviewData"
                    ></crud-popup>
                </div>
                <home-view v-show="this.$store.state.global.shownView == 'Home'"></home-view>
            </div>
        </div>
        <account-popup v-show="showAccountPopup"></account-popup>
        <warning-popup v-show="showWarningPopup"></warning-popup>
        <settings-popup v-show="showSettingsPopup"></settings-popup>
        <loading-popup v-show="showLoadingPopup"></loading-popup>
    </div>
</template>

<script>
import axios from "../../node_modules/axios"
import { bus } from "../main"
import SCHEMAS from "./schemas.json"
import TABLES from "./tables.json"

import SideNav from "../navs/SideNav.vue"
import TopNav from "../navs/TopNav.vue"
import AccountPopup from "../global/AccountPopup.vue"
import WarningPopup from "../global/WarningPopup.vue"
import SettingsPopup from "../global/SettingsPopup.vue"
import LoadingPopup from "../global/LoadingPopup.vue"
import HomeView from "../main_view/HomeView.vue"
import QueryView from "../main_view/QueryView.vue"
import ResultsTable from "../main_view/ResultsTable.vue"
import CrudPopup from "../main_view/CrudPopup.vue"

export default {
    name: "Dashboard",
    components: {
        SideNav,
        TopNav,
        AccountPopup,
        WarningPopup,
        SettingsPopup,
        LoadingPopup,
        HomeView,
        QueryView,
        ResultsTable,
        CrudPopup
    },
    data() {
        return {
            title: "Vue file",
            showAccountPopup: false,
            showWarningPopup: false,
            showSettingsPopup: false,
            showLoadingPopup: false,
            showCrud: false,
            resultsData: null,
            crudData: null,
            reviewData: [],
            SCHEMAS: SCHEMAS,
            TABLES: TABLES
        }
    },
    methods: {
        submitSearch(searchInput) {
            bus.$emit("showLoading", "Contacting Server");
            axios.post(this.$store.state.query.queryRoute, {
                query: searchInput
            }).then((response) => {
                this.$store.commit("setHasNext", response["data"]["result"]["has_next"]);
                this.$store.commit("setHasPrev", response["data"]["result"]["has_prev"]);
                this.resultsData = response["data"]["result"]["query_result"];
                this.$store.commit("clearCrudList");

                // Populate Crud list and set table row names
                this.populateCrudList();
            }).catch((error) => {
                bus.$emit("showWarning", error.response.data);
            }).finally(() => {
                bus.$emit("hideLoading");
            });
        },
        populateCrudList() {
            let shownView = this.$store.state.global.shownView;
            let tableInfo = TABLES[shownView];

            // Set crudSchema
            let crudSchema = SCHEMAS[shownView];

            this.$store.commit("setCrudSchema", crudSchema);

            // Construct resultsData from schema
            for (var i=0; i<this.resultsData.length; i++) {
                let currentData = this.resultsData[i];
                let crudObject = {};

                crudObject.viewObject = tableInfo["viewObject"];

                crudObject.id = currentData["id"];
                crudObject.name = currentData[tableInfo["nameValue"]];

                crudObject.fields = JSON.parse(JSON.stringify(crudSchema));

                // Iterate over crudSchema and replace relevant values
                // Also initialize dirty attribute
                for (var key in crudObject.fields) {
                    if (crudObject.fields.hasOwnProperty(key)) {
                        if (shownView === "Part" && key === "supplier_list") {
                            crudObject.fields["supplier_list"].value = currentData["supplier_id"];
                            crudObject.fields["supplier_list"].selects = currentData["supplier_list"]; 
                        } else if (shownView === "Part" && key === "categories") {
                            crudObject.fields["categories"].value = currentData["product_category_list"];
                            crudObject.fields["categories"].selects = currentData["category_list"]; 
                        } else {
                            crudObject.fields[key].value = currentData[key];
                        }

                        crudObject.fields[key].dirty = false;
                    }
                }

                crudObject.tableRowValues = [];
                let keyOrder = tableInfo["tableKeys"];
                for (var j=0; j<keyOrder.length; j++) {
                    crudObject.tableRowValues.push(currentData[keyOrder[j]]);
                }

                crudObject.dirtyObject = {};

                this.$store.commit("pushCrud", crudObject);
            }

            // set table row names
            this.$store.commit("setTableRowNames", tableInfo["tableRowNames"]);
        },
        emptyCrud(shownView, replaceObj={}) {
            let tableInfo = TABLES[shownView];

            // new empty object mapping
            let crudObject = {};

            crudObject.id = null;
            crudObject.name = null;

            crudObject.viewObject = tableInfo["viewObject"];

            crudObject.fields = JSON.parse(JSON.stringify(this.$store.state.table.crudSchema));

            // Iterate over fields and adjust necessary values
            for (var key in crudObject.fields) {
                if (crudObject.fields.hasOwnProperty(key)) {
                    if (replaceObj.hasOwnProperty(key)) {
                        for (var replacementKey in replaceObj[key]) {
                            crudObject.fields[key][replacementKey] = replaceObj[key][replacementKey];
                        }
                    } else {
                        if (crudObject.fields[key].type === "multiselect") {
                            crudObject.fields[key].value = [];
                        } else {
                            crudObject.fields[key].value = "";
                        }
                    }
                }
            }

            crudObject.tableRowValues = [];
            crudObject.dirtyObject = {};

            this.crudData = crudObject;
        }
    },
    computed: {
        isCommonView: function() {
            return ["Part", "Supplier", "Transactions", "Customers", "Sales", "Categories"].includes(this.$store.state.global.shownView);
        }
    },
    beforeCreate() {
        axios.post("/get_employee_info/").then((response) => {
            this.$store.commit("setAccountObj", response.data.result);
        });
    },
    created() {
        bus.$on("mainViewChange", (data) => {
            let shownView = data;
            let tableInfo = TABLES[shownView];

            this.$store.commit("setShownView", data);

            if (["Part", "Supplier", "Transactions", "Sales", "Customers", "Categories"].includes(data)) {
                // clear old info
                this.$store.commit("clearCrudList");
                this.$store.commit("setTableRowNames", []);

                // apply query filter and button statuses
                let queryFilter = {};
                if (tableInfo.hasOwnProperty("selects")) {
                    queryFilter["selects"] = tableInfo["selects"];
                }
                if (tableInfo.hasOwnProperty("checkboxes")) {
                    queryFilter["checkboxes"] = tableInfo["checkboxes"];
                }

                this.$store.commit("setQueryFilters", queryFilter);
                this.$store.commit("setCrudLabel", tableInfo["crudLabel"]);
                this.$store.commit("setHasNew", tableInfo["hasNew"]);
                this.$store.commit("setHasEdit", tableInfo["hasEdit"]);
                this.$store.commit("resetQuery");
                this.$store.commit("setHasDelete", tableInfo["hasDelete"]);
                this.$store.commit("setDeleteLabel", tableInfo["deleteLabel"]);
                this.$store.commit("setHasUndelete", tableInfo["hasUndelete"]);
                this.$store.commit("setUndeleteLabel", tableInfo["undeleteLabel"]);
                this.$store.commit("setQueryRoute", tableInfo["queryRoute"]);

                this.$nextTick(function() {
                    bus.$emit("runQuery");
                });
            }
        });
        bus.$on("emptyCrud", () => {
            let shownView = this.$store.state.global.shownView;

            // Pass either shownview or shownview + ajax result to emptycrud method
            if (shownView === "Part") {
                bus.$emit("showLoading", "Contacting Server");
                let supplierQuery = axios.post("/get_supplier_list/");
                let categoryQuery = axios.post("/get_category_list/");

                Promise.all(
                    [supplierQuery, categoryQuery]
                ).then((response) => {
                    let supplierList = response[0].data.result;
                    let categoryList = response[1].data.result;
                    this.emptyCrud(shownView, {
                        "supplier_list": {
                            "selects": supplierList
                        },
                        "categories": {
                            "selects": categoryList
                        }
                    });
                }).catch((error) => {
                    bus.$emit("showWarning", error.response.data);
                }).finally(() => {
                    bus.$emit("hideLoading");
                });
            } else if (shownView === "Sales") {
                bus.$emit("showLoading", "Contacting Server");
                axios.post("/get_part_list/").then((response) => {
                    let partList = response.data.result;
                    this.emptyCrud(shownView, {
                        "product_name": {
                            "selects": partList,
                            "type": "select",
                            "selectName": "product_id"
                        }
                    });
                }).catch((error) => {
                    bus.$emit("showWarning", error.response.data);
                }).finally(() => {
                    bus.$emit("hideLoading");
                });
            } else {
                this.emptyCrud(shownView);
            }
        });
        bus.$on("saveCrud", (crudData) => {
            let shownView = this.$store.state.global.shownView;
            let tableInfo = TABLES[shownView];

            this.showCrud = false;

            bus.$emit("showLoading", "Contacting Server");
            axios.post(tableInfo["saveRoute"], {
                modifications: crudData.dirtyObject
            }).then((response) => {
                if (crudData.dirtyObject.id !== null) {
                    // Update crudObject
                    for (var key in crudData.dirtyObject) {
                        if (crudData.dirtyObject.hasOwnProperty(key) || key === "image") {
                            // Handle id and name
                            if (key === "id") {
                                crudData.id = crudData.dirtyObject["id"];
                            } else if (key === "name") {
                                crudData.name = crudData.dirtyObject["name"];
                            } else if (key === "image") {
                                crudData.fields["image"].value = crudData.dirtyObject["image"]["file"];
                                crudData.fields["image_name"].value = crudData.dirtyObject["image"]["name"];
                            } else if (key === "supplier_id") {
                                crudData.fields["supplier_list"].value = crudData.dirtyObject["supplier_id"];
                            }

                            // Handle fields
                            if (crudData.fields.hasOwnProperty(key) && key !== "image") {
                                crudData.fields[key].value = crudData.dirtyObject[key];
                            }

                            // Handle row values
                            let keyOrder = tableInfo["tableKeys"];
                            crudData.tableRowValues = [];
                            let currentData = response.data.result;
                            for (var j=0; j<keyOrder.length; j++) {
                                crudData.tableRowValues.push(currentData[keyOrder[j]]);
                            }
                        }
                    }

                    crudData.dirtyObject = {};
                } else {
                    // Add new item to crudList
                    let currentData = response.data.result;
                    let crudObject = {};

                    crudObject.id = currentData["id"];
                    crudObject.name = currentData[tableInfo["nameValue"]];

                    crudObject.viewObject = tableInfo["viewObject"];

                    crudObject.fields = JSON.parse(JSON.stringify(this.$store.state.table.crudSchema));

                    // Iterate over crudSchema and replace relevant values
                    for (var key in crudObject.fields) {
                        if (crudObject.fields.hasOwnProperty(key)) {
                            if (shownView === "Part" && key === "supplier_list") {
                                crudObject.fields["supplier_list"].value = currentData["supplier_id"];
                                crudObject.fields["supplier_list"].selects = currentData["supplier_list"]; 
                            } else {
                                crudObject.fields[key].value = currentData[key];
                            }
                        }
                    }

                    crudObject.tableRowValues = [];
                    let keyOrder = tableInfo["tableKeys"];
                    for (var j=0; j<keyOrder.length; j++) {
                        crudObject.tableRowValues.push(currentData[keyOrder[j]]);
                    }

                    crudObject.dirtyObject = {};

                    this.$store.commit("pushCrud", crudObject);
                }
            }).catch((error) => {
                bus.$emit("showWarning", error.response.data);
            }).finally(() => {
                bus.$emit("hideLoading");
            });
        });
        bus.$on("hideAccount", () => {
            this.showAccountPopup = false;
        });
        bus.$on("showAccount", () => {
            this.showAccountPopup = true;
        });
        bus.$on("hideWarning", () => {
            this.showWarningPopup = false;
            this.$store.commit("setWarningText", "");
        });
        bus.$on("showWarning", (warningMessage) => {
            this.$store.commit("setWarningText", warningMessage);
            this.showWarningPopup = true;
        });
        bus.$on("hideSettings", () => {
            this.showSettingsPopup = false;
        });
        bus.$on("showSettings", () => {
            this.showSettingsPopup = true;
        });
        bus.$on("hideLoading", () => {
            this.showLoadingPopup = false;
            this.$store.commit("setLoadingMessage", "");
        });
        bus.$on("showLoading", (loadingMessage) => {
            this.$store.commit("setLoadingMessage", loadingMessage);
            this.showLoadingPopup = true;
        });
        bus.$on("popCrud", (crudData) => {
            this.crudData = crudData;
        });
        bus.$on("showCrud", () => {
            let shownView = this.$store.state.global.shownView;

            // Get Reviews for Part and Customers
            if ((shownView === "Part" || shownView === "Customers") && this.crudData !== null && this.crudData.id !== null) {
                let queryObj = {
                    "sort_by": "date",
                    "offset": "0",
                    "limit": "100"
                }
                if (shownView === "Part") {
                    queryObj["product_id"] = this.crudData.id;
                } else if (shownView === "Customers") {
                    queryObj["customer_id"] = this.crudData.id;
                }
                bus.$emit("showLoading", "Contacting Server");
                axios.post("/query_reviews/", {
                    query: queryObj
                }).then((response) => {
                    this.reviewData = response["data"]["result"]["query_result"];
                    this.showCrud = true;
                    bus.$emit("resetValues");
                }).catch((error) => {
                    bus.$emit("showWarning", error.response.data);
                }).finally(() => {
                    bus.$emit("hideLoading");
                }); 
            } else {
                this.reviewData = [];
                this.showCrud = true;
                bus.$emit("resetValues");
            }
        });
        bus.$on("hideCrud", () => {
            this.showCrud = false;
        });
    }
}
</script>

<style lang="scss">

* {
    box-sizing: border-box;
    font-family: 'Martel Sans', sans-serif;
    font-weight: 200;
}

.app-view {
    display: flex;
}

.main-view {
    height: calc(100vh - 36px);
    width: 100%;
}

</style>
