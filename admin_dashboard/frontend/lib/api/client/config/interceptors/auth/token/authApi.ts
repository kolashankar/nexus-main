import apiClient from './apiClient'

export interface User {
  _id?: string
  email: string
  name: string
  role: 'admin' | 'sub_admin' | 'user'
  is_active?: boolean
  created_at?: string
}

export interface LoginResponse {
  success: boolean
  access_token: string
  token_type: string
  user_type: string
  user_id: string
  email: string
  full_name: string
  role?: string
}

export interface RegisterData {
  email: string
  password: string
  name: string
  role?: 'admin' | 'sub_admin'
}

export interface LoginData {
  email: string
  password: string
}

export const authApi = {
  // Admin Authentication
  adminRegister: async (data: RegisterData): Promise<LoginResponse> => {
    const response = await apiClient.post('/auth/admin/register', data)
    return response.data
  },

  adminLogin: async (data: LoginData): Promise<LoginResponse> => {
    const response = await apiClient.post('/auth/admin/login', data)
    return response.data
  },

  // User Authentication (for testing)
  userRegister: async (data: Omit<RegisterData, 'role'>): Promise<LoginResponse> => {
    const response = await apiClient.post('/auth/user/register', data)
    return response.data
  },

  userLogin: async (data: LoginData): Promise<LoginResponse> => {
    const response = await apiClient.post('/auth/user/login', data)
    return response.data
  },

  // Profile Management
  getProfile: async (token: string): Promise<{ success: boolean; user: User }> => {
    const response = await apiClient.get('/auth/me', {
      headers: { Authorization: `Bearer ${token}` }
    })
    return response.data
  },

  updateProfile: async (token: string, data: Partial<User>): Promise<{ success: boolean; user: User }> => {
    const response = await apiClient.put('/auth/profile', data, {
      headers: { Authorization: `Bearer ${token}` }
    })
    return response.data
  },

  changePassword: async (token: string, data: {
    current_password: string
    new_password: string
  }): Promise<{ success: boolean }> => {
    const response = await apiClient.post('/auth/change-password', data, {
      headers: { Authorization: `Bearer ${token}` }
    })
    return response.data
  },
}
