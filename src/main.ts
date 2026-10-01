import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { router } from './router'
import './style.css'
import App from './App.vue'

const pinia = createPinia()
const app = createApp(App)

// errors catched by Vue are handed on as ordinary window errors
app.config.errorHandler = (err) => reportError(err)

app.use(pinia)
app.use(router)

app.mount('#app')
