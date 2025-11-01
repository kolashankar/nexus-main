import apiClient from './apiClient'

export const settingsApi = {
  getGeneral: () => apiClient.get('/admin/settings/general'),
  updateGeneral: (data: any) => apiClient.put('/admin/settings/general', data),
  
  getEmail: () => apiClient.get('/admin/settings/email'),
  updateEmail: (data: any) => apiClient.put('/admin/settings/email', data),
  testEmail: (email: string) => apiClient.post('/admin/settings/email/test', { email }),
  
  getApiKeys: () => apiClient.get('/admin/settings/api-keys'),
  updateApiKeys: (data: any) => apiClient.put('/admin/settings/api-keys', data),
  
  getTheme: () => apiClient.get('/admin/settings/theme'),
  updateTheme: (data: any) => apiClient.put('/admin/settings/theme', data),
  
  backup: () => apiClient.post('/admin/settings/backup'),
  restore: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return apiClient.post('/admin/settings/restore', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  
  getSystemHealth: () => apiClient.get('/admin/settings/system-health'),
}
