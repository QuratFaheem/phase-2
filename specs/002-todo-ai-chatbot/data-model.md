# Data Model: Multi-User Todo Application with AI Chatbot

## Overview
This document defines the data models for the Multi-User Todo Application with AI Chatbot, based on the requirements in the feature specification and constitution.

## Entity: User
Represents a registered user in the system.

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the user
- `email`: String (Unique, Indexed) - User's email address for login
- `hashed_password`: String - BCrypt hashed password
- `created_at`: DateTime - Timestamp when the user account was created
- `updated_at`: DateTime - Timestamp when the user account was last updated

**Validation Rules**:
- Email must be a valid email format
- Email must be unique across all users
- Password must meet minimum strength requirements (8+ characters)

## Entity: Task
Represents a user's todo item.

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the task
- `user_id`: UUID (Foreign Key) - References the user who owns this task
- `title`: String (Indexed) - Brief title of the task
- `description`: Text (Optional) - Detailed description of the task
- `completed`: Boolean - Whether the task is completed (default: false)
- `created_at`: DateTime - Timestamp when the task was created
- `updated_at`: DateTime - Timestamp when the task was last updated

**Validation Rules**:
- Title must not be empty
- Title must be less than 200 characters
- Description must be less than 1000 characters
- User_id must reference an existing user

**Relationships**:
- Belongs to one User (user_id → users.id)

## Entity: Conversation
Represents a chat session between a user and the AI chatbot.

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the conversation
- `user_id`: UUID (Foreign Key) - References the user who owns this conversation
- `created_at`: DateTime - Timestamp when the conversation was started
- `updated_at`: DateTime - Timestamp when the conversation was last updated

**Validation Rules**:
- User_id must reference an existing user

**Relationships**:
- Belongs to one User (user_id → users.id)
- Has many Messages (conversation_id → messages.conversation_id)

## Entity: Message
Represents individual messages in a conversation.

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the message
- `conversation_id`: UUID (Foreign Key) - References the conversation this message belongs to
- `user_id`: UUID (Foreign Key) - References the user who sent this message
- `role`: String (Enum: 'user', 'assistant') - The role of the message sender
- `content`: Text - The content of the message
- `created_at`: DateTime - Timestamp when the message was created

**Validation Rules**:
- Role must be either 'user' or 'assistant'
- Content must not be empty
- Content must be less than 5000 characters
- Conversation_id must reference an existing conversation
- User_id must reference an existing user

**Relationships**:
- Belongs to one Conversation (conversation_id → conversations.id)
- Belongs to one User (user_id → users.id)

## Relationships Diagram

```
Users ||--o{ Tasks : "owns"
Users ||--o{ Conversations : "initiates"
Conversations ||--o{ Messages : "contains"
Users ||--o{ Messages : "sends"
```

## State Transitions

### Task State Transitions
- `created` → `active` (automatically when created)
- `active` → `completed` (when user marks as complete)
- `completed` → `active` (when user unmarks as complete)

### Message State Transitions
- `created` → `sent` (automatically when saved to DB)
- `sent` → `read` (when retrieved by frontend, for future enhancement)

## Indexes
- Users.email (unique)
- Tasks.user_id (foreign key index)
- Tasks.created_at (for sorting)
- Conversations.user_id (foreign key index)
- Messages.conversation_id (foreign key index)
- Messages.created_at (for chronological ordering)