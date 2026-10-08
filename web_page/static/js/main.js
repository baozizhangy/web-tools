import { createApp } from 'vue';
import store from './store';

const app = createApp(App);
app.use(store);  // 使用 Vuex store
app.mount('#app');
