import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import NetInfo from '@react-native-community/netinfo';
import { cacheData, getCachedData, queueOfflineAction } from './cacheManager';

const API_URL = process.env.EXPO_PUBLIC_BACKEND_URL;

// Create axios instance
const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Request interceptor to add auth token and handle offline requests
api.interceptors.request.use(
  async (config) => {
    // Add auth token
    const token = await AsyncStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    // Check if online
    const netInfo = await NetInfo.fetch();
    if (!netInfo.isConnected) {
      // If offline and it's a write operation, queue it
      if (config.method && ['post', 'put', 'delete'].includes(config.method.toLowerCase())) {
        await queueOfflineAction({
          type: config.method.toLowerCase() as 'create' | 'update' | 'delete',
          endpoint: config.url || '',
          data: config.data,
        });
        // Return a fake response
        throw new Error('OFFLINE_MODE');
      }
      
      // For GET requests, try to get cached data
      if (config.method?.toLowerCase() === 'get' && config.url) {
        const cacheKey = config.url;
        const cachedResponse = await getCachedData(cacheKey);
        if (cachedResponse) {
          // Return cached data as if it came from the server
          return Promise.reject({
            config,
            response: { data: cachedResponse },
            isOfflineCache: true,
          });
        }
      }
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle caching and errors
api.interceptors.response.use(
  async (response) => {
    // Cache GET responses
    if (response.config.method?.toLowerCase() === 'get' && response.config.url) {
      const cacheKey = response.config.url;
      await cacheData(cacheKey, response.data);
    }
    return response;
  },
  async (error) => {
    // Handle offline cache
    if (error.isOfflineCache) {
      return Promise.resolve(error.response);
    }

    // Handle offline mode
    if (error.message === 'OFFLINE_MODE') {
      return Promise.reject({
        message: 'You are offline. This action will be synced when you\'re back online.',
        isOffline: true,
      });
    }

    // Handle auth errors
    if (error.response?.status === 401) {
      // Token expired or invalid - clear auth data
      await AsyncStorage.removeItem('auth_token');
      await AsyncStorage.removeItem('user_data');
    }
    
    return Promise.reject(error);
  }
);

export default api;
