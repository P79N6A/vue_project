const state = {
    tableRowNames: [],
    crudList: [],
    hasNew: false,
    crudLabel: "",
    crudSchema: {}
}

const mutations = {
    pushCrud: (state, crud) => {
        state.crudList.push(crud);
    },
    clearCrudList: (state) => {
        state.crudList = [];
    },
    setTableRowNames: (state, rowArray) => {
        state.tableRowNames = rowArray;
    },
    setCrudLabel: (state, crudLabel) => {
        state.crudLabel = crudLabel;
    },
    setHasNew: (state, hasNew) => {
        state.hasNew = hasNew;
    },
    setCrudSchema: (state, crudSchema) => {
        state.crudSchema = crudSchema;
    }
}

export default {
    state,
    mutations
}