import MainPage from '../views/MainPage.vue'
import SecondPage from '../views/SecondPage.vue'
import AdminView from '../views/AdminView.vue'
import RemoteControl from '../views/RemoteControl.vue'
import { RouteNames } from './RouteNames'

import type { RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
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
    path: '/remote',
    name: RouteNames.REMOTE_CONTROL,
    component: () => RemoteControl,
  },
  {
    path: '/second',
    name: RouteNames.SECOND_PAGE,
    component: SecondPage,
  },
]

export default routes
