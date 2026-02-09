// frontend/src/app/dashboard/page.tsx
'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import TaskList from '@/components/TaskList/TaskList';
import { useAuth } from '@/services/auth';

const DashboardPage = () => {
  const router = useRouter();
  const { user, loading } = useAuth();

  useEffect(() => {
    if (!loading && !user) {
      router.push('/auth/signin');
    }
  }, [user, loading, router]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!user) {
    return null; // Redirect handled by useEffect
  }

  return (
    <div className="dashboard">
      <header>
        <nav className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex">
                <div className="flex-shrink-0 flex items-center">
                  <span className="text-indigo-600 font-bold text-xl">TodoApp</span>
                </div>
                <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                  <a
                    href="/dashboard"
                    className="border-indigo-500 text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                  >
                    Tasks
                  </a>
                  <a
                    href="/chat"
                    className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                  >
                    AI Chat
                  </a>
                </div>
              </div>
              <div className="flex items-center">
                <div className="ml-3 relative">
                  <div>
                    <button className="bg-white flex text-sm rounded-full focus:outline-none">
                      <span className="sr-only">Open user menu</span>
                      <span className="inline-block h-8 w-8 rounded-full overflow-hidden bg-gray-100">
                        <svg className="h-full w-full text-gray-300" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M24 20.993V24H0v-2.996A14.977 14.977 0 0112.004 15c4.904 0 9.26 2.354 12 5.993zM16.002 8.999a4 4 0 11-8 0 4 4 0 018 0z" />
                        </svg>
                      </span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </nav>
      </header>
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <h1>Dashboard</h1>
        <p>Welcome, {user.name || user.email}!</p>
        <TaskList userId={user.id} />
      </main>
    </div>
  );
};

export default DashboardPage;