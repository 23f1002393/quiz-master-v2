import { createApp } from 'vue'
import '@assets/style.css'
import App from '@/App.vue'
import router from '@/router'
import { store } from '@/store'

const app = createApp(App)
app.config.performance = true
app.use(router).use(store).mount('#app')
