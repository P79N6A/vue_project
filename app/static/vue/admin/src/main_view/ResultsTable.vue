<template>
    <div class="results-table">
        <button 
            v-if="this.$store.state.table.hasNew === true" 
            @click="showEmptyCrud" 
            class="results-table__button"
        >New</button>
        <table class="results-table__table">
            <thead>
                <tr>
                    <th 
                        v-for="header in this.$store.state.table.tableRowNames" 
                        class="results-table__table-cell results-table__table-cell--columnHead"
                    >{{ header }}</th>
                    <th class="results-table__table-cell results-table__table-cell--columnHead"></th>
                </tr>
            </thead>
            <tbody>
                <tr 
                    v-for="rowArray in this.$store.state.table.crudList" 
                    class="results-table__table-row"
                    :class="{ dirty: isDirty(rowArray) }"
                >
                    <td 
                        v-for="tableData in rowArray.tableRowValues" 
                        class="results-table__table-cell"
                    >{{ tableData }}</td>
                    <td class="results-table__table-cell">
                        <button 
                            @click="showCrud(rowArray)" 
                            class="results-table__button-cell"
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
        showCrud: function(rowArray) {
            bus.$emit("popCrud", rowArray);
            bus.$emit("showCrud");
        },
        previous: function() {
            if (this.$store.state.query.hasPrev) {
                this.$store.commit("setQueryOffset", this.$store.state.query.queryOffset - 1);
                bus.$emit("runQuery");
            }
        },
        next: function() {
            if (this.$store.state.query.hasNext) {
                this.$store.commit("setQueryOffset", this.$store.state.query.queryOffset + 1);
                bus.$emit("runQuery");
            }
        },
        isDirty: function(rowArray) {
            return rowArray.hasOwnProperty("isDirty") && rowArray.isDirty === true;
        }
    },
    computed: {
        tableHeaders: function() {
            if (this.resultsData === null || this.resultsData === undefined) {
                return [];
            } else {
                let resultsArray = Object.keys(this.resultsData[0]);

                return resultsArray;
            }
        },
        tableArray: function() {
            if (this.resultsData === null || this.resultsData === undefined) {
                return [];
            } else {
                // Uses this.tableHeaders as keys for each row in this.resultsData
                let resultsArray = []
                for (var i=0; i<this.resultsData.length; i++) {
                    let subArray = [];
                    for (var j=0; j<this.tableHeaders.length; j++) {
                        subArray.push(this.resultsData[i][this.tableHeaders[j]]);
                    }
                    resultsArray.push(subArray);
                }

                return resultsArray;
            }
        },
        hasNext: function() {
            return this.$store.state.query.hasNext;
        },
        hasPrev: function() {
            return this.$store.state.query.hasPrev;
        },
        crudLabel: function() {
            return this.$store.state.table.crudLabel;
        }
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