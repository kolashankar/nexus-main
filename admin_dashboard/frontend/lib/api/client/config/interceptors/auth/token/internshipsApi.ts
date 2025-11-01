import apiClient from './apiClient'

export interface Internship {
  _id?: string
  title: string
  company: string
  description: string
  location: string
  internship_type: string
  category: string
  duration: string
  stipend_min?: number
  stipend_max?: number
  currency: string
  skills_required: string[]
  qualifications: string[]
  responsibilities: string[]
  benefits: string[]
  application_deadline?: string
  company_logo?: string
  apply_link?: string
  is_active: boolean
  created_at?: string
  updated_at?: string
}

export interface InternshipsResponse {
  total: number
  skip: number
  limit: number
  internships: Internship[]
}

export const internshipsApi = {
  // Get all internships with filters
  getAll: async (params?: {
    skip?: number
    limit?: number
    search?: string
    category?: string
    internship_type?: string
    is_active?: boolean
    sort_by?: string
    sort_order?: number
  }): Promise<InternshipsResponse> => {
    const response = await apiClient.get('/admin/internships', { params })
    return response.data
  },

  // Get single internship
  getById: async (id: string): Promise<Internship> => {
    const response = await apiClient.get(`/admin/internships/${id}`)
    return response.data
  },

  // Create internship manually
  create: async (internship: Omit<Internship, '_id' | 'created_at' | 'updated_at'>): Promise<Internship> => {
    const response = await apiClient.post('/admin/internships', internship)
    return response.data
  },

  // Generate internship with AI
  generateWithAI: async (params: {
    title: string
    company: string
    location: string
    duration: string
    category: string
  }): Promise<Internship> => {
    const response = await apiClient.post('/admin/internships/generate-ai', null, { params })
    return response.data
  },

  // Update internship
  update: async (id: string, internship: Partial<Internship>): Promise<Internship> => {
    const response = await apiClient.put(`/admin/internships/${id}`, internship)
    return response.data
  },

  // Delete internship
  delete: async (id: string): Promise<{ message: string; id: string }> => {
    const response = await apiClient.delete(`/admin/internships/${id}`)
    return response.data
  },
}
