import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { router } from './router'
import './style.css'
import App from './App.vue'
import Vue3TouchEvents, {
  type Vue3TouchEventsOptions,
} from "vue3-touch-events";

const pinia = createPinia()
const app = createApp(App)

app.use(pinia)
app.use(router)
app.use<Vue3TouchEventsOptions>(Vue3TouchEvents, {
  disableClick: false
})

app.mount('#app').$nextTick(() => {
  // Use contextBridge
  window.ipcRenderer.on('main-process-message', (_event, message) => {
    console.log(message)
  })
})
