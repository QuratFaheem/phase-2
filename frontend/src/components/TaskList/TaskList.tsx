// frontend/src/components/TaskList/TaskList.tsx
import React, { useState, useEffect } from 'react';
import { Task } from '@/types/task';
import { taskApi } from '@/services/api';
import TaskItem from '../TaskItem/TaskItem';
import TaskForm from '../TaskForm/TaskForm';

interface TaskListProps {
  userId: string;
}

const TaskList: React.FC<TaskListProps> = ({ userId }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const tasksData = await taskApi.getTasks(userId);
      setTasks(tasksData);
    } catch (err) {
      setError('Failed to fetch tasks');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleTaskCreated = (newTask: Task) => {
    setTasks([...tasks, newTask]);
  };

  const handleTaskUpdated = (updatedTask: Task) => {
    setTasks(tasks.map(task => task.id === updatedTask.id ? updatedTask : task));
  };

  const handleTaskDeleted = (taskId: string) => {
    setTasks(tasks.filter(task => task.id !== taskId));
  };

  const handleToggleCompletion = async (taskId: string, completed: boolean) => {
    try {
      const updatedTask = await taskApi.toggleTaskCompletion(userId, taskId, completed);
      setTasks(tasks.map(task => task.id === taskId ? updatedTask : task));
    } catch (err) {
      setError('Failed to update task completion status');
      console.error(err);
    }
  };

  if (loading) return <div className="loading">Loading tasks...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="task-list-container">
      <h2>Your Tasks</h2>
      <TaskForm userId={userId} onTaskCreated={handleTaskCreated} />
      
      {tasks.length === 0 ? (
        <p className="no-tasks-message">No tasks yet. Add your first task above!</p>
      ) : (
        <div className="tasks-grid">
          {tasks.map(task => (
            <TaskItem
              key={task.id}
              task={task}
              onTaskUpdated={handleTaskUpdated}
              onTaskDeleted={handleTaskDeleted}
              onToggleCompletion={handleToggleCompletion}
              userId={userId}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default TaskList;