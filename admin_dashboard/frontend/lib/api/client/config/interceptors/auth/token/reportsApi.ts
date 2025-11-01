import apiClient from './apiClient'

export const reportsApi = {
  // Report Builder
  buildReport: (config: any) => apiClient.post('/admin/reports/build', config),
  
  // Scheduled Reports
  getScheduled: () => apiClient.get('/admin/reports/scheduled'),
  createScheduled: (data: any) => apiClient.post('/admin/reports/scheduled', data),
  updateScheduled: (id: string, data: any) => apiClient.put(`/admin/reports/scheduled/${id}`, data),
  deleteScheduled: (id: string) => apiClient.delete(`/admin/reports/scheduled/${id}`),
  
  // Email Reports
  emailReport: (reportId: string, emails: string[]) => 
    apiClient.post(`/admin/reports/${reportId}/email`, { emails }),
  
  // Export
  exportPDF: (reportData: any) => 
    apiClient.post('/admin/reports/export/pdf', reportData, { responseType: 'blob' }),
  exportCSV: (reportData: any) => 
    apiClient.post('/admin/reports/export/csv', reportData, { responseType: 'blob' }),
}
