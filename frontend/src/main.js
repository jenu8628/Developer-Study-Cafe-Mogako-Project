import Vue from 'vue'
import App from './App.vue'
import router from './router'
import VueGtag from 'vue-gtag'

import InfiniteLoading from 'vue-infinite-loading';

Vue.use(InfiniteLoading, { /* options */ });

Vue.config.productionTip = false

Vue.use(VueGtag, {
  config: {
      id: 'UA-196947883-1' 
  }
}, router);

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
