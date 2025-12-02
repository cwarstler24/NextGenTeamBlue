import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AssetView from '../views/AssetView.vue'
import AssetAddView from '../views/AssetAddView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/tester',
      name: 'api-tester',
      component: () => import('../views/ApiTesterView.vue'),
    },
    {
      path: '/assets/:id',
      name: 'AssetView',
      component: AssetView,
    },
    {
      path: '/add-asset',
      name: 'AssetAdd',
      component: AssetAddView,
    },
  ],
})

export default router
