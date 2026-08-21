import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { router } from './router'
import './style.css'
import App from './App.vue'

const pinia = createPinia()
const app = createApp(App)

app.config.errorHandler = (err, _instance, info) => {
  console.error(`[vue error] ${info}`, err)
}

window.addEventListener('error', (event) => {
  console.error('[window error]', event.error ?? event.message)
})

window.addEventListener('unhandledrejection', (event) => {
  console.error('[unhandled rejection]', event.reason)
})

app.use(pinia)
app.use(router)

app.mount('#app')
