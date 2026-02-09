# Multi-User Todo Application with AI Chatbot

## Overview
This is a secure, multi-user todo application with persistent storage that extends to an AI-powered chatbot for natural-language task management. The system demonstrates stateless backend design with database-backed memory and showcases MCP-based tool invocation by AI agents.

## Architecture
- **Frontend**: Next.js 16+ (App Router) with React
- **Backend**: Python FastAPI with JWT-secured endpoints
- **AI Agent Logic**: OpenAI Agents SDK with MCP-based tool invocation
- **MCP Tools**: Official MCP SDK
- **Database Persistence**: Neon Serverless PostgreSQL with SQLModel ORM

## Features
1. **User Authentication**: Secure registration and login with Better Auth
2. **Task Management**: Full CRUD operations for todo tasks
3. **AI Chatbot**: Natural language processing for task management
4. **Stateless Design**: No session state held on the server
5. **Data Isolation**: Strict user data separation

## Tech Stack
- Frontend: Next.js 16+, React, TypeScript
- Backend: Python 3.11, FastAPI, SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT
- AI Framework: OpenAI Agents SDK
- MCP Server: Official MCP SDK

## Setup Instructions

### Prerequisites
- Node.js 18+
- Python 3.11+
- Poetry or pip
- Git
- Access to Neon PostgreSQL
- OpenAI API key

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Set up Python environment:
   ```bash
   # Using pip
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   Create a `.env` file in the backend directory:
   ```env
   DATABASE_URL="postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require"
   SECRET_KEY="your-super-secret-key-here"
   ALGORITHM="HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   OPENAI_API_KEY="your-openai-api-key-here"
   MCP_SERVER_URL="http://localhost:8080"
   ```

4. Run database migrations:
   ```bash
   alembic upgrade head
   ```

5. Start the backend server:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure environment variables:
   Create a `.env.local` file in the frontend directory:
   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   NEXT_PUBLIC_MCP_SERVER_URL=http://localhost:8080
   ```

4. Start the frontend development server:
   ```bash
   npm run dev
   ```

### MCP Server Setup
1. The MCP server is integrated into the backend and starts with the main application.

## Usage

### Web Interface
1. Register a new account or sign in
2. Manage your tasks via the dashboard
3. Create, update, delete, and mark tasks as complete

### AI Chatbot
1. Navigate to the chat interface
2. Use natural language to manage your tasks:
   - "Add a task to buy groceries"
   - "Show me my tasks"
   - "Mark the meeting task as complete"
   - "Delete the old project task"

## API Endpoints

### Authentication
- `POST /auth/signup` - Register a new user
- `POST /auth/signin` - Authenticate a user

### Task Management
- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

### Chat Interface
- `POST /api/{user_id}/chat` - Send a message to the AI chatbot

## Evaluation Criteria

This project meets the following hackathon requirements:

1. ✅ **Spec-driven development**: All functionality originates from written specifications
2. ✅ **Agentic workflow**: Following agentic workflow with MCP tools
3. ✅ **Security-first architecture**: All endpoints require authentication, data isolation enforced
4. ✅ **Stateless backend**: Backend holds no session state, conversation context reconstructed from DB
5. ✅ **Clear separation of concerns**: Frontend, REST API, AI Agent Logic, MCP Tools, Database clearly separated
6. ✅ **Database as single source of truth**: Database is the single source of truth, AI agents never directly access DB
7. ✅ **Technology constraints**: Using Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth, OpenAI Agents SDK, Official MCP SDK
8. ✅ **AI agent rules**: AI agents interpret natural language, select MCP tools, and never directly access DB
9. ✅ **Statelessness requirements**: Backend services stateless, conversation context reconstructed from DB

## Key Innovations

1. **MCP Integration**: Implements Model Context Protocol for secure AI-tool interaction
2. **Stateless AI**: Ensures conversation state is preserved in the database, not server memory
3. **Tool-Only AI**: AI agents can only perform actions through approved MCP tools
4. **Data Isolation**: Strict enforcement that users can only access their own data

## Files Structure
```
backend/
├── src/
│   ├── models/          # Data models
│   ├── services/        # Business logic
│   ├── api/            # API endpoints
│   ├── ai_agents/      # AI agent logic
│   ├── mcp_server/     # MCP tools
│   ├── database/       # Database utilities
│   └── middleware/     # Authentication, logging, etc.
├── requirements.txt
├── alembic.ini
└── main.py

frontend/
├── src/
│   ├── app/            # Next.js app router pages
│   ├── components/     # UI components
│   ├── services/       # API clients
│   └── types/          # TypeScript types
├── package.json
└── next.config.js
```

## Testing
- Unit tests for MCP tools
- Integration tests for API endpoints
- Contract tests for API compliance
- End-to-end tests for user workflows

## Security Features
- JWT-based authentication for all endpoints
- User data isolation at the database query level
- Input validation and sanitization
- Rate limiting to prevent abuse
- Secure password hashing with bcrypt