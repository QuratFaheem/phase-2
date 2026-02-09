# MCP (Model Context Protocol) Server Contracts: Todo Application

## Overview
This document defines the MCP contracts for the Todo Application as specified in the feature requirements. The MCP server exposes task operations as tools for the AI agent to use, ensuring that AI agents never directly access the database.

## MCP Server Endpoint
`http://localhost:8080/mcp` (development)  
`https://mcp.todoapp.com/v1` (production)

## Authentication
All MCP endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <JWT_TOKEN>
```

## Tool Definitions

### Tool: list_tasks
Retrieve all tasks for the authenticated user.

**Parameters**:
```json
{
  "user_id": "uuid-string",
  "completed": "boolean (optional)",
  "limit": "integer (optional)",
  "offset": "integer (optional)"
}
```

**Response**:
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

### Tool: create_task
Create a new task for the authenticated user.

**Parameters**:
```json
{
  "user_id": "uuid-string",
  "title": "string",
  "description": "string (optional)"
}
```

**Response**:
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

### Tool: get_task
Retrieve a specific task for the authenticated user.

**Parameters**:
```json
{
  "user_id": "uuid-string",
  "task_id": "uuid-string"
}
```

**Response**:
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

### Tool: update_task
Update a specific task for the authenticated user.

**Parameters**:
```json
{
  "user_id": "uuid-string",
  "task_id": "uuid-string",
  "title": "string (optional)",
  "description": "string (optional)"
}
```

**Response**:
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

### Tool: delete_task
Delete a specific task for the authenticated user.

**Parameters**:
```json
{
  "user_id": "uuid-string",
  "task_id": "uuid-string"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

### Tool: toggle_task
Toggle the completion status of a specific task for the authenticated user.

**Parameters**:
```json
{
  "user_id": "uuid-string",
  "task_id": "uuid-string",
  "completed": "boolean"
}
```

**Response**:
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

## Common Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "error": {
    "code": "INVALID_INPUT",
    "message": "One or more parameters are invalid",
    "details": {
      "param_name": "error_description"
    }
  }
}
```

### 401 Unauthorized
```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid or expired authentication token"
  }
}
```

### 403 Forbidden
```json
{
  "success": false,
  "error": {
    "code": "FORBIDDEN",
    "message": "User not authorized to perform this action"
  }
}
```

### 404 Not Found
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Requested resource does not exist"
  }
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred"
  }
}
```