<template>
    <div class="query-view">
        <h3 class="query-view__banner">
            {{ this.$store.state.global.shownView }} Query
        </h3>
        <form @submit.prevent="submitSearch" class="query-view__form">
            <input 
                type="text" 
                name="search" 
                placeholder="Search" 
                v-model="form.search" 
                class="query-view__form-input" 
                autocomplete="off" 
            />
            <button 
                @click="submitSearch" 
                type="button" 
                class="query-view__form-button" 
                ref="searchButton"
            >Search</button><br />
            <template v-for="querySelect in this.$store.state.query.queryFilters.selects">
                <label :for="querySelect.name">
                    {{ querySelect.label }}
                </label>
                <select :name="querySelect.name" class="query-view__form-select">
                    <option 
                        v-for="selectUnit in querySelect.selectVals" 
                        :value="selectUnit.value"
                    >{{ selectUnit.valueLabel }}</option>
                </select>
            </template>
            <template v-for="queryCheckbox in this.$store.state.query.queryFilters.checkboxes">
                <label :for="queryCheckbox.name">
                    {{ queryCheckbox.label }}
                </label>
                <input 
                    type="checkbox" 
                    :name="queryCheckbox.name" 
                    :value="queryCheckbox.name" 
                />
            </template>
            <label for="limit">Per Page</label>
            <select name="limit" class="query-view__form-select">
                <option value="10">10</option>
                <option value="20">20</option>
            </select>
        </form>
    </div>
</template>

<script>
import { bus } from "../main"

export default {
    data() {
        return {
            form: {
                search: ""
            }
        }
    },
    methods: {
        submitSearch(event) {
            let formObj = {};
            let queryForm = event.target.form || event.target;

            for (var i=0; i<queryForm.elements.length; i++) {
                let currentElement = queryForm.elements[i];
                if (currentElement.nodeName === "INPUT") {
                    switch (currentElement.type) {
                        case "file":
                        case "submit":
                        case "button":
                            break;
                        case "checkbox":
                        case "radio":
                            if (currentElement.checked) {
                                formObj[currentElement.name] = true;
                            } else {
                                formObj[currentElement.name] = false;
                            }
                            break;
                        default:
                            formObj[currentElement.name] = currentElement.value;
                            break;
                    }
                } else if (currentElement.nodeName === "TEXTAREA") {
                    formObj[currentElement.name] = currentElement.value;
                } else if (currentElement.nodeName === "SELECT") {
                    formObj[currentElement.name] = currentElement.value;
                }
            }

            formObj["offset"] = this.currentOffset;

            this.$parent.submitSearch(formObj);
        }
    },
    computed: {
        currentOffset: function() {
            return this.$store.state.query.queryOffset;
        }
    },
    created() {
        bus.$on("runQuery", ($event) => {
            let elem = this.$refs.searchButton;
            elem.click();
        });
    }
}
</script>

<style lang="scss">

.query-view {
    padding-bottom: 10px;
}

.query-view__banner {
    text-align: center;
}

.query-view__form {
    padding: 10px 20px;
}

.query-view__form-input {
    font-size: 20px;
    padding: 4px;
    border: 1px solid #F6F6F6;
    background-color: #FAFAFA;
    height: 32px;
    vertical-align: top;
}

.query-view__form-button {
    font-size: 20px;
    height: 32px;
    border: 1px solid #CCCCCC;
    padding: 4px 10px;
    background-color: #CCCCCC;
    margin-left: -5px;
    vertical-align: top;
    cursor: pointer;
    color: #333333;

    &:hover {
        background-color: #F3F3F3;
    }
}

.query-view__form-select {
    margin-top: 16px;
    background-color: #FAFAFA;
    border: 1px solid #F6F6F6;
}

</style>