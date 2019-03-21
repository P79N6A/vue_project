import Vue from "vue/dist/vue.js"
import Router from "vue-router"
import Login from "../pages/Login"
import Dashboard from "../pages/Dashboard"

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: "/",
            name: "Dashboard",
            component: Dashboard
        },
        {
            path: "/login/",
            name: "Login",
            component: Login
        }
    ],
    mode: "history"
})