<template>
    <div class="crud-popup">
        <h5 class="crud-popup__id">
            {{ crudData|ifExists("id") }}
        </h5>
        <h3 class="crud-popup__banner">
            {{ crudData|ifExists("name") }}
        </h3>
        <span @click="hideCrud" class="crud-popup__close">
            X
        </span>
        <form id="crud_form" @submit.prevent="onSubmit" class="crud-popup__form">
            <span class="crud-popup__error" v-if="errors.any()">
                {{ errors.all()[0] }}
            </span>
            <div v-for="currentField in fieldOrder" class="crud-popup__form-group">
                <template v-if="crudData['fields'][currentField].type === 'string'">
                    <label class="crud-popup__form-group-label">
                        {{ crudData["fields"][currentField].label }}
                    </label>
                    <input 
                        type="text" 
                        class="crud-popup__form-group-input" 
                        :name="currentField" 
                        :data-original="crudData['fields'][currentField].value" 
                        @keyup="dirtyDetector" 
                        autocomplete="off" 
                        v-validate.disable="{required: isRequired(crudData['fields'][currentField])}"
                        :class="{ dirty: crudData['fields'][currentField].dirty }"  
                    />
                </template>
                <template v-if="crudData['fields'][currentField].type === 'timestamp'">
                    <label class="crud-popup__form-group-label">
                        {{ crudData["fields"][currentField].label }}
                    </label>
                    <input 
                        type="text" 
                        class="crud-popup__form-group-input" 
                        :name="currentField" 
                        :data-original="crudData['fields'][currentField].value" 
                        @keyup="dirtyDetector" 
                        autocomplete="off" 
                        v-validate.disable="{required: isRequired(crudData['fields'][currentField])}" 
                        :class="{ dirty: crudData['fields'][currentField].dirty }" 
                    />
                </template>
                <template v-else-if="crudData['fields'][currentField].type === 'integer'">
                    <label class="crud-popup__form-group-label">
                        {{ crudData["fields"][currentField].label }}
                    </label>
                    <input 
                        type="text" 
                        class="crud-popup__form-group-input" 
                        :name="currentField" 
                        :data-original="crudData['fields'][currentField].value" 
                        @keyup="dirtyDetector" 
                        autocomplete="off" 
                        v-validate.disable="{required: isRequired(crudData['fields'][currentField])}" 
                        :class="{ dirty: crudData['fields'][currentField].dirty }" 
                    />
                </template>
                <template v-else-if="crudData['fields'][currentField].type === 'decimal'">
                    <label class="crud-popup__form-group-label">
                        {{ crudData["fields"][currentField].label }}
                    </label>
                    <input 
                        type="text" 
                        class="crud-popup__form-group-input" 
                        :name="currentField" 
                        :data-original="crudData['fields'][currentField].value" 
                        @keyup="dirtyDetector" 
                        autocomplete="off" 
                        v-validate.disable="{required: isRequired(crudData['fields'][currentField])}" 
                        :class="{ dirty: crudData['fields'][currentField].dirty }" 
                    />
                </template>
                <template v-else-if="crudData['fields'][currentField].type === 'select'">
                    <label class="crud-popup__form-group-label">
                        {{ crudData["fields"][currentField].label }}
                    </label>
                    <select 
                        :name="crudData['fields'][currentField].selectName" 
                        :data-original="crudData['fields'][currentField].value" 
                        @change="dirtyDetector" 
                        class="crud-popup__form-group-select" 
                        v-validate.disable="{required: isRequired(crudData['fields'][currentField])}" 
                        :class="{ dirty: crudData['fields'][currentField].dirty }" 
                    >
                        <option v-for="crudOption in crudData['fields'][currentField].selects" :value="crudOption[0]">
                            {{ crudOption[1] }}
                        </option>
                    </select>
                </template>
                <template v-else-if="crudData['fields'][currentField].type === 'multiselect'">
                    <label class="crud-popup__form-group-label crud-popup__form-group-label--multiselect">
                        {{ crudData["fields"][currentField].label }}
                    </label>
                    <select 
                        :name="crudData['fields'][currentField].selectName" 
                        class="crud-popup__form-group-select" 
                        @change="dirtyDetector" 
                        v-model="crudData['fields'][currentField].value" 
                        multiple 
                        v-validate.disable="{required: isRequired(crudData['fields'][currentField])}" 
                        :class="{ dirty: crudData['fields'][currentField].dirty }" 
                    >
                        <option v-for="crudOption in crudData['fields'][currentField].selects" :value="crudOption[0]">
                            {{ crudOption[1] }}
                        </option>
                    </select>
                </template>
                <template v-else-if="crudData['fields'][currentField].type === 'image_name'">
                    <p class="crud-popup__image-name">
                        {{ crudData["fields"][currentField].value }}
                    </p>
                </template>
                <template v-else-if="crudData['fields'][currentField].type === 'image'">
                    <img v-if="crudData['fields'][currentField].value" :src="crudData['fields'][currentField].value" class="crud-popup__image" alt="product image" />
                    <input 
                        type="file" 
                        @change="onFileChanged" 
                        name="crudImage" 
                        id="crudImage" 
                        class="crud-popup__image-input" 
                        v-validate.disable="'size:1000'" 
                    />
                    <label for="crudImage" class="crud-popup__image-label">
                        Add/Edit Image
                    </label>
                    &nbsp;
                </template>
            </div>
            <div class="crud-popup__form-group" v-if="showSave">
                <button type="button" @click="saveCrud" class="crud-popup__button">
                    Save
                </button>
            </div>
            <div class="crud-popup__form-group" v-if="showDelete">
                <button type="button" @click="deleteCrud" class="crud-popup__button">
                    {{ this.$store.state.global.deleteLabel }}
                </button>
            </div>
            <div class="crud-popup__form-group" v-if="showUndelete">
                <button type="button" @click="undeleteCrud" class="crud-popup__button">
                    {{ this.$store.state.global.undeleteLabel }}
                </button>
            </div>
            <div v-if="reviewDataLength > 0 && idExists" class="crud-popup__form-group crud-popup__form-group-table">
                <h4 class="crud-popup__review-header">
                    Reviews
                </h4>
                <table class="crud-popup__review-table">
                    <tr>
                        <th class="crud-popup__review-table-header">Product Name</th>
                        <th class="crud-popup__review-table-header">Rating</th>
                        <th class="crud-popup__review-table-header">Review</th>
                        <th class="crud-popup__review-table-header">Shown</th>
                    </tr>
                    <tr v-for="row in reviewData">
                        <td class="crud-popup__review-table-data">{{ row.product_name }}</td>
                        <td class="crud-popup__review-table-data">{{ row.rating }}</td>
                        <td class="crud-popup__review-table-data">{{ row.review_truncated }}</td>
                        <td class="crud-popup__review-table-data">
                            <input 
                                type="checkbox" 
                                @click="toggleReview(row, $event)" 
                                :checked="row.shown" 
                            />
                        </td>
                    </tr>
                </table>
            </div>
        </form>
    </div>
