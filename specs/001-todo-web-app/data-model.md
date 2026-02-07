# Data Model Specification: Todo Full-Stack Web Application — Phase II

**Feature**: Todo Full-Stack Web Application — Phase II
**Date**: 2026-01-25
**Author**: Claude Code

## Overview

This document specifies the data model for the multi-user todo web application. It defines the entities, their attributes, relationships, and constraints required to support the functional requirements while ensuring data isolation between users.

## Entity Definitions

### User Entity

**Purpose**: Represents a registered user in the system

**Attributes**:
- `id` (UUID/String): Unique identifier for the user (Primary Key)
- `name` (String, max 100): User's display name
- `email` (String, max 255): User's email address (Unique constraint)
- `password_hash` (String): Securely hashed password using bcrypt
- `created_at` (DateTime): Timestamp when the user account was created
- `updated_at` (DateTime): Timestamp when the user account was last updated

**Constraints**:
- Email must be unique across all users
- Email must follow standard email format validation
- Password must be securely hashed before storage
- Name and email are required fields

**Relationships**:
- One-to-Many: A user can have many todos (via user_id foreign key)

### Todo Entity

**Purpose**: Represents a todo item owned by a specific user

**Attributes**:
- `id` (UUID/String): Unique identifier for the todo (Primary Key)
- `user_id` (UUID/String): Foreign key linking to the owning user (Foreign Key)
- `title` (String, max 200): Title of the todo item (Required)
- `description` (Text, optional): Detailed description of the todo
- `status` (Enum: pending, in-progress, completed): Current status of the todo (Default: pending)
- `created_at` (DateTime): Timestamp when the todo was created
- `updated_at` (DateTime): Timestamp when the todo was last updated

**Constraints**:
- Title is required and must not be empty
- Status must be one of the allowed enum values
- Each todo must belong to a valid user (foreign key constraint)
- A user can only access their own todos

**Relationships**:
- Many-to-One: Multiple todos can belong to one user (via user_id foreign key)

## Database Schema

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Todos table
CREATE TABLE todos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_todos_user_id ON todos(user_id);
CREATE INDEX idx_todos_status ON todos(status);
CREATE INDEX idx_users_email ON users(email);
```

## Data Validation Rules

### User Validation
- Email format must be valid (using standard email regex pattern)
- Name must be 1-100 characters
- Password must be securely hashed using bcrypt before storage
- Email uniqueness must be enforced at the database level

### Todo Validation
- Title must be 1-200 characters
- Status must be one of: 'pending', 'in-progress', 'completed'
- User_id must reference an existing user
- Description is optional and can be null or empty

## State Transitions

### Todo Status Transitions
- `pending` → `in-progress`: When user starts working on the todo
- `in-progress` → `completed`: When user finishes the todo
- `completed` → `pending`: When user needs to reopen the todo
- `in-progress` → `pending`: When user decides to postpone the todo

## Security & Privacy Considerations

### Data Isolation
- Each user can only access todos where user_id matches their own ID
- Database queries must always filter by user_id for todo access
- Foreign key constraints ensure referential integrity
- Cascade delete on user deletion removes all associated todos

### Access Control
- Authentication required before any data access
- Authorization checks must verify user owns the requested data
- API endpoints must validate that user_id matches authenticated user

## Performance Considerations

### Indexing Strategy
- Index on users.email for efficient login lookups
- Index on todos.user_id for efficient user-specific queries
- Index on todos.status for status-based filtering

### Query Optimization
- Use JOINs efficiently when retrieving user and todo data together
- Implement pagination for large todo lists
- Consider read replicas for high-read scenarios