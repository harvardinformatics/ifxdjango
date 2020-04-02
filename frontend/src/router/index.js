import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Logout from '@/components/Logout'
import Home from '@/components/Home'
import Demo from '@/components/Demo'
import NotFound from '@/components/NotFound'

import auth from '@/auth'

Vue.use(Router)

const router = new Router({
  base: '/ifxtest/',
  mode: 'history',
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login,
      pathToRegexpOptions: {strict: true},
      beforeEnter: (to, from, next) => {
        if (!auth.isAuthenticated()) {
          next()
        } else {
          next({ name: 'Home' })
        }
      }
    },
    {
      path: '/logout',
      name: 'Logout',
      component: Logout,
      pathToRegexpOptions: {strict: true},
      beforeEnter: (to, from, next) => {
        if (auth.isAuthenticated()) {
          next()
        } else {
          next({ name: 'Home' })
        }
      }
    },
    {
      path: '/',
      name: 'Home',
      component: Home,
      pathToRegexpOptions: {strict: true}
    },
    {
      path: '/demo',
      name: 'Demo',
      component: Demo,
      pathToRegexpOptions: {strict: true},
      beforeEnter: (to, from, next) => {
        if (auth.isAuthenticated()) {
          next()
        } else {
          next({ name: 'Login', query: { from: window.location.pathname } })
        }
      }
    },
    {
      path: '/404',
      name: 'NotFound',
      component: NotFound
    },
    {
      path: '*',
      redirect: '/404'
    }
  ]
})

export default router
