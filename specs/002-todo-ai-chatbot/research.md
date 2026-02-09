# Research: Multi-User Todo Application with AI Chatbot

## Overview
This research document addresses the technical decisions and unknowns identified during the planning phase for the Multi-User Todo Application with AI Chatbot.

## Decision: MCP Server Implementation
**Rationale**: The system requires an MCP (Model Context Protocol) server to expose task operations as tools for the AI agent. According to the constitution, AI agents must never directly access the database and must perform all task operations via MCP tools.

**Alternatives considered**:
- Direct database access by AI agent (violates constitution)
- REST API calls from AI agent (violates constitution requirement for MCP tools)
- GraphQL mutations from AI agent (violates constitution requirement for MCP tools)

## Decision: Single AI Agent vs Multiple Agents
**Rationale**: Using a single task-management agent is simpler and more predictable than multiple agents. This approach aligns with the constitution's emphasis on stateless execution and clear separation of concerns.

**Alternatives considered**:
- Multiple specialized agents (more complex coordination)
- Hybrid approach with one orchestrator and multiple specialists (increased complexity)

## Decision: Conversation State Management
**Rationale**: Conversation state must be maintained in the database rather than in memory to ensure the system remains stateless and can be restarted without losing conversation or task data. This satisfies the constitution's statelessness requirements.

**Alternatives considered**:
- In-memory storage (violates statelessness requirement)
- Session-based storage (violates statelessness requirement)
- Cache-based storage (violates statelessness requirement)

## Decision: Authentication Method
**Rationale**: Using Better Auth with JWT tokens for all endpoints (both REST API and chat) ensures consistent authentication across the system and enforces user data isolation as required by the constitution.

**Alternatives considered**:
- Different authentication methods for different endpoints (violates consistency)
- Session-based authentication (doesn't align with stateless architecture)

## Decision: Frontend Architecture
**Rationale**: Using Next.js 16+ with App Router provides a robust foundation for both the task management UI and the conversational chat UI, meeting the constitution's frontend requirements.

**Alternatives considered**:
- Other frameworks (React with CRA, Vue, Angular) - Next.js provides better SSR and routing for this use case
- Pure client-side application (would lack SEO benefits and server-side rendering)

## Decision: Database ORM
**Rationale**: SQLModel is required by the constitution and provides the right balance of SQLAlchemy's power with Pydantic's validation for type safety.

**Alternatives considered**:
- Raw SQL queries (less maintainable)
- Other ORMs like Tortoise ORM (violates constitution requirement for SQLModel)
- Peewee ORM (violates constitution requirement for SQLModel)

## Decision: AI Agent Framework
**Rationale**: OpenAI Agents SDK is specified in the constitution and provides the necessary tools for creating AI agents that can interact with custom tools (MCP server).

**Alternatives considered**:
- LangChain (not specified in constitution)
- Anthropic Claude Functions (not specified in constitution)
- Custom agent implementation (unnecessary complexity)