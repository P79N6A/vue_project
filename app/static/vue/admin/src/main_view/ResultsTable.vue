<template>
    <div class="results-table">
        <!--
        <button 
            v-if="hasNew === true" 
            @click="showEmptyCrud" 
            class="results-table__button"
        >New</button>
        -->
        <table class="results-table__table">
            <thead>
                <tr>
                    <th 
                        v-for="header in tableHeaders" 
                        class="results-table__table-cell results-table__table-cell--columnHead"
                    >{{ header }}</th>
                    <th class="results-table__table-cell results-table__table-cell--columnHead"></th>
                </tr>
            </thead>
            <tbody>
                <tr 
                    v-for="(rowArray, rowIndex) in tableRows" 
                    class="results-table__table-row"
                    :class="{ dirty: isDirty(rowArray) }"
                >
                    <td 
                        v-for="tableData in rowArray" 
                        class="results-table__table-cell"
                    >{{ tableData }}</td>
                    <td class="results-table__table-cell">
                        <button 
                            class="results-table__button-cell"
                            @click="showCrud(rowIndex)" 
                        >{{ crudLabel }}</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <div class="results-table__pagination">
            <button 
                class="results-table__previous" 
                :class="{ 'active': hasPrev }" 
                @click="previous"
            >&lsaquo;</button>
            <button 
                class="results-table__next"  
                :class="{ 'active': hasNext }" 
                @click="next"
            >&rsaquo;</button>
        </div>
    </div>
</template>

<script>
import { bus } from "../main"

export default {
    props: ["resultsData"],
    data() {
        return {}
    },
    methods: {
        showEmptyCrud: function() {
            bus.$emit("emptyCrud");
            this.$nextTick(function() {
                bus.$emit("showCrud");
            });
        },
        showCrud: function(rowIndex) {
            bus.$emit("popCrud", this.$store.state.data.currentTable.result[rowIndex]);
            bus.$emit("showCrud");
        },
        previous: function() {
            if (this.$store.state.data.currentTable.hasPrev) {
                this.$store.commit("setQueryOffset", this.$store.state.query.queryOffset - 1);
                bus.$emit("runQuery");
            }
        },
        next: function() {
            if (this.$store.state.data.currentTable.hasNext) {
                this.$store.commit("setQueryOffset", this.$store.state.query.queryOffset + 1);
                bus.$emit("runQuery");
            }
        },
        isDirty: function(rowArray) {
            // ! NEED TO FIX !

            return false;


            return rowArray.hasOwnProperty("isDirty") && rowArray.isDirty === true;
        },
        sortTableRows: function(firstItem) {
            // Returns sorted list of properties from supplied item
            let sortedIndexes = Object.keys(
                    firstItem
            ).sort(function(a, b) {
                return firstItem[a]["order"] - firstItem[b]["order"];
            });

            let filteredIndexes = sortedIndexes.filter(function(currentValue) {
                return !(
                    [
                        "timestamp_deleted",
                        "address",
                        "zip_code",
                        "image",
                        "product_category_list",
                        "supplier_id",
                        "image_name",
                        "phone"
                    ].includes(currentValue)
                );
            });

            return filteredIndexes;
        }
    },
    computed: {
        hasNext: function() {
            return this.$store.state.data.currentTable.hasNext;
        },
        hasPrev: function() {
            return this.$store.state.data.currentTable.hasPrev;
        },
        crudLabel: function() {
            if (["Parts", "Suppliers"].includes(this.$store.state.global.shownView)) {
                return "Edit";
            } else {
                return "View";
            }
        },
        hasNew: function() {
            if (["Parts", "Suppliers", "Sales", "Categories"].includes(this.$store.state.global.shownView)) {
                return true;
            } else {
                return false;
            }
        },
        tableHeaders: function() {
            if (this.$store.state.data.currentTable.result.length == 0) {
                return [];
            } else {
                // Get sorted list of items
                let firstItem = this.$store.state.data.currentTable.result[0];
                let sortedIndexes = this.sortTableRows(firstItem);

                // Return array of headers
                let headerArray = [];
                for (var i=0; i<sortedIndexes.length; i++) {
                    headerArray.push(firstItem[sortedIndexes[i]]["label"]);
                }

                return headerArray;
            }
        },
        tableRows: function() {
            if (this.$store.state.data.currentTable.result.length == 0) {
                return [];
            } else {
                console.log(this.$store.state.data.currentTable.result);

                // Get sorted list of items
                let firstItem = this.$store.state.data.currentTable.result[0];
                let sortedIndexes = this.sortTableRows(firstItem);

                // Array of arrays of values
                let currentRows = [];
                for (var i=0; i<this.$store.state.data.currentTable.result.length; i++) {
                    let currentItem = this.$store.state.data.currentTable.result[i];
                    let rowList = [];
                    for (var j=0; j<sortedIndexes.length; j++) {
                        rowList.push(currentItem[sortedIndexes[j]]["value"]);
                    }
                    currentRows.push(rowList);
                }

                return currentRows;
            }
        }
    },
    created() {
        bus.$on("tableDataChange", ($event) => {
            // Change current table data
            let shownView = this.$store.state.global.shownView.toLowerCase();
            let currentTableData;

            /*
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
            */
        });
    }
}
</script>

<style lang="scss">

.results-table__banner {
    text-align: center;
}

.results-table__button {
    font-size: 20px;
    height: 32px;
    border: 1px solid #CCCCCC;
    padding: 4px 10px;
    background-color: #CCCCCC;
    vertical-align: top;
    cursor: pointer;
    float: right;
    margin-right: 18px;
    margin-bottom: 10px;
    color: #333333;

    &:hover {
        background-color: #F3F3F3;
    }
}

.results-table__table {
    width: calc(100% - 20px);
    border-collapse: collapse;
    margin: 10px;
}

.results-table__table-row {
    &.dirty {
        background-color: #FFF18C;
    }
}

.results-table__table-row:nth-child(even) {
    background-color: #EEEEEE;

    &.dirty {
        background-color: #FFEB60;
    }
}

.results-table__table-cell {
    padding: 2px 6px;
    max-width: 200px;
    overflow: hidden;

    &:last-child {
        padding: 0;
    }
}

.results-table__table-cell--columnHead {
    border: none;
    padding-top: 6px;
    padding-bottom: 6px;
    background-color: #B1EFC6;
}

.results-table__pagination {
    position: relative;
    padding: 10px 30px;
}

.results-table__next, .results-table__previous {
    border: 1px solid #CCCCCC;
    background-color: 1px solid #CCCCCC;
    color: #333333;
    padding: 6px 10px;
    font-size: 20px;
    cursor: not-allowed;

    &.active {
        background-color: #00b545;
        cursor: pointer;

        &:hover {
            background-color: #F3F3F3;
        }
    }
}

.results-table__next {
    position: absolute;
    right: 30px;
}

.results-table__button-cell {
    font-size: 14px;
    height: 20px;
    width: 100%;
    border: none;
    padding: 4px 10px;
    background-color: #CCCCCC;
    vertical-align: top;
    cursor: pointer;

    &:hover {
        background-color: #F3F3F3;
        border: 1px solid #CCCCCC;
        padding: 3px 9px;
    }
}

</style>