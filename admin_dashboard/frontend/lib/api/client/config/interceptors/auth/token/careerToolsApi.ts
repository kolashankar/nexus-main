import apiClient from './apiClient'

export interface CareerToolTemplate {
  _id?: string
  tool_type: 'resume_review' | 'cover_letter' | 'ats_hack' | 'cold_email'
  name: string
  description: string
  prompt_template: string
  is_active: boolean
  created_at?: string
  updated_at?: string
}

export interface CareerToolUsage {
  _id?: string
  user_id: string
  tool_type: string
  input_data: any
  output_data: any
  created_at?: string
}

export interface CareerToolStats {
  total_usage: number
  usage_by_tool: {
    resume_review: number
    cover_letter: number
    ats_hack: number
    cold_email: number
  }
  recent_usage: CareerToolUsage[]
}

export const careerToolsApi = {
  // Template Management
  getTemplates: async (params?: {
    tool_type?: string
    is_active?: boolean
  }): Promise<{ success: boolean; templates: CareerToolTemplate[]; total: number }> => {
    const response = await apiClient.get('/admin/career-tools/templates', { params })
    return response.data
  },

  createTemplate: async (data: Omit<CareerToolTemplate, '_id' | 'created_at' | 'updated_at'>): Promise<{ success: boolean; template: CareerToolTemplate }> => {
    const response = await apiClient.post('/admin/career-tools/templates', data)
    return response.data
  },

  updateTemplate: async (id: string, data: Partial<CareerToolTemplate>): Promise<{ success: boolean; template: CareerToolTemplate }> => {
    const response = await apiClient.put(`/admin/career-tools/templates/${id}`, data)
    return response.data
  },

  deleteTemplate: async (id: string): Promise<{ success: boolean }> => {
    const response = await apiClient.delete(`/admin/career-tools/templates/${id}`)
    return response.data
  },

  // Statistics
  getStats: async (): Promise<{ success: boolean; stats: CareerToolStats }> => {
    const response = await apiClient.get('/admin/career-tools/stats')
    return response.data
  },

  // User-facing tools (for testing)
  resumeReview: async (data: { resume_text: string }): Promise<{ success: boolean; review: any }> => {
    const response = await apiClient.post('/career-tools/resume-review', data, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
    return response.data
  },

  coverLetter: async (data: { job_title: string; company: string; experience: string }): Promise<{ success: boolean; cover_letter: string }> => {
    const response = await apiClient.post('/career-tools/cover-letter', data, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
    return response.data
  },

  atsHack: async (data: { resume_text: string; job_description: string }): Promise<{ success: boolean; suggestions: any }> => {
    const response = await apiClient.post('/career-tools/ats-hack', data, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
    return response.data
  },

  coldEmail: async (data: { recipient_name: string; company: string; purpose: string }): Promise<{ success: boolean; email: string }> => {
    const response = await apiClient.post('/career-tools/cold-email', data, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    })
    return response.data
  },
}
