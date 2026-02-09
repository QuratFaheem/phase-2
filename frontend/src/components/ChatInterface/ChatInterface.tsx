// frontend/src/components/ChatInterface/ChatInterface.tsx
import React, { useState, useRef, useEffect } from 'react';
import { Message, ChatRequest, ChatResponse } from '@/types/conversation';
import { taskApi } from '@/services/api';
import { Task } from '@/types/task';

interface ChatInterfaceProps {
  userId: string;
  onTaskUpdated?: (task: Task) => void;
  onTaskCreated?: (task: Task) => void;
  onTaskDeleted?: (taskId: string) => void;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ userId, onTaskUpdated, onTaskCreated, onTaskDeleted }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom of messages when new messages arrive
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    try {
      setIsLoading(true);
      setError(null);

      // Add user message to UI immediately
      const userMessage: Message = {
        id: Date.now().toString(), // Temporary ID
        conversation_id: conversationId || '',
        user_id: userId,
        role: 'user',
        content: inputValue,
        created_at: new Date().toISOString(),
      };

      setMessages(prev => [...prev, userMessage]);
      const messageToSend = inputValue;
      setInputValue('');

      // Prepare the request
      const request: ChatRequest = {
        message: messageToSend,
        conversation_id: conversationId || undefined,
      };

      // Send to backend
      const response: ChatResponse = await taskApi.sendMessage(userId, request);

      if (response.success) {
        // Update conversation ID if it was created
        if (!conversationId) {
          setConversationId(response.data.conversation_id);
        }

        // Add AI response to messages
        const aiMessage: Message = {
          id: Date.now().toString(), // Temporary ID
          conversation_id: response.data.conversation_id,
          user_id: userId,
          role: 'assistant',
          content: response.data.response,
          created_at: new Date(response.data.timestamp * 1000).toISOString(), // Convert Unix timestamp
        };

        setMessages(prev => [...prev, aiMessage]);

        // Handle any tool calls that affected tasks
        response.data.tool_calls.forEach(call => {
          if (call.tool_name.includes('task')) {
            // Trigger callbacks to update task list in parent components
            switch (call.tool_name) {
              case 'create_task':
                if (onTaskCreated && call.result.id) {
                  onTaskCreated(call.result as Task);
                }
                break;
              case 'update_task':
                if (onTaskUpdated && call.result.id) {
                  onTaskUpdated(call.result as Task);
                }
                break;
              case 'delete_task':
                if (onTaskDeleted && call.result.id) {
                  onTaskDeleted(call.result.id);
                }
                break;
              case 'toggle_task':
                if (onTaskUpdated && call.result.id) {
                  onTaskUpdated(call.result as Task);
                }
                break;
              default:
                console.log('Tool call result:', call.result);
            }
          }
        });
      } else {
        setError('Failed to get response from AI');
      }
    } catch (err) {
      setError('Error sending message: ' + (err as Error).message);
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="chat-interface">
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <h3>Hello! How can I help you with your tasks today?</h3>
            <p>You can ask me to create, update, or manage your tasks.</p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`message ${message.role === 'user' ? 'user-message' : 'ai-message'}`}
            >
              <div className="message-content">
                <strong>{message.role === 'user' ? 'You:' : 'Assistant:'}</strong>
                <p>{message.content}</p>
              </div>
              <small className="message-time">
                {new Date(message.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </small>
            </div>
          ))
        )}
        {isLoading && (
          <div className="message ai-message">
            <div className="message-content">
              <strong>Assistant:</strong>
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {error && <div className="error">{error}</div>}

      <div className="chat-input-area">
        <textarea
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message here..."
          disabled={isLoading}
          rows={3}
        />
        <button 
          onClick={handleSendMessage} 
          disabled={isLoading || !inputValue.trim()}
          className="send-button"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatInterface;