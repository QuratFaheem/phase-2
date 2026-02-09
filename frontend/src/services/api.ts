// frontend/src/services/api.ts
import axios from 'axios';

// Create an axios instance with base configuration
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
});

// Add a request interceptor to include the auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token might be expired, redirect to login
      localStorage.removeItem('access_token');
      window.location.href = '/auth/signin';
    }
    return Promise.reject(error);
  }
);

export default api;

// Task-related API functions
export const taskApi = {
  // Get all tasks for a user
  getTasks: async (userId: string, completed?: boolean, limit: number = 50, offset: number = 0) => {
    const params: any = { limit, offset };
    if (completed !== undefined) {
      params.completed = completed;
    }
    const response = await api.get(`/api/${userId}/tasks`, { params });
    return response.data;
  },

  // Create a new task
  createTask: async (userId: string, taskData: { title: string; description?: string }) => {
    const response = await api.post(`/api/${userId}/tasks`, taskData);
    return response.data;
  },

  // Get a specific task
  getTask: async (userId: string, taskId: string) => {
    const response = await api.get(`/api/${userId}/tasks/${taskId}`);
    return response.data;
  },

  // Update a task
  updateTask: async (userId: string, taskId: string, taskData: { title?: string; description?: string }) => {
    const response = await api.put(`/api/${userId}/tasks/${taskId}`, taskData);
    return response.data;
  },

  // Delete a task
  deleteTask: async (userId: string, taskId: string) => {
    const response = await api.delete(`/api/${userId}/tasks/${taskId}`);
    return response.data;
  },

  // Toggle task completion
  toggleTaskCompletion: async (userId: string, taskId: string, completed: boolean) => {
    const response = await api.patch(`/api/${userId}/tasks/${taskId}/complete`, {}, {
      params: { completed }
    });
    return response.data;
  },

  // Send a message to the chatbot
  sendMessage: async (userId: string, messageData: { message: string; conversation_id?: string }) => {
    const response = await api.post(`/api/${userId}/chat`, messageData);
    return response.data;
  },

  // Get chat history
  getChatHistory: async (userId: string, conversationId: string, limit: number = 50) => {
    const response = await api.get(`/api/${userId}/conversations/${conversationId}/messages`, {
      params: { limit }
    });
    return response.data;
  }
};

// Auth-related API functions
export const authApi = {
  // Sign up a new user
  signUp: async (userData: { email: string; password: string; name?: string }) => {
    const response = await api.post('/auth/signup', userData);
    return response.data;
  },

  // Sign in a user
  signIn: async (credentials: { email: string; password: string }) => {
    const response = await api.post('/auth/signin', credentials);
    return response.data;
  }
};