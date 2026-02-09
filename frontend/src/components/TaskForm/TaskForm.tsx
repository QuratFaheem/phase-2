// frontend/src/components/TaskForm/TaskForm.tsx
import React, { useState } from 'react';
import { Task, TaskCreate } from '@/types/task';
import { taskApi } from '@/services/api';

interface TaskFormProps {
  userId: string;
  onTaskCreated: (task: Task) => void;
}

const TaskForm: React.FC<TaskFormProps> = ({ userId, onTaskCreated }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    try {
      const newTask = await taskApi.createTask(userId, { title, description });
      onTaskCreated(newTask);
      setTitle('');
      setDescription('');
      setError(null);
    } catch (err) {
      setError('Failed to create task');
      console.error(err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="task-form">
      <h3>Add New Task</h3>
      {error && <div className="error">{error}</div>}
      <div className="form-group">
        <label htmlFor="title">Title:</label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter task title"
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="description">Description:</label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Enter task description (optional)"
        />
      </div>
      <button type="submit">Add Task</button>
    </form>
  );
};

export default TaskForm;