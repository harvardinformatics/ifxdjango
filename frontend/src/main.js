// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import APIService from '@/API/API'
import ifxvue from 'ifxvue'
import APIStore from '@/API/APIStore'
import vuexStore from '@/store'
import { IFXRequestAPI } from '@/API/IFXRequestAPI'
import vuetify from '@/plugins/vuetify'
import JsonCSV from 'vue-json-csv'
import axios from 'axios'
import VueCookie from 'vue-cookie'
import moment from 'moment'
import { router } from './router'
import App from './App'
import 'vuetify/dist/vuetify.min.css'
import 'ifxvue/dist/ifxvue.css'
import '@mdi/font/css/materialdesignicons.css'

Vue.component('downloadCsv', JsonCSV)
Vue.use(VueCookie)
Vue.config.productionTip = false

Vue.config.productionTip = false
// Register ifxvue module
// Pass in vuexStore to register incoming vuex modules
// Pass in APIStore so ifxvue has access to application config data
Vue.use(ifxvue, { vuexStore, APIStore })

const api = new APIService(APIStore)
Vue.prototype.$api = Vue.observable(api)
api.auth.initAuthUser()

// Loop through routes, set options for all paths and admin routes
// To make route admin only, go to router index and add isCNSAdminRoute:true to specific route

router.beforeEach((to, from, next) => {
  if (to.name === 'Forbidden' || to.name === 'Login') {
    next()
  }
  if (api.authUser && api.authUser.isAuthenticated) {
    if (to.matched.some((mroute) => mroute.meta.AdminRoute)) {
      if (api.authUser.hasGroup('Admin')) {
        next()
      } else {
        next({ name: 'Forbidden' })
      }
    } else {
      next()
    }
  } else {
    // When a user is not authenticated, this branch will be run twice for some reason
    // The query parameter "next" is added the first time, and then just passed along the second time
    const routeData = { name: 'Login' }
    if (Object.keys(to.query).length !== 0) {
      routeData.query = to.query
    } else {
      routeData.query = { next: to.path }
    }
    next(routeData)
  }
})

const requestApi = new IFXRequestAPI(api, 'default-approver')
Vue.prototype.$requestApi = requestApi

Vue.filter('users', (value) => {
  // Display one or more users via full_name attribute
  let names = []
  if (value) {
    if (Array.isArray(value)) {
      names = value.map((u) => {
        return u.full_name ? u.full_name : u.username
      })
    } else {
      names = [value.full_name ? value.full_name : value.username]
    }
  }
  return names.join(', ')
})

Vue.filter('yesno', (value) => {
  return value ? 'Yes' : 'No'
})

Vue.filter('humanDate', (value) => {
  let datestr = ''
  if (value) {
    datestr = moment(String(value)).format('M/DD/YYYY')
  }
  return datestr
})

Vue.filter('timeOnly', (value) => {
  let datestr = ''
  if (value) {
    datestr = moment(String(value)).format('h:mm A')
  }
  return datestr
})

Vue.filter('spelledOutDay', (value) => {
  let datestr = ''
  if (value) {
    datestr = moment(String(value)).format('dddd, MMMM Do')
  }
  return datestr
})

// An eventhub is needed to emit and register events in sibling components instantaneously
// Instantiate and add as global mixin
const eventHub = new Vue()
Vue.mixin({
  data: function () {
    return {
      eventHub: eventHub,
    }
  },
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  vuetify,
  store: vuexStore,
  router,
  axios,
  components: { App },
  render: (h) => h(App),
})

// auth.checkAuthentication()
