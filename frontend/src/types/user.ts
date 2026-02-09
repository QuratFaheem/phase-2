export interface User {
  id: string;
  email: string;
  name?: string;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
}