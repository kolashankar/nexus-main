import apiClient from './apiClient'

export const bulkApi = {
  // Jobs
  exportJobs: (params?: any) => apiClient.get('/admin/bulk/jobs/export', { params, responseType: 'blob' }),
  importJobs: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return apiClient.post('/admin/bulk/jobs/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  deleteJobs: (ids: string[]) => apiClient.post('/admin/bulk/jobs/delete', { ids }),
  updateJobsStatus: (ids: string[], status: boolean) => apiClient.post('/admin/bulk/jobs/update-status', { ids, is_active: status }),
  
  // Internships
  exportInternships: (params?: any) => apiClient.get('/admin/bulk/internships/export', { params, responseType: 'blob' }),
  importInternships: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return apiClient.post('/admin/bulk/internships/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  deleteInternships: (ids: string[]) => apiClient.post('/admin/bulk/internships/delete', { ids }),
  updateInternshipsStatus: (ids: string[], status: boolean) => apiClient.post('/admin/bulk/internships/update-status', { ids, is_active: status }),
}
