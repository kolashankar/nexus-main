import apiClient from './apiClient'

export interface Job {
  _id?: string
  title: string
  company: string
  description: string
  location: string
  job_type: string
  category: string
  salary_min?: number
  salary_max?: number
  currency: string
  experience_level: string
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

export interface JobsResponse {
  total: number
  skip: number
  limit: number
  jobs: Job[]
}

export const jobsApi = {
  // Get all jobs with filters
  getAll: async (params?: {
    skip?: number
    limit?: number
    search?: string
    category?: string
    job_type?: string
    experience_level?: string
    is_active?: boolean
    sort_by?: string
    sort_order?: number
  }): Promise<JobsResponse> => {
    const response = await apiClient.get('/admin/jobs', { params })
    return response.data
  },

  // Get single job
  getById: async (id: string): Promise<Job> => {
    const response = await apiClient.get(`/admin/jobs/${id}`)
    return response.data
  },

  // Create job manually
  create: async (job: Omit<Job, '_id' | 'created_at' | 'updated_at'>): Promise<Job> => {
    const response = await apiClient.post('/admin/jobs', job)
    return response.data
  },

  // Generate job with AI
  generateWithAI: async (params: {
    job_title: string
    company: string
    location: string
    job_type: string
    category: string
    experience_level: string
  }): Promise<Job> => {
    const response = await apiClient.post('/admin/jobs/generate-ai', null, { params })
    return response.data
  },

  // Update job
  update: async (id: string, job: Partial<Job>): Promise<Job> => {
    const response = await apiClient.put(`/admin/jobs/${id}`, job)
    return response.data
  },

  // Delete job
  delete: async (id: string): Promise<{ message: string; id: string }> => {
    const response = await apiClient.delete(`/admin/jobs/${id}`)
    return response.data
  },
}
