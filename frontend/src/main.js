import { createApp, reactive } from 'vue'
import APIService from '@/API/API'
import ifxvue from 'ifxvue'
import APIStore from '@/API/APIStore'
import pinia from '@/store'
import { IFXRequestAPI } from '@/API/IFXRequestAPI'
import vuetify from '@/plugins/vuetify'
import DownloadCsv from '@/components/DownloadCsv.vue'
import axios from 'axios'
import { router } from './router'
import App from './App.vue'
import { useFilters } from '@/composables/useFilters'
import { eventBus } from '@/composables/useEventBus'
import 'ifxvue/dist/ifxvue.css'
import '@mdi/font/css/materialdesignicons.css'

const app = createApp(App)

app.use(pinia)
app.use(vuetify)
app.use(router)
app.component('downloadCsv', DownloadCsv)

app.use(ifxvue, { pinia, APIStore })

const api = reactive(new APIService(APIStore))
api.auth.initAuthUser()

app.config.globalProperties.$api = api
app.config.globalProperties.$axios = axios
app.config.globalProperties.$eventBus = eventBus

const filters = useFilters()
app.config.globalProperties.$filters = filters

router.beforeEach((to, from, next) => {
  if (to.name === 'Forbidden' || to.name === 'Login') {
    next()
    return
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
app.config.globalProperties.$requestApi = requestApi

app.mount('#app')
