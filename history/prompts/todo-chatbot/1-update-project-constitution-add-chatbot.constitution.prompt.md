---
id: 1
title: update-project-constitution-add-chatbot
stage: constitution
date_iso: 2026-02-09
surface: agent
model: Qwen
feature: todo-chatbot
branch: main
user: user
command: /sp.constitution
labels:
  - constitution
  - todo-chatbot
  - phase-iii
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - .specify/memory/constitution.md
tests_yaml: []
prompt_text: |
  $ARGUMENTS

  As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

  1) Determine Stage
     - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

  2) Generate Title and Determine Routing:
     - Generate Title: 3–7 words (slug for filename)
     - Route is automatically determined by stage:
       - `constitution` → `history/prompts/constitution/`
       - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
       - `general` → `history/prompts/general/`

  3) Create and Fill PHR (Shell first; fallback agent‑native)
     - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
     - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
     - If the script fails:
       - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
       - Allocate an ID; compute the output path based on stage from step 2; write the file
       - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

  4) Validate + report
     - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
     - On failure: warn, don't block. Skip only for `/sp.phr`.

  /sp.constitution Project: Multi-User Todo Application with AI Chatbot (Phase II + Phase III)
  Hackathon: Hackathon II – Spec-Driven Development

  Core principles:

  Spec-driven development only (no manual coding)

  Agentic Dev Stack workflow enforcement

  Security-first, user-isolated architecture

  Stateless backend services

  Clear separation of concerns:

  Frontend UI

  REST API

  AI Agent logic

  MCP tools

  Database persistence

  Reproducibility through documented specs, plans, tasks, and prompts

  Key standards:

  All functionality must originate from written specifications

  All code must be generated via Claude Code + Spec-Kit Plus

  Manual code edits are strictly forbidden

  REST APIs and AI agents must enforce task ownership

  Backend services must not rely on in-memory state

  All user actions must be authenticated and authorized

  Database is the single source of truth

  Supported phases:
  Phase II – Full-Stack Web Application

  Multi-user Todo web application

  RESTful API architecture

  JWT-secured endpoints

  Responsive frontend interface

  Persistent storage using Neon Serverless PostgreSQL

  Phase III – Todo AI Chatbot

  Conversational interface for managing todos

  Natural language interaction via AI agent

  MCP-based tool invocation for task operations

  Stateless chat execution with database-backed memory

  Technology constraints:

  Frontend:

  Next.js 16+ (App Router) for web app

  OpenAI ChatKit for chatbot UI

  Backend:

  Python FastAPI

  ORM:

  SQLModel only

  Database:

  Neon Serverless PostgreSQL

  Authentication:

  Better Auth

  JWT-based authentication

  AI Framework:

  OpenAI Agents SDK

  MCP Server:

  Official MCP SDK only

  REST API rules (Phase II):

  API endpoints must follow defined contracts:

  GET /api/{user_id}/tasks

  POST /api/{user_id}/tasks

  GET /api/{user_id}/tasks/{id}

  PUT /api/{user_id}/tasks/{id}

  DELETE /api/{user_id}/tasks/{id}

  PATCH /api/{user_id}/tasks/{id}/complete

  All API requests must include:

  Authorization: Bearer <JWT>


  Backend must:

  Verify JWT signature and expiry

  Match JWT user with {user_id} in route

  Filter all data by authenticated user

  AI & MCP rules (Phase III):

  AI agents must never directly access the database

  All task operations must be performed via MCP tools

  MCP tools must be stateless and persist state in the database

  MCP tools must enforce user ownership using user_id

  AI agents must:

  Interpret natural language intent

  Select correct MCP tools

  Confirm actions in natural language

  Handle errors gracefully

  Never hallucinate task data

  Stateless execution rules:

  Backend servers must hold no session state

  For each request:

  Fetch required state from database

  Execute logic (REST or Agent + MCP)

  Persist results to database

  Return response

  Conversation context (Phase III) must be reconstructed from database on every request

  Server must be safe to restart at any time without data loss

  Data models governed by this constitution:

  Task

  id, user_id, title, description, completed, created_at, updated_at

  Conversation

  id, user_id, created_at, updated_at

  Message

  id, conversation_id, user_id, role, content, created_at

  Security rules:

  All endpoints (REST and Chat) require authentication

  Requests without valid authentication return 401 Unauthorized

  Cross-user data access is strictly forbidden

  Task ownership must be enforced at:

  REST API layer

  MCP tool layer

  Frontend must never be trusted as the source of authorization

  Development workflow rules:

  Mandatory workflow:

  /sp.specify

  /sp.clarify

  /sp.plan

  /sp.tasks

  /sp.implement

  Any implementation not traceable to specs is invalid

  Each phase may extend specs but must not violate this constitution

  Success criteria:

  Phase II:

  Fully functional multi-user Todo web application

  Secure REST API with JWT

  Persistent storage in Neon PostgreSQL

  Phase III:

  Fully functional AI chatbot for Todo management

  MCP tools correctly invoked by AI agent

  Stateless chat with persistent conversation memory

  Entire project:

  Reviewable via specs alone

  No manual coding violations

  Clear, scalable, production-style architecture

  Final authority clause:

  This /sp.constitution is the single source of truth for both Phase II and Phase III.
  Any behavior, implementation, or decision that conflicts with this document is invalid.
response_text: |
  Now I'll update the constitution file with the detailed principles you've provided. Let me create a comprehensive constitution based on your requirements:

  I have successfully updated the project constitution to include the AI chatbot functionality. The new constitution document includes:

  1. Core principles for spec-driven development
  2. Agentic Dev Stack workflow enforcement
  3. Security-first, user-isolated architecture
  4. Stateless backend services
  5. Clear separation of concerns
  6. Database as single source of truth

  It also defines technology constraints, API contract standards, AI agent rules, data models, statelessness requirements, and success criteria for both Phase II (Full-Stack Web Application) and Phase III (Todo AI Chatbot).

  The constitution is now stored at `.specify/memory/constitution.md` and serves as the single source of truth for both phases of the project.
outcome: |
  Updated project constitution to include AI chatbot functionality with comprehensive guidelines for both Phase II (Web App) and Phase III (Chatbot).
evaluation: |
  The constitution update was successful and includes all required principles for both phases of the project.
---

# Constitution Update: Multi-User Todo Application with AI Chatbot

## Summary
Updated the project constitution to incorporate AI chatbot functionality alongside the existing full-stack web application. The new constitution establishes comprehensive guidelines for both Phase II (Web App) and Phase III (Chatbot) development.

## Changes Made
- Created a comprehensive constitution document at `.specify/memory/constitution.md`
- Defined core principles for spec-driven development
- Established security-first architecture requirements
- Specified technology constraints for both phases
- Outlined API contract standards for Phase II
- Defined AI agent rules for Phase III
- Set success criteria for both phases

## Files Modified
- `.specify/memory/constitution.md` - New constitution document

## Next Steps
- Use the constitution to guide the implementation of both Phase II and Phase III
- Ensure all future development adheres to the established principles
- Reference the constitution during the specification, planning, and task creation phases