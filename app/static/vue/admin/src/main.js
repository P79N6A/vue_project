require("./assets/normalize.css")

import Vue from "vue/dist/vue.js"
import VeeValidate from "vee-validate"
Vue.use(VeeValidate);

import App from "./App.vue"
import router from "./router"
import store from "./store/store"

import * as OfflinePluginRuntime from 'offline-plugin/runtime';
OfflinePluginRuntime.install();

export const bus = new Vue();

Vue.config.productionTip = false

window.addEventListener("load", function() {
    new Vue({
      el: "#app",
      router,
      store,
      template: "<App/>",
      components: { App }
    });
});