</template>

<script>
import { bus } from "../main"
import axios from "../../node_modules/axios"

export default {
    props: ["crudData", "reviewData"],
    data() {
        return {
            modifiedObject: {}
        }
    },
    methods: {
        hideCrud: function() {
            this.errors.clear();
            this.$nextTick(() => this.$validator.reset())
            bus.$emit("hideCrud");
        },
        dirtyDetector: function(event) {
            // Don't use .value for multiselects.
            if (event.target.tagName === "SELECT" && event.target.multiple === true) {
                let selectedList = [];
                for (var i=0; i<event.target.options.length; i++) {
                    let currentOption = event.target.options[i];

                    if (currentOption.selected) {
                        selectedList.push(currentOption.value);
                    }
                }

                this.modifiedObject[event.target.name] = selectedList;
            } else {
                let key = event.target.name;
                let originalValue = event.target.dataset.original;
                let newValue = event.target.value;
                let isDirty = originalValue !== newValue;
                if (isDirty) {
                    this.modifiedObject[key] = newValue;
                } else {
                    delete this.modifiedObject[key];
                }
            }

            this.updateDirtyFields();
        },
        updateDirtyFields: function() {
            // Iterates through and sets the .dirty attribute on modified data for conditional classes.
            for (var field in this.crudData.fields) {
                if (this.crudData.fields.hasOwnProperty(field)) {
                    let name = field;
                    if (this.crudData.fields[field].hasOwnProperty("selectName")) {
                        name = this.crudData.fields[field].selectName;
                    }
                    if (this.modifiedObject.hasOwnProperty(name)) {
                        this.crudData.fields[field].dirty = true;
                    } else {
                        this.crudData.fields[field].dirty = false;
                    }
                }
            }
        },
        onFileChanged: function(event) {
            let reader = new FileReader();
            let self = this;
            console.log(event.target);
            let image_element = event.target.previousElementSibling;

            reader.addEventListener("load", function() {
                let fileData = reader.result;
                console.log("!");
                if (image_element) {
                    console.log("@");
                    image_element.src = fileData;
                }
                self.modifiedObject["image"] = {
                    "file": fileData,
                    "name": event.target.files[0]["name"]
                }
            }, false);

            if (event.target.files[0]) {
                reader.readAsDataURL(event.target.files[0]);
            }
        },
        saveCrud: function(event) {
            this.$validator.validateAll().then(result => {
                if (this.errors.any()) {
                    return;
                }

                if (this.crudData.hasOwnProperty("id")) {
                    this.modifiedObject["id"] = this.crudData["id"];
                }
                this.crudData.dirtyObject = this.modifiedObject;
                this.crudData.isDirty = true;

                bus.$emit("saveCrud", this.crudData);
                this.errors.clear();
                this.$nextTick(() => this.$validator.reset())
            });
        },
        deleteCrud: function(event) {
            // "delete" parameter that is eventually passed as a POST argument is
            // to be interpreted by the flask route and handled according to the
            // model. Most deletes are soft.
            if (this.crudData.hasOwnProperty("id")) {
                this.modifiedObject["id"] = this.crudData["id"];
                this.modifiedObject["delete"] = true;
                this.crudData.dirtyObject = this.modifiedObject;
                bus.$emit("saveCrud", this.crudData);
            } else {
                bus.$emit("hideCrud");
            }
        },
        undeleteCrud: function(event) {
            // Toggles soft delete. "delete" property is handled on server side
            // according to the object being modified.
            if (this.crudData.hasOwnProperty("id")) {
                this.modifiedObject["id"] = this.crudData["id"];
                this.modifiedObject["delete"] = false;
                this.crudData.dirtyObject = this.modifiedObject;
                bus.$emit("saveCrud", this.crudData);
            } else {
                bus.$emit("hideCrud");
            }
        },
        toggleReview: function(row, event) {
            // This is done async and doesn't wait for a save.
            let rowId = row.id;

            bus.$emit("showLoading", "Contacting Server");
            axios.post("/toggle_review/", {
                id: rowId
            }).then((response) => {
                ;
            }).catch((error) => {
                bus.$emit("showWarning", error.response.data);
            }).finally(() => {
                bus.$emit("hideLoading");
            });
        },
        isRequired: function(rowInfo) {
            if (rowInfo.hasOwnProperty("validators") && rowInfo.validators.hasOwnProperty("required") && rowInfo.validators.required === true) {
                return true;
            } else {
                return false;
            }
        }
    },
    computed: {
        fieldOrder: function() {
            // Sets the fieldOrder array based off of the schema json.
            // This does lead to long dictionary calls in the template, however.
            // Future versions of the data structure will probably avoid this.
            if (this.crudData === null || this.crudData === undefined) {
                return [];
            } else {
                let resultsArray = Object.keys(
                    this.crudData.fields
                ).sort(function(a, b) {
                    return b.order > a.order;
                });
                return resultsArray;
            }
        },
        reviewDataLength: function() {
            return this.reviewData.length;
        },
        idExists: function() {
            return this.crudData.hasOwnProperty("id") && this.crudData["id"] !== null;
        },
        showSave: function() {
            if (this.crudData !== null) {
                return (this.crudData.hasOwnProperty("id") && this.crudData["id"] !== null && this.$store.state.global.hasEdit === true) || ((!this.crudData.hasOwnProperty("id") || this.crudData["id"] === null) && this.$store.state.table.hasNew === true)
            } else {
                return false
            }
        },
        showDelete: function() {
            if (this.crudData !== null && this.$store.state.global.hasDelete && this.crudData.id && this.crudData.id !== null) {
                if (this.crudData.viewObject === "CategoryView" && this.crudData.tableRowValues[3] === "") {
                    return true;
                }
                if (this.crudData.viewObject === "SaleView" && this.crudData.tableRowValues[4] === "") {
                    return true;
                }
            }

            return false;
        },
        showUndelete: function() {
            if (this.crudData !== null && this.$store.state.global.hasUndelete && !this.showDelete && this.crudData.id && this.crudData.id !== null) {
                return true;
            } else {
                return false;
            }
        }
    },
    filters: {
        ifExists: function(base, value) {
            try {
                return base[value] === null && value === "name" ? "New" : base[value];
            } catch(err) {
                return "New";
            }
        }
    },
    watch: {
        crudData: function() {
            this.modifiedObject = {}
        }
    },
    created() {
        bus.$on("resetValues", () => {
            this.errors.clear();
            this.$nextTick(() => this.$validator.reset())

            // Nasty hack to get around v-validate resetting :value from crudData
            this.$nextTick(function() {
                try {
                    let currentForm = document.getElementById("crud_form");
                    let nameObj = {};
                    for (var field in this.crudData.fields) {
                        if (this.crudData.fields[field].hasOwnProperty("selectName")) {
                            nameObj[this.crudData.fields[field].selectName] = field;
                        } else {
                            nameObj[field] = field;
                        }
                    }

                    for (var i=0; i<currentForm.length; i++) {
                        let currentInput = currentForm[i];
                        if (nameObj.hasOwnProperty(currentInput.name)) {
                            let currentField = this.crudData.fields[nameObj[currentInput.name]];
                            if (currentField.type !== "multiselect") {
                                if (this.crudData.id !== null) {
                                    currentInput.value = currentField.value;
                                } else {
                                    currentInput.value = "";
                                }
                            }
                        }
                    }
                } catch(err) {
                    ;
                }
            });
        });
    }
}
</script>

