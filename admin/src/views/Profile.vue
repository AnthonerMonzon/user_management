<template>
  <div class="profile-container">
    <h2>My Profile</h2>
    
    <div v-if="authStore.loading" class="loading">Loading profile...</div>
    
    <div v-else-if="authStore.user" class="profile-card">
      <div class="profile-header">
        <div class="avatar">
          {{ authStore.user.username.charAt(0).toUpperCase() }}
        </div>
        <div class="user-info">
          <h3>{{ authStore.user.username }}</h3>
          <p>{{ authStore.user.email }}</p>
        </div>
      </div>
      
      <div class="profile-details">
        <div class="detail-item">
          <span class="label">Full Name:</span>
          <span class="value">{{ fullName }}</span>
        </div>
        <div class="detail-item">
          <span class="label">Role:</span>
          <span :class="['value', 'role', authStore.user.user_type.toLowerCase()]">
            {{ authStore.user.user_type }}
          </span>
        </div>
        <div class="detail-item">
          <span class="label">Status:</span>
          <span :class="['value', 'status', authStore.user.is_active ? 'active' : 'inactive']">
            {{ authStore.user.is_active ? 'Active' : 'Inactive' }}
          </span>
        </div>
        <div class="detail-item">
          <span class="label">Member Since:</span>
          <span class="value">{{ formatDate(authStore.user.created_at) }}</span>
        </div>
      </div>
      
      <div class="permissions-info">
        <h4>Permissions</h4>
        <ul>
          <li v-if="authStore.isSuperAdmin">✓ Can manage users (CRUD operations)</li>
          <li v-if="authStore.isSuperAdmin">✓ Full system access</li>
          <li v-if="authStore.isEditor">✓ Can view users (read-only)</li>
          <li v-if="authStore.isEditor">✗ Cannot manage users</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const fullName = computed(() => {
  const user = authStore.user
  if (!user) return ''
  const parts = [user.first_name, user.last_name].filter(Boolean)
  return parts.length > 0 ? parts.join(' ') : 'Not set'
})

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(() => {
  authStore.fetchCurrentUser()
})
</script>

<style scoped>
.profile-container {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: 0 auto;
}

.profile-container h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #7f8c8d;
}

.profile-card {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #ecf0f1;
}

.avatar {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: bold;
  color: white;
}

.user-info h3 {
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.user-info p {
  color: #7f8c8d;
}

.profile-details {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.detail-item .label {
  font-weight: 500;
  color: #34495e;
}

.detail-item .value {
  color: #2c3e50;
}

.detail-item .role.superadmin {
  color: #e74c3c;
  font-weight: 600;
}

.detail-item .role.editor {
  color: #3498db;
  font-weight: 600;
}

.detail-item .status.active {
  color: #27ae60;
  font-weight: 600;
}

.detail-item .status.inactive {
  color: #95a5a6;
  font-weight: 600;
}

.permissions-info {
  padding: 1.5rem;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.permissions-info h4 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.permissions-info ul {
  list-style: none;
  padding: 0;
}

.permissions-info li {
  padding: 0.5rem 0;
  color: #34495e;
}
</style>
