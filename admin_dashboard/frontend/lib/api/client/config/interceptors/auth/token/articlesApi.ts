import apiClient from './apiClient'

export interface Article {
  _id?: string
  title: string
  content: string
  excerpt: string
  author: string
  tags: string[]
  category: string
  cover_image?: string
  read_time?: number
  is_published: boolean
  views_count?: number
  created_at?: string
  updated_at?: string
}

export const articlesApi = {
  getAll: (params?: any) => apiClient.get('/admin/articles', { params }),
  getById: (id: string) => apiClient.get(`/admin/articles/${id}`),
  create: (data: Article) => apiClient.post('/admin/articles', data),
  update: (id: string, data: Partial<Article>) => apiClient.put(`/admin/articles/${id}`, data),
  delete: (id: string) => apiClient.delete(`/admin/articles/${id}`),
  generateAI: (data: any) => apiClient.post('/admin/articles/generate-ai', data),
  togglePublish: (id: string) => apiClient.post(`/admin/articles/${id}/toggle-publish`),
}
