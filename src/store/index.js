import { createStore } from 'vuex';

export default createStore({
  state: {
    userInfo: JSON.parse(localStorage.getItem('userInfo')) || null, // 从 localStorage 加载用户信息
  },
  mutations: {
    setUserInfo(state, userInfo) {
      state.userInfo = userInfo;
      localStorage.setItem('userInfo', JSON.stringify(userInfo)); // 保存用户信息到 localStorage
    },
    clearUserInfo(state) {
      state.userInfo = null;
      localStorage.removeItem('userInfo'); // 清除用户信息
    },
  },
  actions: {
    updateUserInfo({ commit }, userInfo) {
      commit('setUserInfo', userInfo);
    },
    clearUserInfo({ commit }) {
      commit('clearUserInfo');
    },
  },
  getters: {
    userInfo: (state) => state.userInfo,
    isAuthenticated: (state) => !!state.userInfo, // 检查用户是否已登录
  },
});