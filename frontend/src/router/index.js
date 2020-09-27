import Vue from 'vue'
import Router from 'vue-router'

const routerOptions = [
  { path: '/', component: 'login' },
  { path: '/login', name: 'login', query: { next: '' }, component: 'login' },
  { path: '/pageA', name: 'pageA', query: { auth: '' }, component: 'pageA' },
  { path: '*', component: 'NotFound' },
  { path: '/races', component: 'races' }

]

const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`)
  }
})

Vue.use(Router)

export default new Router({
  routes,
  mode: 'history'
})
