import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('auth_token') || null)
  
  const isAuthenticated = computed(() => !!token.value)
  const isSuperAdmin = computed(() => user.value?.user_type === 'SUPERADMIN')
  const isEditor = computed(() => user.value?.user_type === 'EDITOR')

  const api = axios.create({
    baseURL: 'http://localhost:8000/api',
    headers: {
      'Content-Type': 'application/json'
    }
  })

  api.interceptors.request.use((config) => {
    if (token.value) {
      config.headers.Authorization = `Token ${token.value}`
    }
    return config
  })

  const login = async (username, password) => {
    try {
      const response = await api.post('/auth/login/', { username, password })
      token.value = response.data.token
      localStorage.setItem('auth_token', response.data.token)
      await fetchCurrentUser()
      return true
    } catch (error) {
      console.error('Login error:', error)
      throw error
    }
  }

  const logout = async () => {
    token.value = null
    user.value = null
    localStorage.removeItem('auth_token')
  }

  const fetchCurrentUser = async () => {
    try {
      const response = await api.get('/users/me/')
      user.value = response.data
    } catch (error) {
      console.error('Fetch user error:', error)
      throw error
    }
  }

  return {
    user,
    token,
    isAuthenticated,
    isSuperAdmin,
    isEditor,
    login,
    logout,
    fetchCurrentUser
  }
})
