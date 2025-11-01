import apiClient from './apiClient'

export const usersApi = {
  getAll: (params?: any) => apiClient.get('/admin/users', { params }),
  getById: (id: string) => apiClient.get(`/admin/users/${id}`),
  update: (id: string, data: any) => apiClient.put(`/admin/users/${id}`, data),
  ban: (id: string, reason: string) => apiClient.post(`/admin/users/${id}/ban`, { reason }),
  unban: (id: string) => apiClient.post(`/admin/users/${id}/unban`),
  getActivity: (id: string, params?: any) => apiClient.get(`/admin/users/${id}/activity`, { params }),
  getSegments: () => apiClient.get('/admin/users/segments'),
  getStats: () => apiClient.get('/admin/users/stats'),
}
