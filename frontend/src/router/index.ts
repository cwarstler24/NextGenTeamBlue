import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import AssetView from '../views/AssetView.vue'
import AssetAddView from '../views/AssetAddView.vue'
import AssetListView from '../views/AssetListView.vue'
import AssetUpdateView from '../views/AssetUpdateView.vue'
import EmployeeListView from '../views/EmployeeListView.vue'
import MascotTheme from '../views/MascotTheme.vue'
import AboutView from '../views/AboutView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/assets',
      name: 'AssetList',
      component: AssetListView,
    },
    {
      path: '/assets/:id',
      name: 'AssetView',
      component: AssetView,
    },
    {
      path : '/assets/:id/update',
      name: 'AssetUpdate',
      component: AssetUpdateView,
    },
    {
      path: '/add-asset',
      name: 'AssetAdd',
      component: AssetAddView,
    },
    {
      path: '/employees',
      name: 'EmployeeList',
      component: EmployeeListView,
    },
    {
      path: '/mascot-theme',
      name: 'MascotTheme',
      component: MascotTheme,
    },
    {
      path: '/about',
      name: 'About',
      component: AboutView,
    },
  ],
})

export default router
