// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import vuetify from './plugins/vuetify';
import App from './App.vue'
import router from './router'
import 'vuetify/dist/vuetify.min.css'
import axios from 'axios'
import VueCookie from 'vue-cookie'
import auth from './auth'
import moment from 'moment'
import store from './store'
import ifxvue from 'ifxvue'

Vue.use(VueCookie)
Vue.config.productionTip = false
Vue.use(ifxvue, {store})

Vue.filter('yesno', function (value) {
  return value ? 'Yes' : 'No';
})
Vue.filter('humanDatetime', function (value) {
  let datestr = ''
  if (value) {
    datestr = moment(String(value)).format('M/DD/YYYY h:mm A')
  }
  return datestr
})
Vue.filter('emailDisplay', function (value) {
  let emailstr = ''
  if (value) {
    emailstr = value.replace('@', ' at ')
  }
  return emailstr
})

const eventHub = new Vue()

Vue.mixin({
  data: function () {
    return {
      eventHub: eventHub
    }
  }
})

// Every component used by the ifxvue plugin must be globally registered


/* eslint-disable no-new */
new Vue({
  vuetify,
  el: '#app',
  store,
  router,
  axios,
  components: { App },
  render: h => h(App)
})

auth.checkAuthentication()
