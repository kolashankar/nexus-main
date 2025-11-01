import apiClient from './apiClient'

export const adminsApi = {
  getAll: (params?: any) => apiClient.get('/admin/admins', { params }),
  getById: (id: string) => apiClient.get(`/admin/admins/${id}`),
  create: (data: any) => apiClient.post('/admin/admins', data),
  update: (id: string, data: any) => apiClient.put(`/admin/admins/${id}`, data),
  delete: (id: string) => apiClient.delete(`/admin/admins/${id}`),
  updatePermissions: (id: string, permissions: any) => apiClient.put(`/admin/admins/${id}/permissions`, { permissions }),
  getActivityLogs: (params?: any) => apiClient.get('/admin/admins/activity-logs', { params }),
}