<style lang="scss">

.crud-popup {
    border: 2px solid #555555;
    width: 600px;
    height: 800px;
    position: fixed;
    top: 50px;
    background-color: white;
    left: calc(50vw - 300px);
    padding: 20px;
    overflow-y: scroll;

    @media screen and (max-height: 880px) {
        height: 600px;
    }
}

.crud-popup__banner {
    text-align: center;
    color: #00B545;
    font-size: 30px;
}

.crud-popup__id {
    position: absolute;
    left: 20px;
    top: 0;
    padding: 5px;
    color: #AAAAAA;
}

.crud-popup__close {
    position: absolute;
    cursor: pointer;
    right: 20px;
    top: 20px;
    padding: 5px;

    &:hover {
        color: #AAAAAA;
    }
}

.crud-popup__image-name {
    text-align: center;
}

.crud-popup__image {
    width: 200px;
    height: auto;
    display: block;
    margin-left: calc(50% - 100px);
    margin-bottom: 20px;
}

.crud-popup__button {
    font-size: 20px;
    height: 32px;
    border: 1px solid #CCCCCC;
    padding: 4px 10px;
    background-color: #CCCCCC;
    color: #333333;
    vertical-align: top;
    cursor: pointer;
    float: right;
    margin-bottom: 10px;
    margin-left: 20px;

    &:hover {
        background-color: #F3F3F3;
    }
}

