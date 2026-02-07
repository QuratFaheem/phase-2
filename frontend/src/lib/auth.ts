import { User, UserRegistration, UserCredentials, AuthResponse } from '../types/todo';
import { authService } from './api';

// Store the current user and token
let currentUser: User | null = null;
let accessToken: string | null = null;

export const authStore = {
  // Get the current user
  getUser(): User | null {
    if (!currentUser) {
      const userStr = localStorage.getItem('user');
      if (userStr) {
        currentUser = JSON.parse(userStr);
      }
    }
    return currentUser;
  },

  // Get the access token
  getToken(): string | null {
    if (!accessToken) {
      accessToken = localStorage.getItem('access_token');
    }
    return accessToken;
  },

  // Set the current user and token
  setUser(userData: AuthResponse) {
    currentUser = userData.user;
    accessToken = userData.access_token;
    
    // Store in localStorage for persistence
    localStorage.setItem('user', JSON.stringify(currentUser));
    localStorage.setItem('access_token', accessToken);
  },

  // Clear the current user and token
  clearUser() {
    currentUser = null;
    accessToken = null;
    
    // Remove from localStorage
    localStorage.removeItem('user');
    localStorage.removeItem('access_token');
  },

  // Check if user is authenticated
  isAuthenticated(): boolean {
    return !!this.getToken();
  },
};

export const authActions = {
  // Register a new user
  async register(userData: UserRegistration): Promise<User> {
    try {
      const response = await authService.register(userData);
      authStore.setUser(response);
      return response.user;
    } catch (error) {
      throw error;
    }
  },

  // Sign in a user
  async signIn(credentials: UserCredentials): Promise<User> {
    try {
      const response = await authService.signIn(credentials);
      authStore.setUser(response);
      return response.user;
    } catch (error) {
      throw error;
    }
  },

  // Sign out the current user
  signOut() {
    authStore.clearUser();
  },
};