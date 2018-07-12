import Vue from "vue"
import Vuex from "vuex"
import query from "./query"
import table from "./table"
import global from "./global"

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        query,
        table,
        global
    }
})