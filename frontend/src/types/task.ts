export interface Task {
  id: string;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
}

export interface TaskCreate {
  title: string;
  description?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
}