# Quickstart Guide: Multi-User Todo Application with AI Chatbot

## Overview
This guide provides instructions for setting up and running the Multi-User Todo Application with AI Chatbot locally.

## Prerequisites
- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- Poetry or pip (for Python dependency management)
- Git
- Access to Neon PostgreSQL (sign up at https://neon.tech)
- OpenAI API key (for AI agent functionality)

## Setting Up the Backend (FastAPI)

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Set Up Python Environment
Using Poetry:
```bash
poetry install
poetry shell
```

Or using pip:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the backend directory:

```env
DATABASE_URL="postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require"
SECRET_KEY="your-super-secret-key-here"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENAI_API_KEY="your-openai-api-key-here"
MCP_SERVER_URL="http://localhost:8080"
```

### 4. Run Database Migrations
```bash
alembic upgrade head
```

### 5. Start the Backend Server
```bash
uvicorn src.main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`.

## Setting Up the MCP Server

### 1. Navigate to MCP Server Directory
```bash
cd mcp-server  # If separate, otherwise it's integrated in the backend
```

### 2. Configure Environment Variables
Create a `.env` file in the MCP server directory:

```env
DATABASE_URL="postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require"
SECRET_KEY="your-super-secret-key-here"
OPENAI_API_KEY="your-openai-api-key-here"
BACKEND_API_URL="http://localhost:8000"
```

### 3. Start the MCP Server
```bash
python -m src.mcp_server.main
```

The MCP server will be available at `http://localhost:8080`.

## Setting Up the Frontend (Next.js)

### 1. Navigate to Frontend Directory
```bash
cd frontend  # From the repository root
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Configure Environment Variables
Create a `.env.local` file in the frontend directory:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_MCP_SERVER_URL=http://localhost:8080
```

### 4. Start the Frontend Development Server
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`.

## Running All Servers Together

For development, you can run both servers simultaneously using a tool like `concurrently`:

```bash
# From the repository root
npm install -g concurrently
concurrently "cd backend && uvicorn src.main:app --reload --port 8000" "cd mcp-server && python -m src.mcp_server.main" "cd frontend && npm run dev"
```

## API Endpoints

Once all servers are running, you can access the following endpoints:

- **Frontend**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000`
- **MCP Server**: `http://localhost:8080`
- **API Documentation**: `http://localhost:8000/docs`
- **API Redoc**: `http://localhost:8000/redoc`

## Testing the Application

### 1. User Registration
Send a POST request to `/auth/signup` with the following payload:

```json
{
  "name": "Test User",
  "email": "test@example.com",
  "password": "securepassword123"
}
```

### 2. User Login
Send a POST request to `/auth/signin` with the following payload:

```json
{
  "email": "test@example.com",
  "password": "securepassword123"
}
```

### 3. Creating a Todo
After logging in, use the returned token to create a todo by sending a POST request to `/api/{user_id}/tasks` with the header `Authorization: Bearer <token>` and the following payload:

```json
{
  "title": "Sample Todo",
  "description": "This is a sample todo item"
}
```

### 4. Using the Chat Interface
After logging in, navigate to the chat interface at `/chat` and send a message like "Add a task to buy groceries". The AI agent will process your request using the MCP tools.

## Troubleshooting

### Common Issues

1. **Database Connection Issues**:
   - Verify your Neon PostgreSQL connection string is correct
   - Ensure your IP address is whitelisted in Neon dashboard
   - Check that SSL mode is properly configured

2. **CORS Issues**:
   - Make sure the backend allows requests from the frontend origin
   - Check that `ALLOWED_ORIGINS` in the backend configuration includes `http://localhost:3000`

3. **Authentication Issues**:
   - Ensure tokens are being properly stored and sent with requests
   - Verify that the secret key matches between frontend and backend

4. **MCP Server Issues**:
   - Verify that the MCP server is running and accessible
   - Check that the AI agent can communicate with the MCP server
   - Ensure proper authentication between the AI agent and MCP server