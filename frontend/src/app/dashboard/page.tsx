'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Todo, TodoCreate, TodoUpdate } from '../../types/todo';
import { todoService, authService } from '../../lib/api';
import { authStore, authActions } from '../../lib/auth';

export default function DashboardPage() {
  const router = useRouter();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [newTodo, setNewTodo] = useState<Omit<TodoCreate, 'userId'>>({ title: '', description: '', status: 'pending' });
  const [editingTodo, setEditingTodo] = useState<Todo | null>(null);
  const [editForm, setEditForm] = useState<TodoUpdate>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Check authentication on mount
  useEffect(() => {
    if (!authStore.isAuthenticated()) {
      router.push('/auth/signin');
    } else {
      loadTodos();
    }
  }, []);

  const loadTodos = async () => {
    try {
      setLoading(true);
      const todosData = await todoService.getTodos();
      setTodos(todosData);
    } catch (err: any) {
      setError(err.message || 'Failed to load todos');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTodo = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const createdTodo = await todoService.createTodo(newTodo);
      setTodos([...todos, createdTodo]);
      setNewTodo({ title: '', description: '', status: 'pending' });
    } catch (err: any) {
      setError(err.message || 'Failed to create todo');
    }
  };

  const handleUpdateTodo = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingTodo) return;

    try {
      const updatedTodo = await todoService.updateTodo(editingTodo.id, editForm);
      setTodos(todos.map(todo => todo.id === updatedTodo.id ? updatedTodo : todo));
      setEditingTodo(null);
      setEditForm({});
    } catch (err: any) {
      setError(err.message || 'Failed to update todo');
    }
  };

  const handleDeleteTodo = async (id: string) => {
    try {
      await todoService.deleteTodo(id);
      setTodos(todos.filter(todo => todo.id !== id));
    } catch (err: any) {
      setError(err.message || 'Failed to delete todo');
    }
  };

  const startEditing = (todo: Todo) => {
    setEditingTodo(todo);
    setEditForm({
      title: todo.title,
      description: todo.description,
      status: todo.status
    });
  };

  const cancelEditing = () => {
    setEditingTodo(null);
    setEditForm({});
  };

  const handleSignOut = () => {
    authActions.signOut();
    router.push('/auth/signin');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading your todos...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">Todo Dashboard</h1>
            </div>
            <div className="flex items-center">
              <button
                onClick={handleSignOut}
                className="ml-4 px-3 py-2 rounded-md text-sm font-medium text-white bg-red-600 hover:bg-red-700"
              >
                Sign out
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {error && (
            <div className="rounded-md bg-red-50 p-4 mb-4">
              <div className="text-sm text-red-700">{error}</div>
            </div>
          )}

          {/* Create Todo Form */}
          <div className="bg-white shadow overflow-hidden sm:rounded-lg mb-6">
            <div className="px-4 py-5 sm:px-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900">Create New Todo</h3>
            </div>
            <div className="border-t border-gray-200 px-4 py-5 sm:p-6">
              <form onSubmit={handleCreateTodo}>
                <div className="grid grid-cols-6 gap-6">
                  <div className="col-span-6">
                    <label htmlFor="title" className="block text-sm font-medium text-gray-700">
                      Title *
                    </label>
                    <input
                      type="text"
                      name="title"
                      id="title"
                      required
                      value={newTodo.title}
                      onChange={(e) => setNewTodo({...newTodo, title: e.target.value})}
                      className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    />
                  </div>

                  <div className="col-span-6">
                    <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                      Description
                    </label>
                    <textarea
                      id="description"
                      name="description"
                      rows={3}
                      value={newTodo.description}
                      onChange={(e) => setNewTodo({...newTodo, description: e.target.value})}
                      className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 mt-1 block w-full sm:text-sm border border-gray-300 rounded-md"
                    />
                  </div>

                  <div className="col-span-6 sm:col-span-3">
                    <label htmlFor="status" className="block text-sm font-medium text-gray-700">
                      Status
                    </label>
                    <select
                      id="status"
                      name="status"
                      value={newTodo.status}
                      onChange={(e) => setNewTodo({...newTodo, status: e.target.value as 'pending' | 'in-progress' | 'completed'})}
                      className="mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    >
                      <option value="pending">Pending</option>
                      <option value="in-progress">In Progress</option>
                      <option value="completed">Completed</option>
                    </select>
                  </div>

                  <div className="col-span-6">
                    <button
                      type="submit"
                      className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                      Create Todo
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </div>

          {/* Todo List */}
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:px-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900">Your Todos ({todos.length})</h3>
            </div>
            <div className="border-t border-gray-200">
              {todos.length === 0 ? (
                <div className="px-4 py-5 sm:p-6 text-center">
                  <p className="text-gray-500">You don't have any todos yet. Create one above!</p>
                </div>
              ) : (
                <ul className="divide-y divide-gray-200">
                  {todos.map((todo) => (
                    <li key={todo.id}>
                      {editingTodo?.id === todo.id ? (
                        // Edit form for this todo
                        <form onSubmit={handleUpdateTodo} className="px-4 py-5 sm:px-6 bg-blue-50">
                          <div className="grid grid-cols-6 gap-6">
                            <div className="col-span-6">
                              <label htmlFor={`edit-title-${todo.id}`} className="block text-sm font-medium text-gray-700">
                                Title *
                              </label>
                              <input
                                type="text"
                                id={`edit-title-${todo.id}`}
                                name="title"
                                value={editForm.title}
                                onChange={(e) => setEditForm({...editForm, title: e.target.value})}
                                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                              />
                            </div>

                            <div className="col-span-6">
                              <label htmlFor={`edit-description-${todo.id}`} className="block text-sm font-medium text-gray-700">
                                Description
                              </label>
                              <textarea
                                id={`edit-description-${todo.id}`}
                                name="description"
                                rows={2}
                                value={editForm.description || ''}
                                onChange={(e) => setEditForm({...editForm, description: e.target.value})}
                                className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 mt-1 block w-full sm:text-sm border border-gray-300 rounded-md"
                              />
                            </div>

                            <div className="col-span-6 sm:col-span-3">
                              <label htmlFor={`edit-status-${todo.id}`} className="block text-sm font-medium text-gray-700">
                                Status
                              </label>
                              <select
                                id={`edit-status-${todo.id}`}
                                name="status"
                                value={editForm.status || todo.status}
                                onChange={(e) => setEditForm({...editForm, status: e.target.value as 'pending' | 'in-progress' | 'completed'})}
                                className="mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                              >
                                <option value="pending">Pending</option>
                                <option value="in-progress">In Progress</option>
                                <option value="completed">Completed</option>
                              </select>
                            </div>

                            <div className="col-span-6">
                              <button
                                type="submit"
                                className="inline-flex justify-center mr-2 py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                              >
                                Save
                              </button>
                              <button
                                type="button"
                                onClick={cancelEditing}
                                className="inline-flex justify-center py-2 px-4 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                              >
                                Cancel
                              </button>
                            </div>
                          </div>
                        </form>
                      ) : (
                        // Display todo
                        <div className="px-4 py-5 sm:px-6">
                          <div className="flex justify-between">
                            <div>
                              <h4 className="text-lg font-medium text-gray-900">{todo.title}</h4>
                              <p className="mt-1 text-sm text-gray-500">{todo.description}</p>
                              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                                todo.status === 'pending' 
                                  ? 'bg-yellow-100 text-yellow-800' 
                                  : todo.status === 'in-progress' 
                                    ? 'bg-blue-100 text-blue-800' 
                                    : 'bg-green-100 text-green-800'
                              }`}>
                                {todo.status}
                              </span>
                            </div>
                            <div className="flex space-x-2">
                              <button
                                onClick={() => startEditing(todo)}
                                className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                              >
                                Edit
                              </button>
                              <button
                                onClick={() => handleDeleteTodo(todo.id)}
                                className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                              >
                                Delete
                              </button>
                            </div>
                          </div>
                          <div className="mt-2 text-xs text-gray-500">
                            Created: {new Date(todo.created_at).toLocaleString()}
                          </div>
                        </div>
                      )}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}