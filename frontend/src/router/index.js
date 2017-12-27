import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Topics from '@/components/Topics'

Vue.use(Router)

export default new Router({
  mode: 'history',
  scrollBehavior: function (to, from, savedPosition) {
    if (to.hash) {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve({selector: to.hash})
        }, 500)
      })
    } else {
      return { x: 0, y: 0 }
    }
  },
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/topics',
      name: 'Topics',
      component: Topics
    }
  ]
})
