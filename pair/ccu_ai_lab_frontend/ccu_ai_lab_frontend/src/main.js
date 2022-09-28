import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import
{
  BootstrapVue,
  IconsPlugin
} from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import Vuex from 'vuex'
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueMeta from 'vue-meta'

Vue.config.productionTip = false;
Vue.use(VueAxios, axios)

// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)
Vue.use(VueMeta)
Vue.use(Vuex)
const store = new Vuex.Store({
  state: {
    isLogin: localStorage.getItem('token') == null ? false : true
  },
})

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
