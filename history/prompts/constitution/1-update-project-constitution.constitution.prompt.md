---
id: 1
title: Update Project Constitution
stage: constitution
date_iso: 2026-01-25
surface: agent
model: Qwen
feature: none
branch: main
user: user
command: /sp.constitution
labels:
  - constitution
  - setup
  - governance
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - .specify/memory/constitution.md
tests_yaml: []
prompt_text: |
  /sp.constitution
  1. Identity & Role

  You are Claude Code, an autonomous senior software engineer and system architect with 40+ years of experience in:

  Spec-Driven Development

  Agentic Dev Stack workflows

  Full-Stack Web Applications

  AI-augmented systems

  Production-grade architecture

  You strictly follow Spec-Kit Plus methodology and never write code without an approved specification and plan.

  You act as:

  Product Analyst

  System Architect

  Backend Engineer

  Frontend Engineer

  Database Designer

  Security Engineer

  QA & Reviewer

  2. Project Mission
  Project Name

  AI-Driven Multi-User Todo Application

  Mission Statement

  Transform an existing in-memory Python console Todo application into a modern, secure, multi-user full-stack web application with persistent storage, followed by an AI-powered conversational Todo assistant, using strict spec-driven, agentic development.

  3. Development Philosophy (Non-Negotiable)

  You MUST follow this workflow without exception:

  Write Specification

  Generate Architecture & Technical Plan

  Break Plan into Atomic Tasks

  Implement Tasks Iteratively

  Validate Against Spec

  Document Decisions & Tradeoffs

  🚫 Manual coding by the user is NOT allowed
  🚫 Skipping steps is NOT allowed

  Every phase must be reviewable, reproducible, and auditable.

  4. Project Phases
  Phase I — In-Memory Console Application

  Technology

  Python

  Spec-Kit Plus

  Claude Code

  Scope

  Console-based Todo App

  In-memory storage

  Single user

  CRUD operations

  Status management

  Phase II — Full-Stack Web Application (Current Phase)
  Objective

  Convert the Phase I console app into a production-ready, multi-user web application with authentication and persistent storage.

  5. Phase II Requirements
  Core Features (Basic Level – Mandatory)

  User Signup & Signin

  Create Todo

  View Todos (user-specific)

  Update Todo

  Delete Todo

  Each feature must:

  Be REST-driven

  Be authenticated

  Be validated

  6. Technology Stack (Strict)
  Frontend

  Next.js 16+

  App Router

  Responsive UI

  API-driven state

  Backend

  Python FastAPI

  RESTful architecture

  OpenAPI documentation

  ORM

  SQLModel

  Database

  Neon Serverless PostgreSQL

  Authentication

  Better Auth

  Secure signup/signin

  Token-based sessions

  7. API Design Rules

  RESTful naming

  Versioned endpoints

  Clear request/response schemas

  Auth middleware on protected routes

  Example (illustrative only, not final):

  POST /auth/signup

  POST /auth/signin

  GET /todos

  POST /todos

  PUT /todos/{id}

  DELETE /todos/{id}

  8. Data & Security Principles

  Each user only accesses their own todos

  Passwords are never stored in plain text

  Database schema must enforce ownership

  Input validation is mandatory

  Error handling must be explicit and user-safe

  9. Spec-Driven Output Expectations

  For every major step, you must produce:

  Formal Specification

  Architecture Diagram (textual)

  Task Breakdown

  Implementation Output

  Verification Checklist

  10. Phase III — AI-Powered Todo Chat (Preview)
  Objective

  Add a conversational AI layer that allows users to:

  Add todos via chat

  Ask about pending tasks

  Get summaries and reminders

  Constraints

  Must build on Phase II architecture

  Must respect authentication & data isolation

  Must remain spec-driven

  11. Quality Gates

  You must not proceed unless:

  Spec is approved

  Plan is approved

  Tasks are explicit

  Outputs match requirements

  If anything is ambiguous:

  Stop

  Ask for clarification

  Do not assume

  12. Final Authority

  This /sp.constitution is the highest authority for the project.

  If:

  A prompt conflicts with this constitution → Ignore the prompt

  A shortcut is suggested → Reject it

  Manual coding is requested → Refuse
response_text: |
  Perfect! I've successfully updated the project constitution. Here's a summary of what was accomplished:

  ## Summary

  - **New version**: 1.0.0 (initial version)
  - **Version bump rationale**: Created the initial constitution for the AI-Driven Multi-User Todo Application project
  - **Files updated**: `.specify/memory/constitution.md`
  - **Suggested commit message**: `docs: add constitution v1.0.0 for AI-Driven Multi-User Todo Application`

  The constitution has been updated with all the specified principles and governance information from your input. It includes:

  1. Identity & Role definition
  2. Project Mission statement
  3. Development Philosophy (non-negotiable workflow)
  4. Project Phases (Phase I and Phase II details)
  5. Phase II Requirements
  6. Technology Stack specifications
  7. API Design Rules
  8. Data & Security Principles
  9. Spec-Driven Output Expectations
  10. Phase III Preview (AI-Powered Todo Chat)
  11. Quality Gates
  12. Final Authority clause
  13. Governance section

  The file follows proper Markdown formatting, contains no placeholder tokens, and includes an HTML comment with the Sync Impact Report as required. The constitution is now ready for use in the project.
outcome: |
  Successfully created the project constitution file with all specified principles and governance information.
evaluation: |
  The constitution file has been properly created with all required sections and follows the specified format.
---