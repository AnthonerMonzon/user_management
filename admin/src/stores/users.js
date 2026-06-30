import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'
import { useAuthStore } from './auth'

export const useUsersStore = defineStore('users', () => {
  const users = ref([])
  const loading = ref(false)
  const error = ref(null)

  const authStore = useAuthStore()

  const api = axios.create({
    baseURL: 'http://localhost:8000/api',
    headers: {
      'Content-Type': 'application/json'
    }
  })

  api.interceptors.request.use((config) => {
    if (authStore.token) {
      config.headers.Authorization = `Token ${authStore.token}`
    }
    return config
  })

  const fetchUsers = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/users/')
      users.value = response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch users'
      console.error('Fetch users error:', err)
    } finally {
      loading.value = false
    }
  }

  const createUser = async (userData) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/users/', userData)
      users.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.response?.data || 'Failed to create user'
      console.error('Create user error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateUser = async (id, userData) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.put(`/users/${id}/`, userData)
      const index = users.value.findIndex(u => u.id === id)
      if (index !== -1) {
        users.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.response?.data || 'Failed to update user'
      console.error('Update user error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteUser = async (id) => {
    loading.value = true
    error.value = null
    try {
      await api.delete(`/users/${id}/`)
      users.value = users.value.filter(u => u.id !== id)
      return true
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to delete user'
      console.error('Delete user error:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    users,
    loading,
    error,
    fetchUsers,
    createUser,
    updateUser,
    deleteUser
  }
})
