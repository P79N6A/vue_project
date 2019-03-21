import Vue from "vue/dist/vue.js"
import Vuex from "vuex"
import query from "./query"
import table from "./table"
import global from "./global"
import data from "./data"

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        query,
        table,
        global,
        data
    }
})