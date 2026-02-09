# Todo API Documentation for Developers

## Base URL
```
Production: https://api.todoapp.com/v1
Development: http://localhost:8000/v1
```

## Authentication
All API requests require a valid JWT token in the Authorization header:
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

## Available Endpoints

### Authentication

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
- `200 OK`: User successfully registered
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
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid or expired token
- `403 Forbidden`: User attempting to update another user's task
- `404 Not Found`: Task or user does not exist

## Rate Limiting
The API implements rate limiting to prevent abuse. Standard limits are:
- 100 requests per minute per IP
- 1000 requests per hour per IP

## Error Codes
- `AUTHENTICATION_ERROR`: Authentication failed
- `AUTHORIZATION_ERROR`: Not authorized to perform this action
- `RESOURCE_NOT_FOUND`: Requested resource does not exist
- `VALIDATION_ERROR`: Request validation failed
- `INTERNAL_ERROR`: An internal server error occurred

## SDKs and Libraries
Coming soon: Official SDKs for popular programming languages.

## Support
For API support, contact: api-support@todoapp.com