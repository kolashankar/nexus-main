import apiClient from './apiClient'

export const contentApprovalApi = {
  submit: (data: any) => apiClient.post('/admin/content/submit', data),
  getPending: (params?: any) => apiClient.get('/admin/content/pending', { params }),
  approve: (id: string, comment?: string) => apiClient.post(`/admin/content/${id}/approve`, { comment }),
  reject: (id: string, comment: string) => apiClient.post(`/admin/content/${id}/reject`, { comment }),
  getStats: () => apiClient.get('/admin/content/stats'),
  getHistory: (params?: any) => apiClient.get('/admin/content/history', { params }),
}
