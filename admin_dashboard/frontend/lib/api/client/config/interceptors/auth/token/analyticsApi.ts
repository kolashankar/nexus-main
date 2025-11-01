import apiClient from './apiClient'

export interface AnalyticsDashboard {
  users: {
    total: number
    active: number
    new_this_month: number
  }
  jobs: {
    total: number
    active: number
    applications: number
  }
  internships: {
    total: number
    active: number
    applications: number
  }
  articles: {
    total: number
    published: number
    total_views: number
  }
  career_tools: {
    total_usage: number
    popular_tool: string
  }
  gemini_usage: {
    total_calls: number
    total_tokens: number
    cost_estimate: number
  }
}

export interface BulkImportResult {
  success: boolean
  imported: number
  failed: number
  errors: string[]
}

export const analyticsApi = {
  getDashboard: async (): Promise<{ success: boolean; data: AnalyticsDashboard }> => {
    const response = await apiClient.get('/admin/analytics/dashboard')
    return response.data
  },

  getUserEngagement: async (params?: { days?: number }): Promise<{ success: boolean; data: any }> => {
    const response = await apiClient.get('/admin/analytics/user-engagement', { params })
    return response.data
  },

  getJobApplications: async (params?: { days?: number }): Promise<{ success: boolean; data: any }> => {
    const response = await apiClient.get('/admin/analytics/job-applications', { params })
    return response.data
  },

  getGeminiUsage: async (params?: { days?: number }): Promise<{ success: boolean; data: any }> => {
    const response = await apiClient.get('/admin/analytics/gemini-usage', { params })
    return response.data
  },

  getApiLogs: async (params?: { page?: number; limit?: number }): Promise<{ success: boolean; logs: any[]; total: number }> => {
    const response = await apiClient.get('/admin/analytics/api-logs', { params })
    return response.data
  },

  getErrorLogs: async (params?: { page?: number; limit?: number }): Promise<{ success: boolean; logs: any[]; total: number }> => {
    const response = await apiClient.get('/admin/analytics/error-logs', { params })
    return response.data
  },
}

// Bulk Operations API
export const bulkApi = {
  // Export operations
  exportJobs: async (): Promise<Blob> => {
    const response = await apiClient.get('/admin/bulk/jobs/export', {
      responseType: 'blob'
    })
    return response.data
  },

  exportInternships: async (): Promise<Blob> => {
    const response = await apiClient.get('/admin/bulk/internships/export', {
      responseType: 'blob'
    })
    return response.data
  },

  // Import operations
  importJobs: async (file: File): Promise<BulkImportResult> => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await apiClient.post('/admin/bulk/jobs/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
  },

  importInternships: async (file: File): Promise<BulkImportResult> => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await apiClient.post('/admin/bulk/internships/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
  },

  // Bulk delete
  bulkDeleteJobs: async (ids: string[]): Promise<{ success: boolean; deleted: number }> => {
    const response = await apiClient.post('/admin/bulk/jobs/delete', { ids })
    return response.data
  },

  bulkDeleteInternships: async (ids: string[]): Promise<{ success: boolean; deleted: number }> => {
    const response = await apiClient.post('/admin/bulk/internships/delete', { ids })
    return response.data
  },

  // Bulk update
  bulkUpdateJobStatus: async (ids: string[], is_active: boolean): Promise<{ success: boolean; updated: number }> => {
    const response = await apiClient.post('/admin/bulk/jobs/update-status', { ids, is_active })
    return response.data
  },

  bulkUpdateInternshipStatus: async (ids: string[], is_active: boolean): Promise<{ success: boolean; updated: number }> => {
    const response = await apiClient.post('/admin/bulk/internships/update-status', { ids, is_active })
    return response.data
  },
}
