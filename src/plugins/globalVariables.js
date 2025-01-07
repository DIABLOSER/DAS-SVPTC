// plugins/globalVariables.ts
export default {
  install: (app) => {
    app.config.globalProperties.$accessToken = null;
    app.config.globalProperties.$openId = null;
    app.config.globalProperties.$avator=null;
  }
}