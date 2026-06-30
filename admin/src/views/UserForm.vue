<template>
  <div class="user-form-container">
    <h2>{{ isEdit ? 'Edit User' : 'Create User' }}</h2>
    
    <form @submit.prevent="handleSubmit" class="user-form">
      <div class="form-group">
        <label for="username">Username *</label>
        <input
          id="username"
          v-model="formData.username"
          type="text"
          required
          placeholder="Enter username"
        />
      </div>
      
      <div class="form-group">
        <label for="email">Email *</label>
        <input
          id="email"
          v-model="formData.email"
          type="email"
          required
          placeholder="Enter email"
        />
      </div>
      
      <div class="form-group">
        <label for="firstName">First Name</label>
        <input
          id="firstName"
          v-model="formData.first_name"
          type="text"
          placeholder="Enter first name"
        />
      </div>
      
      <div class="form-group">
        <label for="lastName">Last Name</label>
        <input
          id="lastName"
          v-model="formData.last_name"
          type="text"
          placeholder="Enter last name"
        />
      </div>
      
      <div class="form-group">
        <label for="userType">User Type *</label>
        <select id="userType" v-model="formData.user_type" required>
          <option value="EDITOR">Editor</option>
          <option value="SUPERADMIN">SuperAdmin</option>
        </select>
      </div>
      
      <div v-if="!isEdit" class="form-group">
        <label for="password">Password *</label>
        <input
          id="password"
          v-model="formData.password"
          type="password"
          required
          placeholder="Enter password"
        />
      </div>
      
      <div v-if="!isEdit" class="form-group">
        <label for="passwordConfirm">Confirm Password *</label>
        <input
          id="passwordConfirm"
          v-model="formData.password_confirm"
          type="password"
          required
          placeholder="Confirm password"
        />
      </div>
      
      <div v-if="isEdit" class="form-group">
        <label for="isActive">
          <input
            id="isActive"
            v-model="formData.is_active"
            type="checkbox"
          />
          Active
        </label>
      </div>
      
      <div class="form-actions">
        <button type="button" @click="goBack" class="cancel-btn">Cancel</button>
        <button type="submit" :disabled="loading" class="submit-btn">
          {{ loading ? 'Saving...' : (isEdit ? 'Update' : 'Create') }}
        </button>
      </div>
      
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUsersStore } from '../stores/users'

const router = useRouter()
const route = useRoute()
const usersStore = useUsersStore()

const isEdit = computed(() => !!route.params.id)
const userId = computed(() => route.params.id)

const formData = ref({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  user_type: 'EDITOR',
  password: '',
  password_confirm: '',
  is_active: true
})

const loading = ref(false)
const error = ref('')

onMounted(async () => {
  if (isEdit.value) {
    try {
      const user = usersStore.users.find(u => u.id === parseInt(userId.value))
      if (user) {
        formData.value = {
          username: user.username,
          email: user.email,
          first_name: user.first_name,
          last_name: user.last_name,
          user_type: user.user_type,
          is_active: user.is_active
        }
      }
    } catch (err) {
      error.value = 'Failed to load user data'
    }
  }
})

const handleSubmit = async () => {
  loading.value = true
  error.value = ''
  
  try {
    if (!isEdit.value) {
      if (formData.value.password !== formData.value.password_confirm) {
        error.value = 'Passwords do not match'
        loading.value = false
        return
      }
      await usersStore.createUser(formData.value)
    } else {
      const updateData = {
        username: formData.value.username,
        email: formData.value.email,
        first_name: formData.value.first_name,
        last_name: formData.value.last_name,
        user_type: formData.value.user_type,
        is_active: formData.value.is_active
      }
      await usersStore.updateUser(userId.value, updateData)
    }
    router.push('/users')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Operation failed'
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.push('/users')
}
</script>

<style scoped>
.user-form-container {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: 0 auto;
}

.user-form-container h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.user-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: #34495e;
}

.form-group input,
.form-group select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
}

.form-group input[type="checkbox"] {
  width: auto;
  margin-right: 0.5rem;
}

.form-group label[for="isActive"] {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.cancel-btn {
  flex: 1;
  padding: 0.75rem;
  background-color: #95a5a6;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.cancel-btn:hover {
  background-color: #7f8c8d;
}

.submit-btn {
  flex: 1;
  padding: 0.75rem;
  background-color: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.submit-btn:hover:not(:disabled) {
  background-color: #5568d3;
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  color: #e74c3c;
  padding: 1rem;
  background-color: #fadbd8;
  border-radius: 4px;
  margin-top: 1rem;
}
</style>
