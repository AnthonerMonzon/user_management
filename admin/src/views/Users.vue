<template>
  <div class="users-container">
    <div class="users-header">
      <h2>Users Management</h2>
      <button v-if="authStore.isSuperAdmin" @click="goToCreate" class="create-btn">
        + Create User
      </button>
    </div>

    <div v-if="usersStore.loading" class="loading">Loading users...</div>
    
    <div v-else-if="usersStore.error" class="error">{{ usersStore.error }}</div>
    
    <div v-else class="users-table">
      <table>
        <thead>
          <tr>
            <th>Username</th>
            <th>Email</th>
            <th>Type</th>
            <th>Status</th>
            <th v-if="authStore.isSuperAdmin">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in usersStore.users" :key="user.id">
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>
              <span :class="['user-type', user.user_type.toLowerCase()]">
                {{ user.user_type }}
              </span>
            </td>
            <td>
              <span :class="['status', user.is_active ? 'active' : 'inactive']">
                {{ user.is_active ? 'Active' : 'Inactive' }}
              </span>
            </td>
            <td v-if="authStore.isSuperAdmin" class="actions">
              <button @click="goToEdit(user.id)" class="edit-btn">Edit</button>
              <button @click="confirmDelete(user)" class="delete-btn">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="usersStore.users.length === 0" class="no-users">
        No users found.
      </div>
    </div>

    <div v-if="showDeleteModal" class="modal-overlay" @click="closeModal">
      <div class="modal" @click.stop>
        <h3>Confirm Delete</h3>
        <p>Are you sure you want to delete user "{{ userToDelete?.username }}"?</p>
        <div class="modal-actions">
          <button @click="closeModal" class="cancel-btn">Cancel</button>
          <button @click="handleDelete" class="confirm-delete-btn">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUsersStore } from '../stores/users'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const usersStore = useUsersStore()
const authStore = useAuthStore()

const showDeleteModal = ref(false)
const userToDelete = ref(null)

onMounted(() => {
  usersStore.fetchUsers()
})

const goToCreate = () => {
  router.push('/users/create')
}

const goToEdit = (id) => {
  router.push(`/users/${id}/edit`)
}

const confirmDelete = (user) => {
  userToDelete.value = user
  showDeleteModal.value = true
}

const closeModal = () => {
  showDeleteModal.value = false
  userToDelete.value = null
}

const handleDelete = async () => {
  try {
    await usersStore.deleteUser(userToDelete.value.id)
    closeModal()
  } catch (error) {
    console.error('Delete failed:', error)
  }
}
</script>

<style scoped>
.users-container {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.users-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.users-header h2 {
  color: #2c3e50;
}

.create-btn {
  background-color: #27ae60;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.create-btn:hover {
  background-color: #219150;
}

.loading, .error, .no-users {
  text-align: center;
  padding: 2rem;
  color: #7f8c8d;
}

.error {
  color: #e74c3c;
}

.users-table table {
  width: 100%;
  border-collapse: collapse;
}

.users-table th,
.users-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #ecf0f1;
}

.users-table th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #2c3e50;
}

.user-type {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
}

.user-type.superadmin {
  background-color: #e74c3c;
  color: white;
}

.user-type.editor {
  background-color: #3498db;
  color: white;
}

.status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
}

.status.active {
  background-color: #27ae60;
  color: white;
}

.status.inactive {
  background-color: #95a5a6;
  color: white;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.edit-btn {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: background-color 0.3s;
}

.edit-btn:hover {
  background-color: #2980b9;
}

.delete-btn {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: background-color 0.3s;
}

.delete-btn:hover {
  background-color: #c0392b;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  max-width: 400px;
  width: 90%;
}

.modal h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.modal p {
  margin-bottom: 1.5rem;
  color: #34495e;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.cancel-btn {
  background-color: #95a5a6;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.cancel-btn:hover {
  background-color: #7f8c8d;
}

.confirm-delete-btn {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.confirm-delete-btn:hover {
  background-color: #c0392b;
}
</style>
