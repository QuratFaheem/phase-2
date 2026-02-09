<!--
Sync Impact Report:
- Version change: N/A → 1.0.0 (initial constitution for Todo Application with AI Chatbot)
- Modified principles: N/A (new file)
- Added sections: All sections (new constitution)
- Removed sections: N/A
- Templates requiring updates: ✅ updated / ⚠ pending
- Follow-up TODOs: None
-->
# Multi-User Todo Application with AI Chatbot Constitution

## Core Principles

### I. Spec-Driven Development Only
All functionality must originate from written specifications. Manual code edits are strictly forbidden. All code must be generated via Claude Code + Spec-Kit Plus. Development follows the mandatory workflow: /sp.specify → /sp.clarify → /sp.plan → /sp.tasks → /sp.implement. Any implementation not traceable to specs is invalid.

### II. Agentic Dev Stack Workflow Enforcement
The development process must follow the agentic workflow with MCP tools. Each phase may extend specs but must not violate this constitution. The system must maintain reproducibility through documented specs, plans, tasks, and prompts.

### III. Security-First, User-Isolated Architecture
All endpoints (REST and Chat) require authentication. Requests without valid authentication return 401 Unauthorized. Cross-user data access is strictly forbidden. Task ownership must be enforced at the REST API layer, MCP tool layer, and frontend must never be trusted as the source of authorization.

### IV. Stateless Backend Services
Backend servers must hold no session state. For each request: fetch required state from database, execute logic (REST or Agent + MCP), persist results to database, return response. Server must be safe to restart at any time without data loss. Conversation context (Phase III) must be reconstructed from database on every request.

### V. Clear Separation of Concerns
The system must maintain clear separation of concerns:
- Frontend UI: Next.js 16+ (App Router) for web app, OpenAI ChatKit for chatbot UI
- REST API: Python FastAPI with JWT-secured endpoints
- AI Agent Logic: OpenAI Agents SDK with MCP-based tool invocation
- MCP Tools: Official MCP SDK only
- Database Persistence: Neon Serverless PostgreSQL with SQLModel ORM

### VI. Database as Single Source of Truth
Database is the single source of truth. All user actions must be authenticated and authorized. Backend services must not rely on in-memory state. AI agents must never directly access the database - all task operations must be performed via MCP tools.

## Technology Constraints

### Frontend Requirements
- Next.js 16+ (App Router) for web app
- OpenAI ChatKit for chatbot UI
- Responsive frontend interface

### Backend Requirements
- Python FastAPI
- ORM: SQLModel only
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT-based authentication

### AI & MCP Framework Requirements
- OpenAI Agents SDK
- Official MCP SDK only
- MCP tools must be stateless and persist state in the database
- MCP tools must enforce user ownership using user_id

## API Contract Standards (Phase II)

### REST API Rules
API endpoints must follow defined contracts:
- GET /api/{user_id}/tasks
- POST /api/{user_id}/tasks
- GET /api/{user_id}/tasks/{id}
- PUT /api/{user_id}/tasks/{id}
- DELETE /api/{user_id}/tasks/{id}
- PATCH /api/{user_id}/tasks/{id}/complete

All API requests must include Authorization: Bearer <JWT>. Backend must verify JWT signature and expiry, match JWT user with {user_id} in route, and filter all data by authenticated user.

### AI Agent Rules (Phase III)
AI agents must:
- Interpret natural language intent
- Select correct MCP tools
- Confirm actions in natural language
- Handle errors gracefully
- Never hallucinate task data

AI agents must never directly access the database. All task operations must be performed via MCP tools.

## Data Models

### Task Model
Fields: id, user_id, title, description, completed, created_at, updated_at

### Conversation Model
Fields: id, user_id, created_at, updated_at

### Message Model
Fields: id, conversation_id, user_id, role, content, created_at

## Statelessness Requirements

All services must follow stateless execution rules:
- Backend servers must hold no session state
- For each request: Fetch required state from database, Execute logic (REST or Agent + MCP), Persist results to database, Return response
- Conversation context (Phase III) must be reconstructed from database on every request
- Server must be safe to restart at any time without data loss

## Success Criteria

### Phase II - Full-Stack Web Application
- Fully functional multi-user Todo web application
- Secure REST API with JWT
- Persistent storage in Neon PostgreSQL
- Multi-user Todo web application with responsive UI

### Phase III - Todo AI Chatbot
- Fully functional AI chatbot for Todo management
- MCP tools correctly invoked by AI agent
- Stateless chat with persistent conversation memory
- Natural language interaction via AI agent

### Overall Project Requirements
- Entire project must be reviewable via specs alone
- No manual coding violations
- Clear, scalable, production-style architecture
- Conversational interface for managing todos with MCP-based tool invocation

## Governance

This constitution is the single source of truth for both Phase II and Phase III. Any behavior, implementation, or decision that conflicts with this document is invalid. Amendments require documentation, approval, and migration plan. All PRs/reviews must verify compliance with these principles.

**Version**: 1.0.0 | **Ratified**: 2026-02-09 | **Last Amended**: 2026-02-09