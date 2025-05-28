import { createRouter, createWebHashHistory } from 'vue-router'
import routes from './Routes'
import { RouteNames } from './RouteNames'

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export { router, RouteNames }
