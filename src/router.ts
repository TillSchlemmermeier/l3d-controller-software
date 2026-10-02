import { createRouter, createWebHashHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import MainPage from './views/MainPage.vue'
import AdminView from './views/AdminView.vue'
import RemoteControl from './views/RemoteControl.vue'

export enum RouteNames {
  MAIN_PAGE = 'main_page',
  ADMIN_VIEW = 'admin_view',
  REMOTE_CONTROL = 'remote_control',
}

const routes: Array<RouteRecordRaw> = [
  { path: '/', name: RouteNames.MAIN_PAGE, component: MainPage },
  { path: '/admin', name: RouteNames.ADMIN_VIEW, component: AdminView },
  { path: '/remote', name: RouteNames.REMOTE_CONTROL, component: RemoteControl },
]

export const router = createRouter({
  history: createWebHashHistory(),
  routes,
})
