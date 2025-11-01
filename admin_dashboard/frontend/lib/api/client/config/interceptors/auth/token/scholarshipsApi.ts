import apiClient from './apiClient'

export interface Scholarship {
  _id?: string
  title: string
  provider: string
  description: string
  scholarship_type: string
  education_level: string
  country: string
  amount_min?: number
  amount_max?: number
  currency: string
  eligibility_criteria: string[]
  application_requirements: string[]
  benefits: string[]
  application_deadline?: string
  apply_link?: string
  is_active: boolean
  created_at?: string
  updated_at?: string
}

export interface ScholarshipsResponse {
  total: number
  skip: number
  limit: number
  scholarships: Scholarship[]
}

export const scholarshipsApi = {
  // Get all scholarships with filters
  getAll: async (params?: {
    skip?: number
    limit?: number
    search?: string
    scholarship_type?: string
    education_level?: string
    country?: string
    is_active?: boolean
    sort_by?: string
    sort_order?: number
  }): Promise<ScholarshipsResponse> => {
    const response = await apiClient.get('/admin/scholarships', { params })
    return response.data
  },

  // Get single scholarship
  getById: async (id: string): Promise<Scholarship> => {
    const response = await apiClient.get(`/admin/scholarships/${id}`)
    return response.data
  },

  // Create scholarship manually
  create: async (scholarship: Omit<Scholarship, '_id' | 'created_at' | 'updated_at'>): Promise<Scholarship> => {
    const response = await apiClient.post('/admin/scholarships', scholarship)
    return response.data
  },

  // Generate scholarship with AI
  generateWithAI: async (params: {
    title: string
    provider: string
    country: string
    education_level: string
  }): Promise<Scholarship> => {
    const response = await apiClient.post('/admin/scholarships/generate-ai', null, { params })
    return response.data
  },

  // Update scholarship
  update: async (id: string, scholarship: Partial<Scholarship>): Promise<Scholarship> => {
    const response = await apiClient.put(`/admin/scholarships/${id}`, scholarship)
    return response.data
  },

  // Delete scholarship
  delete: async (id: string): Promise<{ message: string; id: string }> => {
    const response = await apiClient.delete(`/admin/scholarships/${id}`)
    return response.data
  },
}
