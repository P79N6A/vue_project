const state = {
    shownView: "Home",
    accountObj: {},
    hasEdit: false,
    hasDelete: false,
    deleteLabel: "",
    hasUndelete: false,
    undeleteLabel: "",
    warningText: "",
    loadingMessage: ""
}

const mutations = {
    setAccountObj: (state, accountObj) => {
        state.accountObj = accountObj;
    },
    setShownView: (state, viewString) => {
        state.shownView = viewString;
    },
    setHasEdit: (state, hasEdit) => {
        state.hasEdit = hasEdit;
    },
    setHasDelete: (state, hasDelete) => {
        state.hasDelete = hasDelete;
    },
    setDeleteLabel: (state, deleteLabel) => {
        state.deleteLabel = deleteLabel;
    },
    setHasUndelete: (state, hasUndelete) => {
        state.hasUndelete = hasUndelete;
    },
    setUndeleteLabel: (state, undeleteLabel) => {
        state.undeleteLabel = undeleteLabel;
    },
    setWarningText: (state, warningText) => {
        state.warningText = warningText;
    },
    setLoadingMessage: (state, loadingMessage) => {
        state.loadingMessage = loadingMessage;
    }
}

export default {
    state,
    mutations
}