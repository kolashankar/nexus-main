import apiClient from './apiClient'

export const contentManagementApi = {
  // Media Library
  media: {
    getAll: (params?: any) => apiClient.get('/admin/content/media', { params }),
    upload: (file: File, folder?: string) => {
      const formData = new FormData()
      formData.append('file', file)
      if (folder) formData.append('folder', folder)
      return apiClient.post('/admin/content/media', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    },
    delete: (id: string) => apiClient.delete(`/admin/content/media/${id}`),
  },
  
  // Tags
  tags: {
    getAll: () => apiClient.get('/admin/content/tags'),
    create: (name: string) => apiClient.post('/admin/content/tags', { name }),
    update: (id: string, name: string) => apiClient.put(`/admin/content/tags/${id}`, { name }),
    delete: (id: string) => apiClient.delete(`/admin/content/tags/${id}`),
  },
  
  // Categories
  categories: {
    getAll: () => apiClient.get('/admin/content/categories'),
    create: (data: any) => apiClient.post('/admin/content/categories', data),
    update: (id: string, data: any) => apiClient.put(`/admin/content/categories/${id}`, data),
    delete: (id: string) => apiClient.delete(`/admin/content/categories/${id}`),
  },
  
  // SEO
  seo: {
    getAll: (params?: any) => apiClient.get('/admin/content/seo', { params }),
    update: (contentType: string, contentId: string, data: any) => 
      apiClient.put(`/admin/content/seo/${contentType}/${contentId}`, data),
  },
}
