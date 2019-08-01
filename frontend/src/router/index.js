import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import Home from '@/components/Home'
import NotFound from '@/components/NotFound'
import auth from '@/auth'

Vue.use(Router)

const router = new Router({
  base: '/project_name/',
  mode: 'history',
  routes: [
    {
      path: '/login/',
      name: 'Login',
      component: Login,
      pathToRegexpOptions: {strict: true}
    },
    {
      path: '/',
      name: 'Home',
      component: Home,
      pathToRegexpOptions: {strict: true},
      beforeEnter: (to, from, next) => {
        if (auth.isAuthenticated()) {
          next()
          return
        }
        next({name: 'Login', query: {from: window.location.pathname}})
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
