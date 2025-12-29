---
id: 003
title: Create Todo AI Chatbot Implementation Plan
stage: plan
date: 2025-12-28
surface: agent
model: claude-sonnet-4-5
feature: 001-todo-ai-chatbot
branch: 001-todo-ai-chatbot
user: Ahmed-malik
command: /sp.plan
labels: ["planning", "architecture", "mcp", "stateless", "openai-sdk"]
links:
  spec: specs/001-todo-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-todo-ai-chatbot/plan.md
tests:
  - none
---

## Prompt

Based on the provided SP.CONSTITUTION, generate a detailed SP.PLAN.

The plan must include:
- System architecture overview
- Data models (Task, Conversation, Message)
- API design for POST /api/{user_id}/chat
- MCP server responsibilities
- Agent design using OpenAI Agents SDK
- Stateless request lifecycle
- Error handling strategy
- Tool invocation flow

Rules:
- No code
- Step-by-step logical plan
- Clear separation of frontend, backend, agent, MCP

Output:
- Structured SP.PLAN document

## Response snapshot

Created comprehensive implementation plan (783 lines) with constitution compliance gates, research tasks, and detailed design specifications.

**Constitution Check - All Gates Pass**:
- ✅ Gate 1: MCP-Only Tool Interface (5 tools: add, list, complete, update, delete)
- ✅ Gate 2: Stateless Backend Architecture (no in-memory state, full history fetched per request)
- ✅ Gate 3: Conversation Persistence (messages stored before processing/returning)
- ✅ Gate 4: Database Isolation (agent never accesses DB, only MCP tools)
- ✅ Gate 5: Error Handling (friendly messages, technical details logged)
- ⚠️ Gate 6: Testing Discipline (optional per spec, TDD if included)

**Technical Context**:
- Language: Python 3.11+
- Stack: FastAPI, SQLModel, OpenAI Agents SDK, MCP SDK, ChatKit, Better Auth
- Database: Neon Serverless PostgreSQL
- Performance: <3s response time, 100 concurrent users, <200ms p95 DB latency
- Scale: 100-1000 users, up to 1000 messages/user, up to 1000 tasks/user

**Project Structure**: Web application (frontend + backend)
- Backend: backend/src/{models, services, mcp/tools, api/routes, db}
- Frontend: frontend/src/{components, pages, services}
- Tests: backend/tests/{contract, integration, unit}, frontend/tests/integration

**Phase 0: Research Tasks** (7 tasks):
1. R1: OpenAI Agents SDK integration pattern with MCP tools
2. R2: Neon PostgreSQL connection pooling for async FastAPI
3. R3: ChatKit integration with custom REST API
4. R4: MCP tool error handling patterns (friendly agent responses)
5. R5: Conversation history context window management (summarization)
6. R6: Better Auth integration with FastAPI (JWT validation)
7. R7: Horizontal scaling deployment patterns

**Phase 1: Design Tasks** (4 tasks):
1. D1: Data Model Design (User, Conversation, Message, Task with fields/relationships/indexes)
2. D2: API Contract Design (OpenAPI spec for POST /api/chat, GET /api/conversations)
3. D3: MCP Tool Contract Design (JSON schemas for 5 tools with parameters/returns/errors)
4. D4: Quickstart Guide (setup, development workflow, testing, deployment)

**Key Design Decisions**:
1. Full conversation history fetch per request (enables stateless, impacts DB load)
2. MCP tools return friendly error messages (agent uses in responses)
3. OpenAI Agents SDK for tool orchestration (vs raw API)
4. Neon Serverless PostgreSQL (auto-scaling, connection pooling)
5. Better Auth for authentication (JWT tokens)

**Suggested ADRs**:
1. Stateless Conversation Architecture (/sp.adr stateless-conversation-architecture)
2. MCP-Only Agent Interaction (/sp.adr mcp-only-agent-interaction)
3. OpenAI Agents SDK for Intent (/sp.adr openai-agents-sdk-for-intent)

**Architecture Highlights**:
- Three-tier: ChatKit (UI) → FastAPI (API) → MCP Tools (data)
- Stateless backend: Every request fetches full context from PostgreSQL
- MCP-only agent: AI never touches database, only calls tools
- Persistent conversations: All messages stored with tool_calls metadata
- Horizontal scaling: Stateless design enables load balancing

**Data Model (4 entities)**:
1. User (id UUID, email, managed by Better Auth)
2. Conversation (id UUID, user_id FK, created_at, updated_at)
3. Message (id UUID, conversation_id FK, role enum, content text, tool_calls JSONB, tool_results JSONB, timestamp)
4. Task (id int, user_id FK, title varchar(500), description text, status enum, created_at, completed_at)

**API Contracts**:
- POST /api/chat: {user_id, message, conversation_id?} → {conversation_id, message{id, role, content, tool_calls, timestamp}}
- GET /api/conversations/{user_id}: → {conversations[{id, created_at, updated_at, message_count}]}

**MCP Tool Contracts (5 tools)**:
- add_task(user_id, title, description?) → {success, data{task_id, title, status}, message}
- list_tasks(user_id, status?) → {success, data{tasks[], count}, message}
- complete_task(user_id, task_id) → {success, data{task_id, title, status, completed_at}, message}
- update_task(user_id, task_id, title?, description?) → {success, data{task_id, title, description}, message}
- delete_task(user_id, task_id) → {success, data{task_id, title}, message}

**Error Response**: {success: false, error{type, message (friendly), details (technical)}}

**Performance Budgets**:
- Response time: <3 seconds
- Concurrent users: 100+
- Database latency: <200ms p95
- Conversation history: Up to 1000 messages
- Tasks per user: Up to 1000

**Risks & Mitigations**:
1. Large conversation histories → Monitor size, pagination if needed
2. Database connection limits → Connection pooling, Neon auto-scaling
3. AI context window exceeded → Conversation summarization strategy

## Outcome

- ✅ Impact: Created comprehensive implementation plan defining architecture, data models, API contracts, MCP tools, and research tasks. All constitution gates pass.
- 🧪 Tests: No tests (planning artifact). Plan defines test structure (backend/tests/{contract, integration, unit}).
- 📁 Files: Created specs/001-todo-ai-chatbot/plan.md (783 lines)
- 🔁 Next prompts: /sp.tasks to generate task breakdown; optionally /sp.adr to document architectural decisions
- 🧠 Reflection: Plan successfully translates spec requirements into concrete architecture. Three-tier design (ChatKit → FastAPI → MCP) with stateless backend enables horizontal scaling. All constitution principles enforced via gates. Research tasks identify key integration patterns. Design tasks specify data models and contracts. Ready for task breakdown phase.

## Evaluation notes (flywheel)

- Failure modes observed: None - plan is comprehensive and compliant
- Graders run and results (PASS/FAIL): Constitution Check - ALL 5 MANDATORY GATES PASS (Gate 6 conditional)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to /sp.tasks for implementation breakdown
