import apiClient from './apiClient'

export interface RoadmapNode {
  id: string
  title: string
  description: string
  type: 'content' | 'roadmap_link' | 'article_link'
  position_x: number
  position_y: number
  connections: string[]
  metadata?: {
    roadmap_id?: string
    article_id?: string
    estimated_time?: string
  }
}

export interface Roadmap {
  _id?: string
  title: string
  description: string
  category: string
  level: string
  nodes: RoadmapNode[]
  author: string
  tags: string[]
  estimated_duration: string
  is_published: boolean
  views_count?: number
  created_at?: string
  updated_at?: string
}

export interface RoadmapListResponse {
  success: boolean
  roadmaps: Roadmap[]
  total: number
  page: number
  limit: number
}

export const roadmapsApi = {
  getAll: async (params?: {
    search?: string
    category?: string
    level?: string
    is_published?: boolean
    page?: number
    limit?: number
  }): Promise<RoadmapListResponse> => {
    const response = await apiClient.get('/admin/roadmaps', { params })
    return response.data
  },

  getById: async (id: string): Promise<{ success: boolean; roadmap: Roadmap }> => {
    const response = await apiClient.get(`/admin/roadmaps/${id}`)
    return response.data
  },

  create: async (data: Omit<Roadmap, '_id' | 'created_at' | 'updated_at' | 'views_count'>): Promise<{ success: boolean; roadmap: Roadmap }> => {
    const response = await apiClient.post('/admin/roadmaps', data)
    return response.data
  },

  generateAI: async (data: {
    title: string
    category: string
    level: string
    focus_areas?: string[]
  }): Promise<{ success: boolean; roadmap: Roadmap }> => {
    const response = await apiClient.post('/admin/roadmaps/generate-ai', data)
    return response.data
  },

  update: async (id: string, data: Partial<Roadmap>): Promise<{ success: boolean; roadmap: Roadmap }> => {
    const response = await apiClient.put(`/admin/roadmaps/${id}`, data)
    return response.data
  },

  delete: async (id: string): Promise<{ success: boolean }> => {
    const response = await apiClient.delete(`/admin/roadmaps/${id}`)
    return response.data
  },

  togglePublish: async (id: string): Promise<{ success: boolean; roadmap: Roadmap }> => {
    const response = await apiClient.post(`/admin/roadmaps/${id}/toggle-publish`)
    return response.data
  },

  addNode: async (id: string, node: Omit<RoadmapNode, 'id'>): Promise<{ success: boolean; roadmap: Roadmap }> => {
    const response = await apiClient.post(`/admin/roadmaps/${id}/nodes`, node)
    return response.data
  },

  updateNode: async (id: string, nodeId: string, node: Partial<RoadmapNode>): Promise<{ success: boolean; roadmap: Roadmap }> => {
    const response = await apiClient.put(`/admin/roadmaps/${id}/nodes/${nodeId}`, node)
    return response.data
  },

  deleteNode: async (id: string, nodeId: string): Promise<{ success: boolean; roadmap: Roadmap }> => {
    const response = await apiClient.delete(`/admin/roadmaps/${id}/nodes/${nodeId}`)
    return response.data
  },

  getStats: async (): Promise<{ success: boolean; stats: any }> => {
    const response = await apiClient.get('/admin/roadmaps/stats')
    return response.data
  },
}
