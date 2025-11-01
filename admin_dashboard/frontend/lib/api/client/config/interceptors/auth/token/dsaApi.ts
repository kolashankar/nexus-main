import apiClient from './apiClient'

export const dsaApi = {
  // Topics
  topics: {
    getAll: (params?: any) => apiClient.get('/admin/dsa/topics', { params }),
    getById: (id: string) => apiClient.get(`/admin/dsa/topics/${id}`),
    create: (data: any) => apiClient.post('/admin/dsa/topics', data),
    update: (id: string, data: any) => apiClient.put(`/admin/dsa/topics/${id}`, data),
    delete: (id: string) => apiClient.delete(`/admin/dsa/topics/${id}`),
    getStats: () => apiClient.get('/admin/dsa/topics/stats'),
  },
  
  // Questions
  questions: {
    getAll: (params?: any) => apiClient.get('/admin/dsa/questions', { params }),
    getById: (id: string) => apiClient.get(`/admin/dsa/questions/${id}`),
    create: (data: any) => apiClient.post('/admin/dsa/questions', data),
    update: (id: string, data: any) => apiClient.put(`/admin/dsa/questions/${id}`, data),
    delete: (id: string) => apiClient.delete(`/admin/dsa/questions/${id}`),
    generateAI: (data: any) => apiClient.post('/admin/dsa/questions/generate-ai', data),
    getStatsByDifficulty: () => apiClient.get('/admin/dsa/questions/stats/difficulty'),
    getStatsByTopic: () => apiClient.get('/admin/dsa/questions/stats/topic'),
  },
  
  // Sheets
  sheets: {
    getAll: (params?: any) => apiClient.get('/admin/dsa/sheets', { params }),
    getById: (id: string) => apiClient.get(`/admin/dsa/sheets/${id}`),
    create: (data: any) => apiClient.post('/admin/dsa/sheets', data),
    update: (id: string, data: any) => apiClient.put(`/admin/dsa/sheets/${id}`, data),
    delete: (id: string) => apiClient.delete(`/admin/dsa/sheets/${id}`),
    generateAI: (data: any) => apiClient.post('/admin/dsa/sheets/generate-ai', data),
    addQuestion: (id: string, questionId: string) => apiClient.post(`/admin/dsa/sheets/${id}/questions`, { question_id: questionId }),
    removeQuestion: (id: string, questionId: string) => apiClient.delete(`/admin/dsa/sheets/${id}/questions/${questionId}`),
    togglePublish: (id: string) => apiClient.post(`/admin/dsa/sheets/${id}/toggle-publish`),
    getStats: () => apiClient.get('/admin/dsa/sheets/stats'),
  },
  
  // Companies
  companies: {
    getAll: (params?: any) => apiClient.get('/admin/dsa/companies', { params }),
    getById: (id: string) => apiClient.get(`/admin/dsa/companies/${id}`),
    create: (data: any) => apiClient.post('/admin/dsa/companies', data),
    update: (id: string, data: any) => apiClient.put(`/admin/dsa/companies/${id}`, data),
    delete: (id: string) => apiClient.delete(`/admin/dsa/companies/${id}`),
    getStats: () => apiClient.get('/admin/dsa/companies/stats'),
    getTop: () => apiClient.get('/admin/dsa/companies/top'),
  },
}
