// frontend/src/components/ProtectedRoute/ProtectedRoute.tsx
import React from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/services/auth';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { user, loading } = useAuth();
  const router = useRouter();

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!user) {
    // Redirect to login if not authenticated
    router.push('/auth/signin');
    return null;
  }

  return <>{children}</>;
};

export default ProtectedRoute;