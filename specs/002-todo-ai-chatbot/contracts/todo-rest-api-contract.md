# REST API Contracts: Todo Application

## Overview
This document defines the API contracts for the Todo Application as specified in the feature requirements.

## Base URL
`https://api.todoapp.com/v1` (production)  
`http://localhost:8000` (development)

## Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <JWT_TOKEN>
```

## Common Response Format

### Success Response
```json
{
  "success": true,
  "data": { /* response data */ },
  "message": "Optional success message"
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": { /* optional error details */ }
  }
}
```

## Endpoints

### User Authentication

#### POST /auth/signup
Register a new user account.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```

**Responses**:
- `201 Created`: User successfully registered
- `400 Bad Request`: Invalid input data
- `409 Conflict`: Email already exists

#### POST /auth/signin
Authenticate a user and return JWT token.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "access_token": "jwt_token_here",
    "token_type": "bearer",
    "user": {
      "id": "uuid-string",
      "email": "user@example.com",
      "name": "John Doe"
    }
  }
}
```

**Responses**:
- `200 OK`: Authentication successful
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid credentials

#### POST /auth/signout
Invalidate the user's session.

**Headers**:
```
Authorization: Bearer <JWT_TOKEN>
```

**Responses**:
- `200 OK`: Successfully signed out
- `401 Unauthorized`: Invalid or expired token

### Todo Tasks API

#### GET /api/{user_id}/tasks
Retrieve all tasks for the authenticated user.

**Path Parameters**:
- `user_id`: The ID of the user whose tasks to retrieve (must match JWT user ID)

**Query Parameters**:
- `completed` (optional): Filter by completion status (true/false)
- `limit` (optional): Number of tasks to return (default: 50, max: 100)
- `offset` (optional): Number of tasks to skip (for pagination)

**Headers**:
```
Authorization: Bearer <JWT_TOKEN>
```

**Responses**:
- `200 OK`: Successfully retrieved tasks
  ```json
  {
    "success": true,
    "data": {
      "tasks": [
        {
          "id": "uuid-string",
          "user_id": "uuid-string",
          "title": "Task title",
          "description": "Task description",
          "completed": false,
          "created_at": "2023-01-01T00:00:00Z",
          "updated_at": "2023-01-01T00:00:00Z"
        }
      ],
      "pagination": {
        "total": 10,
        "limit": 50,
        "offset": 0
      }
    }
  }
  ```
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: User attempting to access another user's tasks
- `404 Not Found`: User ID does not exist

#### POST /api/{user_id}/tasks
Create a new task for the authenticated user.

**Path Parameters**:
- `user_id`: The ID of the user creating the task (must match JWT user ID)

**Headers**:
```
Authorization: Bearer <JWT_TOKEN>
```

**Request Body**:
```json
{
  "title": "New task title",
  "description": "Optional task description"
}
```

**Responses**:
- `201 Created`: Task successfully created
  ```json
  {
    "success": true,
    "data": {
      "id": "uuid-string",
      "user_id": "uuid-string",
      "title": "New task title",
      "description": "Optional task description",
      "completed": false,
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z"
    }
  }
  ```
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: User attempting to create task for another user

#### GET /api/{user_id}/tasks/{id}
Retrieve a specific task for the authenticated user.

**Path Parameters**:
- `user_id`: The ID of the user (must match JWT user ID)
- `id`: The ID of the task to retrieve

**Headers**:
```
Authorization: Bearer <JWT_TOKEN>
```

**Responses**:
- `200 OK`: Task successfully retrieved
  ```json
  {
    "success": true,
    "data": {
      "id": "uuid-string",
      "user_id": "uuid-string",
      "title": "Task title",
      "description": "Task description",
      "completed": false,
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z"
    }
  }
  ```
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: User attempting to access another user's task
- `404 Not Found`: Task or user does not exist

#### PUT /api/{user_id}/tasks/{id}
Update a specific task for the authenticated user.

**Path Parameters**:
- `user_id`: The ID of the user (must match JWT user ID)
- `id`: The ID of the task to update

**Headers**:
```
Authorization: Bearer <JWT_TOKEN>
```

**Request Body**:
```json
{
  "title": "Updated task title",
  "description": "Updated task description"
}
```

**Responses**:
- `200 OK`: Task successfully updated
  ```json
  {
    "success": true,
    "data": {
      "id": "uuid-string",
      "user_id": "uuid-string",
      "title": "Updated task title",
      "description": "Updated task description",
      "completed": false,
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-02T00:00:00Z"
    }
  }
  ```
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: User attempting to update another user's task
- `404 Not Found`: Task or user does not exist

#### DELETE /api/{user_id}/tasks/{id}
Delete a specific task for the authenticated user.

**Path Parameters**:
- `user_id`: The ID of the user (must match JWT user ID)
- `id`: The ID of the task to delete

**Headers**:
```
Authorization: Bearer <JWT_TOKEN>
```

**Responses**:
- `200 OK`: Task successfully deleted
  ```json
  {
    "success": true,
    "message": "Task deleted successfully"
  }
  ```
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: User attempting to delete another user's task
- `404 Not Found`: Task or user does not exist

#### PATCH /api/{user_id}/tasks/{id}/complete
Toggle the completion status of a specific task for the authenticated user.

**Path Parameters**:
- `user_id`: The ID of the user (must match JWT user ID)
- `id`: The ID of the task to update

**Headers**:
```
Authorization: Bearer <JWT_TOKEN>
```

**Request Body**:
```json
{
  "completed": true
}
```

**Responses**:
- `200 OK`: Task completion status successfully updated
  ```json
  {
    "success": true,
    "data": {
      "id": "uuid-string",
      "user_id": "uuid-string",
      "title": "Task title",
      "description": "Task description",
      "completed": true,
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-02T00:00:00Z"
    }
  }
  ```
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: User attempting to update another user's task
- `404 Not Found`: Task or user does not exist

### Chat API

#### POST /api/{user_id}/chat
Send a message to the AI chatbot and receive a response.

**Path Parameters**:
- `user_id`: The ID of the user (must match JWT user ID)

**Headers**:
```
Authorization: Bearer <JWT_TOKEN>
```

**Request Body**:
```json
{
  "message": "Add a task to buy groceries",
  "conversation_id": "optional-conversation-id"
}
```

**Responses**:
- `200 OK`: Successfully processed chat message
  ```json
  {
    "success": true,
    "data": {
      "conversation_id": "uuid-string",
      "response": "I've added the task 'buy groceries' to your list.",
      "tool_calls": [
        {
          "tool_name": "create_task",
          "arguments": {
            "title": "buy groceries",
            "description": ""
          },
          "result": {
            "id": "new-task-id",
            "title": "buy groceries",
            "completed": false
          }
        }
      ],
      "timestamp": "2023-01-01T00:00:00Z"
    }
  }
  ```
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: User attempting to chat for another user
- `404 Not Found`: User does not exist
- `500 Internal Server Error`: AI processing error