import MainPage from '../views/MainPage.vue'
import SecondPage from '../views/SecondPage.vue'
import AdminView from '../views/AdminView.vue'
import { RouteNames } from './RouteNames'

import type { RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  // {
  //   path: '/',
  //   name: RouteNames.MAIN_PAGE,
  //   redirect: { name: RouteNames.MAIN_PAGE },
  // },
  {
    path: '/',
    name: RouteNames.MAIN_PAGE,
    component: MainPage,
  },
  {
    path: '/admin',
    name: RouteNames.ADMIN_VIEW,
    component: () => AdminView,
  },
  {
    path: '/second',
    name: RouteNames.SECOND_PAGE,
    component: SecondPage,
  },
]

export default routes
