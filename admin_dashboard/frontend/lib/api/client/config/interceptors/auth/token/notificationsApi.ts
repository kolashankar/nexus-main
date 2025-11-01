import apiClient from './apiClient'

export const notificationsApi = {
  getAll: (params?: any) => apiClient.get('/admin/notifications', { params }),
  getById: (id: string) => apiClient.get(`/admin/notifications/${id}`),
  create: (data: any) => apiClient.post('/admin/notifications', data),
  update: (id: string, data: any) => apiClient.put(`/admin/notifications/${id}`, data),
  delete: (id: string) => apiClient.delete(`/admin/notifications/${id}`),
  send: (id: string) => apiClient.post(`/admin/notifications/${id}/send`),
  getStats: () => apiClient.get('/admin/notifications/stats'),
}
