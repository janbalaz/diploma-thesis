import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Topics from '@/components/Topics'

Vue.use(Router)

export default new Router({
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
