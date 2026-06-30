import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/',
    redirect: '/users'
  },
  {
    path: '/users',
    name: 'Users',
    component: () => import('../views/Users.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/users/create',
    name: 'CreateUser',
    component: () => import('../views/UserForm.vue'),
    meta: { requiresAuth: true, requiresSuperAdmin: true }
  },
  {
    path: '/users/:id/edit',
    name: 'EditUser',
    component: () => import('../views/UserForm.vue'),
    meta: { requiresAuth: true, requiresSuperAdmin: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresSuperAdmin && !authStore.isSuperAdmin) {
    next('/users')
  } else {
    next()
  }
})

export default router
