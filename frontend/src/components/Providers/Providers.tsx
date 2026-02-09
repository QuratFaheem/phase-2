// frontend/src/components/Providers/Providers.tsx
'use client';

import React, { ReactNode } from 'react';
import { AuthProvider } from '@/services/auth';

interface ProvidersProps {
  children: ReactNode;
}

export default function Providers({ children }: ProvidersProps) {
  return (
    <AuthProvider>
      {children}
    </AuthProvider>
  );
}