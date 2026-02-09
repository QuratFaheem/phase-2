// frontend/src/services/auth.ts
import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { authApi } from './api';
import { User } from '@/types/user';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => void;
  signUp: (email: string, password: string, name?: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if there's a token in localStorage on initial load
    const token = localStorage.getItem('access_token');
    if (token) {
      // In a real app, you would validate the token with an API call
      // For now, we'll just assume the user object is stored in localStorage too
      const storedUser = localStorage.getItem('user');
      if (storedUser) {
        setUser(JSON.parse(storedUser));
      }
    }
    setLoading(false);
  }, []);

  const signIn = async (email: string, password: string) => {
    try {
      const response = await authApi.signIn({ email, password });
      const { access_token, user: userData } = response.data;

      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user', JSON.stringify(userData));

      setUser(userData);
      // Use window.location to navigate instead of useRouter
      window.location.href = '/dashboard';
    } catch (error) {
      throw error;
    }
  };

  const signOut = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    setUser(null);
    // Use window.location to navigate instead of useRouter
    window.location.href = '/auth/signin';
  };

  const signUp = async (email: string, password: string, name?: string) => {
    try {
      const response = await authApi.signUp({ email, password, name });
      const { access_token, user: userData } = response.data;

      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user', JSON.stringify(userData));

      setUser(userData);
      // Use window.location to navigate instead of useRouter
      window.location.href = '/dashboard';
    } catch (error) {
      throw error;
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, signIn, signOut, signUp }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};