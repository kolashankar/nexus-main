import axios, { AxiosInstance, AxiosError } from 'axios';
import { toast } from 'react-hot-toast';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor - Add JWT token
    this.client.interceptors.request.use(
      (config) => {
        const token = this.getToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor - Handle errors
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response) {
          const status = error.response.status;
          const data: any = error.response.data;

          if (status === 401) {
            this.removeToken();
            if (typeof window !== 'undefined') {
              window.location.href = '/login';
            }
          }

          const message = data?.detail || data?.message || 'An error occurred';
          toast.error(message);
        } else if (error.request) {
          toast.error('Network error. Please check your connection.');
        }

        return Promise.reject(error);
      }
    );
  }

  private getToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('token');
  }

  private removeToken(): void {
    if (typeof window === 'undefined') return;
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }

  // Auth APIs
  async register(data: { email: string; password: string; full_name: string }) {
    const response = await this.client.post('/auth/user/register', data);
    return response.data;
  }

  async login(data: { email: string; password: string }) {
    const response = await this.client.post('/auth/user/login', data);
    return response.data;
  }

  async getProfile() {
    const response = await this.client.get('/auth/me');
    return response.data;
  }

  // Jobs APIs
  async getJobs(params?: any) {
    const response = await this.client.get('/user/jobs', { params });
    return response.data;
  }

  async getJobById(id: string) {
    const response = await this.client.get(`/user/jobs/${id}`);
    return response.data;
  }

  // Internships APIs
  async getInternships(params?: any) {
    const response = await this.client.get('/user/internships', { params });
    return response.data;
  }

  async getInternshipById(id: string) {
    const response = await this.client.get(`/user/internships/${id}`);
    return response.data;
  }

  // Scholarships APIs
  async getScholarships(params?: any) {
    const response = await this.client.get('/user/scholarships', { params });
    return response.data;
  }

  async getScholarshipById(id: string) {
    const response = await this.client.get(`/user/scholarships/${id}`);
    return response.data;
  }

  // Articles APIs
  async getArticles(params?: any) {
    const response = await this.client.get('/user/articles', { params });
    return response.data;
  }

  async getArticleById(id: string) {
    const response = await this.client.get(`/user/articles/${id}`);
    return response.data;
  }

  // DSA Topics APIs
  async getDSATopics(params?: any) {
    const response = await this.client.get('/user/dsa/topics', { params });
    return response.data;
  }

  async getDSATopicById(id: string) {
    const response = await this.client.get(`/user/dsa/topics/${id}`);
    return response.data;
  }

  // DSA Questions APIs
  async getDSAQuestions(params?: any) {
    const response = await this.client.get('/user/dsa/questions', { params });
    return response.data;
  }

  async getDSAQuestionById(id: string) {
    const response = await this.client.get(`/user/dsa/questions/${id}`);
    return response.data;
  }

  async submitDSAQuestion(id: string, data: any) {
    const response = await this.client.post(`/user/dsa/questions/${id}/submit`, data);
    return response.data;
  }

  // DSA Sheets APIs
  async getDSASheets(params?: any) {
    const response = await this.client.get('/user/dsa/sheets', { params });
    return response.data;
  }

  async getDSASheetById(id: string) {
    const response = await this.client.get(`/user/dsa/sheets/${id}`);
    return response.data;
  }

  // DSA Companies APIs
  async getDSACompanies(params?: any) {
    const response = await this.client.get('/user/dsa/companies', { params });
    return response.data;
  }

  async getDSACompanyById(id: string) {
    const response = await this.client.get(`/user/dsa/companies/${id}`);
    return response.data;
  }

  // DSA Dashboard APIs
  async getDSADashboard() {
    const response = await this.client.get('/user/dsa/dashboard');
    return response.data;
  }

  // Roadmaps APIs
  async getRoadmaps(params?: any) {
    const response = await this.client.get('/user/roadmaps', { params });
    return response.data;
  }

  async getRoadmapById(id: string) {
    const response = await this.client.get(`/user/roadmaps/${id}`);
    return response.data;
  }

  // Scholarships APIs
  async getScholarships(params?: any) {
    const response = await this.client.get('/user/scholarships', { params });
    return response.data;
  }

  async getScholarshipById(id: string) {
    const response = await this.client.get(`/user/scholarships/${id}`);
    return response.data;
  }
}

export const apiClient = new ApiClient();
export const api = apiClient; // Alias for compatibility