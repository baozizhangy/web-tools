// store.js
import { createStore } from 'vuex';

const store = createStore({
  state() {
    return {
      selectedEnv: 'BM_SIT',  // 默认环境
    };
  },
  mutations: {
    setSelectedEnv(state, env) {
      state.selectedEnv = env;
    }
  }
});

export default store;
