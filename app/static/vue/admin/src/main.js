require("./assets/normalize.css")

import Vue from "vue"
import App from "./App.vue"
import VeeValidate from "vee-validate"
import router from "./router"
import store from "./store/store"

export const bus = new Vue();

Vue.config.productionTip = false

Vue.use(VeeValidate);

new Vue({
  el: "#app",
  router,
  store,
  template: "<App/>",
  components: { App }
});