.crud-popup__form {
    padding-top: 20px;
}

.crud-popup__form-group {
    width: 400px;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 30px;
    position: relative;
    min-height: 40px;
}

.crud-popup__form-group-table {
    width: 100%;
}

.crud-popup__review-header {
    text-align: center;
}

.crud-popup__review-table {
    border-top: 1px solid #EEEEEE;
    border-bottom: 1px solid #EEEEEE;
    border-collapse: collapse;

    .crud-popup__review-table-header, crud-popup__review-table-data {
        border-bottom: 1px solid #EEEEEE;
        padding: 8px 2px;
    }
}

.crud-popup__form-group-label {
    height: 20px;

    &.crud-popup__form-group-label--multiselect {
        margin-bottom: 93px;
        display: inline-block;
    }
}

.crud-popup__form-group-input {
    padding: 4px;
    border: 1px solid #F6F6F6;
    background-color: #FAFAFA;
    position: absolute;
    right: 0;

    &.dirty {
        border: 1px solid #FFD800;
    }
}

.crud-popup__form-group-select {
    position: absolute;
    right: 0;
    border: 1px solid #F6F6F6;
    background-color: #FAFAFA;

    &.dirty {
        border: 1px solid #FFD800;
    }
}

.crud-popup__image-input {
    display: none;
}

.crud-popup__image-label {
    cursor: pointer;
    padding: 8px 8px;
    border: 1px solid #CCCCCC;
    background-color: #F3F3F3;
    color: #333333;
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 129px;

    &:hover {
        background-color: #CCCCCC;
    }
}

.crud-popup__error {
    color: red;
    text-align: center;
    display: block;
    margin-bottom: 12px;
}

</style>