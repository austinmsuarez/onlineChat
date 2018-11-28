import Vue from 'vue'
import Router from 'vue-router'
import loginPage from '@/components/loginPage'
import signUp from '@/components/signUp'
import myChat from '@/components/myChat'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'loginPage',
      component: loginPage
    },
    {
      path: '/signup',
      name: 'signUp',
      component: signUp
    },

    {
      path: '/myChat',
      name: 'myChat',
      component: myChat
    }
  ]
})
