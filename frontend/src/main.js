/* eslint-disable brace-style, no-else-return, import/no-unresolved */
import Vue from 'vue'
import APIService from '@/API/API'
import ifxvue from 'ifxvue'
import { IFXRequestAPI } from '@/API/IFXRequestAPI'
import APIStore from '@/API/APIStore'
import vuexStore from '@/store'
import App from '@/App'
import { router, routes } from '@/router'
import vuetify from '@/plugins/vuetify';
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import 'vuetify/dist/vuetify.min.css'
import 'ifxvue/dist/ifxvue.css'
import '@mdi/font/css/materialdesignicons.css'
import JsonCSV from 'vue-json-csv'

Vue.component('downloadCsv', JsonCSV)

Vue.config.productionTip = false
// Register ifxvue module
// Pass in vuexStore to register incoming vuex modules
// Pass in APIStore so ifxvue has access to application config data
Vue.use(ifxvue, { vuexStore, APIStore })

const api = new APIService(APIStore)
Vue.prototype.$api = Vue.observable(api)
api.auth.initAuthUser()

// api.loadUserFromStorage()

const requestApi = new IFXRequestAPI(api, 'default-approver')
Vue.prototype.$requestApi = requestApi

// Loop through routes, set options for all paths and admin routes
// To make route admin only, go to router index and add isAdminRoute:true to specific route
//  route.pathToRegexpOptions = { strict: true }
const check = (to, from, next) => {
  if (api.auth.isAdmin) {
    // TODO: add message
    next()
  } else {
    next({ name: 'Forbidden' })
  }
}

routes.forEach((route) => {
  // eslint-disable-next-line no-param-reassign
  route.pathToRegexpOptions = { strict: true }
  if (route.isAdminRoute) {
    // eslint-disable-next-line no-param-reassign
    route.beforeEnter = check;
  }
  router.addRoute(route)
})

// Disable routes by unathenticated users
router.beforeEach((to, from, next) => {
  if (to.name !== 'Home' && !api.auth.isAuthenticated) {
    api.auth.login()
      .then(() => next())
      .catch(() => next({ name: 'Home' }))
  } else {
    next()
  }
})

/* eslint-disable no-new */
new Vue({
  vuetify,
  el: '#app',
  store: vuexStore,
  router,
  components: { App },
  render: h => h(App)
})
