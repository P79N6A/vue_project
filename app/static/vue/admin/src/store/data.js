import axios from "../../node_modules/axios"
import { bus } from "../main"

const state = {
    parts: {
        hasNext: false,
        hasPrev: false,
        result: []
    },
    suppliers: {
        hasNext: false,
        hasPrev: false,
        result: []
    },
    transactions: {
        hasNext: false,
        hasPrev: false,
        result: []
    },
    customers: {
        hasNext: false,
        hasPrev: false,
        result: []
    },
    sales: {
        hasNext: false,
        hasPrev: false,
        result: []
    },
    categories: {
        hasNext: false,
        hasPrev: false,
        result: []
    },
    reviews: {
        hasNext: false,
        hasPrev: false,
        result: []
    },
    currentTable: {
        hasNext: false,
        hasPrev: false,
        result: []
    }
}

const mutations = {
    setParts: (state, payload) => {
        state.parts.hasNext = payload.data.result.has_next;
        state.parts.hasPrev = payload.data.result.has_prev;
        state.parts.result = payload.data.result.query_result;

        state.currentTable.hasNext = payload.data.result.has_next;
        state.currentTable.hasPrev = payload.data.result.has_prev;
        state.currentTable.result = payload.data.result.query_result;
    },
    setSuppliers: (state, payload) => {
        state.suppliers.hasNext = payload.data.result.has_next;
        state.suppliers.hasPrev = payload.data.result.has_prev;
        state.suppliers.result = payload.data.result.query_result;

        state.currentTable.hasNext = payload.data.result.has_next;
        state.currentTable.hasPrev = payload.data.result.has_prev;
        state.currentTable.result = payload.data.result.query_result;
    },
    setTransactions: (state, payload) => {
        state.transactions.hasNext = payload.data.result.has_next;
        state.transactions.hasPrev = payload.data.result.has_prev;
        state.transactions.result = payload.data.result.query_result;

        state.currentTable.hasNext = payload.data.result.has_next;
        state.currentTable.hasPrev = payload.data.result.has_prev;
        state.currentTable.result = payload.data.result.query_result;
    },
    setCustomers: (state, payload) => {
        state.customers.hasNext = payload.data.result.has_next;
        state.customers.hasPrev = payload.data.result.has_prev;
        state.customers.result = payload.data.result.query_result;

        state.currentTable.hasNext = payload.data.result.has_next;
        state.currentTable.hasPrev = payload.data.result.has_prev;
        state.currentTable.result = payload.data.result.query_result;
    },
    setSales: (state, payload) => {
        state.sales.hasNext = payload.data.result.has_next;
        state.sales.hasPrev = payload.data.result.has_prev;
        state.sales.result = payload.data.result.query_result;

        state.currentTable.hasNext = payload.data.result.has_next;
        state.currentTable.hasPrev = payload.data.result.has_prev;
        state.currentTable.result = payload.data.result.query_result;
    },
    setCategories: (state, payload) => {
        state.categories.hasNext = payload.data.result.has_next;
        state.categories.hasPrev = payload.data.result.has_prev;
        state.categories.result = payload.data.result.query_result;

        state.currentTable.hasNext = payload.data.result.has_next;
        state.currentTable.hasPrev = payload.data.result.has_prev;
        state.currentTable.result = payload.data.result.query_result;
    },
    setReviews: (state, payload) => {
        state.reviews.hasNext = payload.data.result.has_next;
        state.reviews.hasPrev = payload.data.result.has_prev;
        state.reviews.result = payload.data.result.query_result;

        state.currentTable.hasNext = payload.data.result.has_next;
        state.currentTable.hasPrev = payload.data.result.has_prev;
        state.currentTable.result = payload.data.result.query_result;
    }
}

const actions = {
    updateParts: (context, payload) => {
        bus.$emit("showLoading", "Contacting Server");
        axios.post("/query_parts/", {
            query: {
                "offset": payload.offset,
                "sort_by": payload.sort_by,
                "limit": payload.limit,
                "search": payload.search,
                "active": payload.active
            }
        }).then((response) => {
            context.commit('setParts', response);
        }).catch((error) => {
            bus.$emit("showWarning", error.response.data);
        });
        bus.$emit("hideLoading");
    },
    updateSuppliers: (context, payload) => {
        bus.$emit("showLoading", "Contacting Server");
        axios.post("/query_suppliers/", {
            query: {
                "offset": payload.offset,
                "sort_by": payload.sort_by,
                "limit": payload.limit,
                "search": payload.search,
                "active": payload.active
            }
        }).then((response) => {
            context.commit('setSuppliers', response);
        }).catch((error) => {
            bus.$emit("showWarning", error.response.data);
        });
        bus.$emit("hideLoading");
    },
    updateTransactions: (context, payload) => {
        bus.$emit("showLoading", "Contacting Server");
        axios.post("/query_transactions/", {
            query: {
                "offset": payload.offset,
                "sort_by": payload.sort_by,
                "limit": payload.limit,
                "search": payload.search,
                "active": payload.active
            }
        }).then((response) => {
            context.commit('setTransactions', response);
        }).catch((error) => {
            bus.$emit("showWarning", error.response.data);
        });
        bus.$emit("hideLoading");
    },
    updateCustomers: (context, payload) => {
        bus.$emit("showLoading", "Contacting Server");
        axios.post("/query_customers/", {
            query: {
                "offset": payload.offset,
                "sort_by": payload.sort_by,
                "limit": payload.limit,
                "search": payload.search,
                "active": payload.active
            }
        }).then((response) => {
            context.commit('setCustomers', response);
        }).catch((error) => {
            bus.$emit("showWarning", error.response.data);
        });
        bus.$emit("hideLoading");
    },
    updateSales: (context, payload) => {
        bus.$emit("showLoading", "Contacting Server");
        axios.post("/query_sales/", {
            query: {
                "offset": payload.offset,
                "sort_by": payload.sort_by,
                "limit": payload.limit,
                "search": payload.search,
                "active": payload.active
            }
        }).then((response) => {
            context.commit('setSales', response);
        }).catch((error) => {
            bus.$emit("showWarning", error.response.data);
        });
        bus.$emit("hideLoading");
    },
    updateCategories: (context, payload) => {
        bus.$emit("showLoading", "Contacting Server");
        axios.post("/query_categories/", {
            query: {
                "offset": payload.offset,
                "sort_by": payload.sort_by,
                "limit": payload.limit,
                "search": payload.search,
                "active": payload.active
            }
        }).then((response) => {
            console.log(response);
            context.commit('setCategories', response);
        }).catch((error) => {
            bus.$emit("showWarning", error.response.data);
        });
        bus.$emit("hideLoading");
    },
    updateReviews: (context, payload) => {
        bus.$emit("showLoading", "Contacting Server");
        axios.post("/query_reviews/", {
            query: {
                "offset": payload.offset,
                "sort_by": payload.sort_by,
                "limit": payload.limit,
                "search": payload.search,
                "active": payload.active
            }
        }).then((response) => {
            context.commit('setReviews', response);
        }).catch((error) => {
            bus.$emit("showWarning", error.response.data);
        });
        bus.$emit("hideLoading");
    },
}

export default {
    state,
    mutations,
    actions
}