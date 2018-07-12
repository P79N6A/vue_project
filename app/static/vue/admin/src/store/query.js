const state = {
    queryRoute: "",
    queryFilters: {},
    hasNext: false,
    hasPrev: false,
    queryOffset: 0
}

const mutations = {
    setQueryFilters: (state, filterObject) => {
        state.queryFilters = filterObject;
    },
    setQueryOffset: (state, offset) => {
        state.queryOffset = offset;
    },
    setHasNext: (state, hasNext) => {
        state.hasNext = hasNext;
    },
    setHasPrev: (state, hasPrev) => {
        state.hasPrev = hasPrev;
    },
    setQueryRoute: (state, queryRoute) => {
        state.queryRoute = queryRoute;
    },
    resetQuery: (state) => {
        state.queryOffset = 0;
        state.hasNext = false;
        state.hasPrev = false;
    }
}

export default {
    state,
    mutations
}