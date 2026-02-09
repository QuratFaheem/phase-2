// frontend/src/components/TaskItem/TaskItem.tsx
import React, { useState } from 'react';
import { Task } from '@/types/task';
import { taskApi } from '@/services/api';

interface TaskItemProps {
  task: Task;
  onTaskUpdated: (task: Task) => void;
  onTaskDeleted: (taskId: string) => void;
  onToggleCompletion: (taskId: string, completed: boolean) => void;
  userId: string;
}

const TaskItem: React.FC<TaskItemProps> = ({
  task,
  onTaskUpdated,
  onTaskDeleted,
  onToggleCompletion,
  userId
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');

  const handleSave = async () => {
    try {
      const updatedTask = await taskApi.updateTask(userId, task.id, { title, description });
      onTaskUpdated(updatedTask);
      setIsEditing(false);
    } catch (err) {
      console.error('Failed to update task:', err);
    }
  };

  const handleCancel = () => {
    setTitle(task.title);
    setDescription(task.description || '');
    setIsEditing(false);
  };

  const handleDelete = async () => {
    try {
      await taskApi.deleteTask(userId, task.id);
      onTaskDeleted(task.id);
    } catch (err) {
      console.error('Failed to delete task:', err);
    }
  };

  const handleToggleCompletion = async () => {
    onToggleCompletion(task.id, !task.completed);
  };

  return (
    <li className={`task-item ${task.completed ? 'completed' : ''}`}>
      {isEditing ? (
        <div className="edit-form">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="edit-title"
          />
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="edit-description"
          />
          <div className="edit-actions">
            <button onClick={handleSave}>Save</button>
            <button onClick={handleCancel}>Cancel</button>
          </div>
        </div>
      ) : (
        <div className="task-content">
          <div className="task-header">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={handleToggleCompletion}
              className="completion-checkbox"
            />
            <h3 className={task.completed ? 'completed-title' : ''}>{task.title}</h3>
            <div className="task-actions">
              <button onClick={() => setIsEditing(true)}>Edit</button>
              <button onClick={handleDelete}>Delete</button>
            </div>
          </div>
          {task.description && (
            <p className="task-description">{task.description}</p>
          )}
          <div className="task-meta">
            <small>Created: {new Date(task.created_at).toLocaleString()}</small>
            <small>Updated: {new Date(task.updated_at).toLocaleString()}</small>
          </div>
        </div>
      )}
    </li>
  );
};

export default TaskItem;