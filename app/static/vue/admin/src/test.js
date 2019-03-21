import Vue from "vue"
import { Test } from "./Test.vue"

Vue.config.productionTip = false

new Vue({
  el: "#app",
  template: "<App/>",
  components: { Test }
});
