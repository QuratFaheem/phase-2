import { Task } from './task';

export interface Conversation {
  id: string;
  user_id: string;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
}

export interface Message {
  id: string;
  conversation_id: string;
  user_id: string;
  role: 'user' | 'assistant';
  content: string;
  created_at: string; // ISO date string
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
}

export interface ChatResponse {
  success: boolean;
  data: {
    conversation_id: string;
    response: string;
    tool_calls: Array<{
      tool_name: string;
      arguments: Record<string, any>;
      result: any;
    }>;
    timestamp: number;
  };
}