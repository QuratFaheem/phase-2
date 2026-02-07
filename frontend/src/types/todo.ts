// User-related types
export interface User {
  id: string;
  name: string;
  email: string;
  created_at: string;
}

export interface UserCredentials {
  email: string;
  password: string;
}

export interface UserRegistration extends UserCredentials {
  name: string;
}

// Todo-related types
export interface Todo {
  id: string;
  user_id: string;
  title: string;
  description?: string;
  status: 'pending' | 'in-progress' | 'completed';
  created_at: string;
  updated_at: string;
}

export interface TodoCreate {
  title: string;
  description?: string;
  status?: 'pending' | 'in-progress' | 'completed';
}

export interface TodoUpdate {
  title?: string;
  description?: string;
  status?: 'pending' | 'in-progress' | 'completed';
}

// API response types
export interface ApiResponse<T> {
  data?: T;
  error?: string;
}

// Authentication response type
export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}