import Vue from 'vue'
import Router from 'vue-router'

const routerOptions = [
  { path: '/', component: 'races' },
  { path: '/login', name: 'login', query: { next: '' }, component: 'login' },
  { path: '/feedback', name: 'feedback', query: { next: '' }, component: 'feedback' },
  { path: '/statistics', name: 'statistics', query: { next: '' }, component: 'statistics' },
  { path: '/disclaimer', name: 'disclaimer', query: { next: '' }, component: 'disclaimer' },
  { path: '/privacyPolicy', name: 'privacyPolicy', query: { next: '' }, component: 'privacyPolicy' },
  { path: '/index', name: 'index', component: 'index' },
  { path: '/races', name: 'races', query: { auth: '' }, component: 'races' },
  { path: '/raceDetail', name: 'raceDetail', component: 'raceDetail' },
  { path: '*', component: 'notFound' }
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
