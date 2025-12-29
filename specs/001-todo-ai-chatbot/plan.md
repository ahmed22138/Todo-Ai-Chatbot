# Implementation Plan: Todo AI Chatbot

**Branch**: `001-todo-ai-chatbot` | **Date**: 2025-12-28 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-todo-ai-chatbot/spec.md`

## Summary

Build an AI-powered todo chatbot with natural language interface where users manage tasks conversationally. The system uses a stateless FastAPI backend that fetches conversation history from PostgreSQL on each request, invokes OpenAI Agents SDK to interpret user intent, and executes task operations exclusively through MCP tools. The chatbot provides friendly confirmations, maintains conversation continuity across sessions, and handles errors gracefully without exposing technical details.

**Primary Requirement**: Natural language task management (add, list, update, complete, delete) with persistent conversation history and zero server-side state.

**Technical Approach**: Three-tier architecture (ChatKit frontend → FastAPI backend → MCP tools) with PostgreSQL as single source of truth. OpenAI Agents SDK handles intent interpretation and tool orchestration. Every request is stateless - fetch full conversation context, process with AI agent, store results, return response.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, SQLModel, OpenAI Agents SDK, MCP SDK (official), ChatKit (frontend), Better Auth
**Storage**: Neon Serverless PostgreSQL (connection pooling, auto-scaling)
**Testing**: pytest, pytest-asyncio (for async tests), httpx (API client testing)
**Target Platform**: Cloud deployment (AWS/GCP/Azure) with containerized FastAPI backend, managed PostgreSQL
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <3 second response time, 100 concurrent users, <200ms p95 latency for database queries
**Constraints**: Stateless backend (no in-memory state), full conversation history fetched per request, MCP-only agent interaction, horizontal scaling support
**Scale/Scope**: MVP supports 100-1000 users, conversation history up to 1000 messages per user, task counts up to 1000 per user

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate 1: MCP-Only Tool Interface ✅ PASS

- ✓ All task operations (add, list, complete, update, delete) exposed as MCP tools
- ✓ Agent interacts ONLY through MCP tool calls (spec FR-008)
- ✓ No direct database access by agent
- ✓ Tool calls logged and included in API responses (spec FR-012)

**Evidence**: Spec FR-008 explicitly requires "AI agent MUST interact with task data exclusively through MCP tools" and constitution principle I enforces this.

### Gate 2: Stateless Backend Architecture ✅ PASS

- ✓ Backend holds no conversation or session state (spec FR-011)
- ✓ All state persisted in PostgreSQL (spec constraints)
- ✓ Every request fetches required context from database (spec FR-004)
- ✓ Server restarts do not affect behavior (spec SC-010)

**Evidence**: Spec FR-011 mandates "stateless backend architecture - no conversation context or session state stored in server memory between requests". Constitution principle II enforces this.

### Gate 3: Conversation Persistence ✅ PASS

- ✓ User messages stored BEFORE sending to agent (spec FR-003)
- ✓ Assistant responses stored BEFORE returning to client (spec FR-003)
- ✓ Full conversation history fetched per request (spec FR-004)
- ✓ Metadata captured (timestamp, role, tool_calls, tool_results) (spec entity: Message)

**Evidence**: Spec FR-003 and FR-004 explicitly require persistence before processing/returning and fetching complete history for each request. Constitution principle III enforces this.

### Gate 4: Database Isolation ✅ PASS

- ✓ Agent code contains no SQL or database imports
- ✓ MCP tools encapsulate ALL database logic (spec FR-008)
- ✓ Database schema hidden from agent context
- ✓ Tools validate and sanitize inputs (error handling requirement)

**Evidence**: Spec FR-008 ensures agent never accesses database directly. Constitution principle V enforces separation of concerns.

### Gate 5: Error Handling ✅ PASS

- ✓ User-facing messages are friendly and clear (spec FR-006, US3)
- ✓ Technical errors logged but not exposed (spec FR-009)
- ✓ Tool failures handled gracefully (spec US3 acceptance scenarios)
- ✓ Agent acknowledges tool results (spec FR-006)

**Evidence**: Spec US3 entirely focused on graceful error handling with 4 acceptance scenarios. Constitution principle VI enforces friendly error messages.

### Gate 6: Testing Discipline ⚠️ CONDITIONAL PASS

- Tests are OPTIONAL per spec (not explicitly required in user stories)
- IF tests are included: Write test → Verify fails → Implement → Verify passes
- Constitution principle VIII applies only when tests are required

**Evidence**: Spec does not mandate tests in deliverables. If tests are added during implementation, TDD discipline must be followed per constitution.

### Summary

**Status**: ✅ ALL MANDATORY GATES PASS

No constitution violations. All architectural principles align with spec requirements. Proceed to Phase 0 research.

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-ai-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── api.openapi.yaml # OpenAPI spec for REST endpoints
│   └── mcp.schema.json  # MCP tool schemas
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/          # SQLModel database models (User, Conversation, Message, Task)
│   ├── services/        # Business logic layer
│   │   ├── conversation_service.py  # Conversation history management
│   │   ├── auth_service.py          # Better Auth integration
│   │   └── agent_service.py         # OpenAI Agents SDK integration
│   ├── mcp/             # MCP tool implementations
│   │   ├── tools/       # Individual tool implementations
│   │   │   ├── add_task.py
│   │   │   ├── list_tasks.py
│   │   │   ├── complete_task.py
│   │   │   ├── update_task.py
│   │   │   └── delete_task.py
│   │   └── server.py    # MCP server registration and routing
│   ├── api/             # FastAPI routes and endpoints
│   │   ├── routes/
│   │   │   ├── chat.py          # POST /api/chat endpoint
│   │   │   ├── conversations.py # GET /api/conversations/{user_id}
│   │   │   └── auth.py          # Better Auth endpoints
│   │   └── middleware/  # Logging, error handling, CORS
│   ├── db/              # Database connection and migrations
│   │   ├── connection.py    # PostgreSQL connection pool
│   │   └── migrations/      # Alembic migration scripts
│   └── main.py          # FastAPI app entry point
└── tests/
    ├── contract/        # MCP tool contract tests
    ├── integration/     # API endpoint integration tests
    └── unit/            # Unit tests for services

frontend/
├── src/
│   ├── components/      # ChatKit components
│   │   ├── ChatInterface.tsx    # Main chat UI
│   │   ├── MessageList.tsx      # Message display
│   │   └── InputField.tsx       # User input
│   ├── pages/
│   │   ├── Login.tsx            # Better Auth login page
│   │   └── Chat.tsx             # Main chat page
│   ├── services/
│   │   ├── api.ts               # API client (fetch wrapper)
│   │   └── auth.ts              # Better Auth client
│   └── App.tsx          # Root component
└── tests/
    └── integration/     # E2E tests with Playwright

.env.example             # Environment variable template
docker-compose.yml       # Local development stack (PostgreSQL, backend, frontend)
```

**Structure Decision**: Web application structure chosen (Option 2 from template) because spec explicitly requires "ChatKit frontend" and "FastAPI backend" as separate components. Frontend uses TypeScript/React with ChatKit for chat UI. Backend uses Python with FastAPI for API server. Both interact exclusively via REST API (`POST /api/chat`). PostgreSQL is shared storage layer accessed only by backend.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations detected.** All constitution gates pass. No complexity justification required.

---

# Phase 0: Research & Technology Evaluation

## Research Tasks

### R1: OpenAI Agents SDK Integration Pattern

**Question**: How does OpenAI Agents SDK integrate with MCP tools for stateless request handling?

**Research Goals**:
- Understand Agents SDK initialization (per-request vs singleton)
- Learn MCP tool registration with Agents SDK
- Identify conversation history format expected by Agents SDK
- Determine tool call/result flow and JSON schema requirements

**Deliverable**: Document in research.md with code examples (pseudocode) and architecture diagram

---

### R2: Neon Serverless PostgreSQL Connection Pooling

**Question**: How should connection pooling be configured for stateless FastAPI backend with Neon PostgreSQL?

**Research Goals**:
- Identify recommended connection pool size for FastAPI async operations
- Understand Neon Serverless connection limits and scaling behavior
- Learn best practices for SQLModel + async PostgreSQL (asyncpg driver)
- Determine transaction handling for atomic message persistence

**Deliverable**: Document in research.md with connection configuration recommendations

---

### R3: ChatKit Integration with Custom API

**Question**: How does ChatKit consume a custom REST API for chat functionality?

**Research Goals**:
- Identify required API response format for ChatKit message display
- Understand authentication flow between ChatKit and Better Auth
- Learn message state management (optimistic updates vs server-driven)
- Determine real-time update mechanism (polling vs SSE - spec excludes SSE, so polling)

**Deliverable**: Document in research.md with ChatKit configuration and API contract

---

### R4: MCP Tool Error Handling Patterns

**Question**: How should MCP tools return errors to enable friendly agent responses?

**Research Goals**:
- Understand MCP error response schema (success/failure with message)
- Learn error categorization (user error vs system error)
- Identify retry semantics for transient failures (database unavailable)
- Determine error context needed for agent to craft helpful messages

**Deliverable**: Document in research.md with error response schemas and examples

---

### R5: Conversation History Context Window Management

**Question**: How to handle conversation history when it exceeds AI model context limits?

**Research Goals**:
- Identify OpenAI model context limits (tokens) for chosen model
- Learn conversation summarization strategies (sliding window, summarize old messages)
- Understand performance impact of fetching large conversation histories
- Determine pagination or truncation strategy

**Deliverable**: Document in research.md with context management strategy and thresholds

---

### R6: Better Auth Integration with FastAPI

**Question**: How does Better Auth provide authentication tokens that FastAPI can validate?

**Research Goals**:
- Understand Better Auth token format (JWT, session cookie)
- Learn FastAPI middleware for token validation
- Identify user ID extraction from authenticated requests
- Determine session expiry and refresh token handling

**Deliverable**: Document in research.md with authentication flow diagram

---

### R7: Horizontal Scaling Considerations

**Question**: What FastAPI deployment patterns support horizontal scaling with stateless architecture?

**Research Goals**:
- Identify load balancing strategies (round-robin, least connections)
- Understand session affinity requirements (none for stateless)
- Learn health check endpoints for container orchestration
- Determine database connection pooling per instance

**Deliverable**: Document in research.md with deployment architecture diagram

---

## Research Consolidation

After completing all research tasks, consolidate findings into `research.md` with sections:

1. **System Architecture Overview** (diagram + narrative)
2. **Technology Integration Patterns** (OpenAI SDK, MCP, ChatKit, Better Auth)
3. **Data Flow** (request lifecycle from user input to response)
4. **Error Handling Strategy** (MCP tool errors → agent responses)
5. **Scalability Approach** (connection pooling, horizontal scaling)
6. **Key Decisions** (context window limits, polling interval, connection pool size)
7. **Alternatives Considered** (what was evaluated but not chosen)

**Output**: `specs/001-todo-ai-chatbot/research.md`

---

# Phase 1: Design & Contracts

## Prerequisites

- `research.md` complete with all NEEDS CLARIFICATION resolved
- Technology integration patterns documented
- Key architectural decisions made

## Phase 1 Tasks

### D1: Data Model Design

**Input**: Spec entities (User, Conversation, Message, Task)

**Output**: `specs/001-todo-ai-chatbot/data-model.md`

**Content**:

1. **Entity: User** (managed by Better Auth, read-only for our app)
   - Fields: id (UUID), email (string), created_at (timestamp)
   - Relationships: has_many Conversations, has_many Tasks
   - Validation: Email format validation (handled by Better Auth)

2. **Entity: Conversation**
   - Fields: id (UUID, PK), user_id (UUID, FK to User), created_at (timestamp), updated_at (timestamp)
   - Relationships: belongs_to User, has_many Messages
   - Indexes: user_id (for fast lookup)
   - Constraints: user_id NOT NULL

3. **Entity: Message**
   - Fields:
     - id (UUID, PK)
     - conversation_id (UUID, FK to Conversation)
     - role (enum: 'user' | 'assistant')
     - content (text, required)
     - tool_calls (JSONB, nullable) - stores array of MCP tool invocations
     - tool_results (JSONB, nullable) - stores array of tool execution results
     - timestamp (timestamp with timezone, default NOW())
   - Relationships: belongs_to Conversation
   - Indexes: conversation_id (for fetching conversation history), timestamp (for ordering)
   - Constraints: conversation_id NOT NULL, role NOT NULL, content NOT NULL

4. **Entity: Task**
   - Fields:
     - id (integer, PK, auto-increment)
     - user_id (UUID, FK to User)
     - title (varchar(500), required)
     - description (text, nullable)
     - status (enum: 'incomplete' | 'complete', default 'incomplete')
     - created_at (timestamp with timezone, default NOW())
     - completed_at (timestamp with timezone, nullable)
   - Relationships: belongs_to User
   - Indexes: user_id (for user task isolation), status (for filtering)
   - Constraints: user_id NOT NULL, title NOT NULL, title max length 500 chars
   - Validation: When status changes to 'complete', set completed_at to NOW()

5. **Database Schema SQL** (Postgres DDL pseudocode):
   ```sql
   -- Users table (managed by Better Auth)
   -- Conversations table with user_id FK
   -- Messages table with conversation_id FK, JSONB columns for tool_calls/tool_results
   -- Tasks table with user_id FK, status enum
   -- Indexes on foreign keys and frequently queried columns
   ```

---

### D2: API Contract Design

**Input**: Spec functional requirements (FR-001 through FR-015)

**Output**: `specs/001-todo-ai-chatbot/contracts/api.openapi.yaml`

**Content**: OpenAPI 3.0 specification with endpoints:

1. **POST /api/chat**
   - Summary: Send message to chatbot and get response
   - Request Body:
     ```json
     {
       "user_id": "uuid",
       "message": "string (user input)",
       "conversation_id": "uuid (optional - creates new if not provided)"
     }
     ```
   - Response 200:
     ```json
     {
       "status": "success",
       "data": {
         "conversation_id": "uuid",
         "message": {
           "id": "uuid",
           "role": "assistant",
           "content": "string (AI response)",
           "tool_calls": [
             {
               "tool": "add_task",
               "parameters": { "title": "buy groceries" },
               "result": { "success": true, "task_id": 123, "message": "✓ Added task: buy groceries" }
             }
           ],
           "timestamp": "ISO8601"
         }
       },
       "metadata": {
         "timestamp": "ISO8601",
         "request_id": "uuid"
       }
     }
     ```
   - Response 401: Unauthorized (invalid/missing auth token)
   - Response 500: Internal server error (friendly message)

2. **GET /api/conversations/{user_id}**
   - Summary: Fetch conversation history for user
   - Path Parameters: user_id (UUID)
   - Query Parameters: limit (int, default 50), offset (int, default 0)
   - Response 200:
     ```json
     {
       "status": "success",
       "data": {
         "conversations": [
           {
             "id": "uuid",
             "created_at": "ISO8601",
             "updated_at": "ISO8601",
             "message_count": 42
           }
         ]
       }
     }
     ```

3. **POST /api/auth/login** (Better Auth managed)
4. **POST /api/auth/register** (Better Auth managed)

---

### D3: MCP Tool Contract Design

**Input**: Spec FR-008 (MCP tool requirements)

**Output**: `specs/001-todo-ai-chatbot/contracts/mcp.schema.json`

**Content**: JSON Schema for MCP tools:

1. **Tool: add_task**
   - Parameters:
     ```json
     {
       "user_id": "string (UUID)",
       "title": "string (required, max 500 chars)",
       "description": "string (optional)"
     }
     ```
   - Returns:
     ```json
     {
       "success": true,
       "data": {
         "task_id": 123,
         "title": "buy groceries",
         "status": "incomplete"
       },
       "message": "✓ Added task: buy groceries"
     }
     ```

2. **Tool: list_tasks**
   - Parameters:
     ```json
     {
       "user_id": "string (UUID)",
       "status": "string (optional: 'all' | 'incomplete' | 'complete', default 'all')"
     }
     ```
   - Returns:
     ```json
     {
       "success": true,
       "data": {
         "tasks": [
           { "id": 123, "title": "buy groceries", "status": "incomplete", "created_at": "ISO8601" }
         ],
         "count": 1
       },
       "message": "You have 1 incomplete task"
     }
     ```

3. **Tool: complete_task**
   - Parameters:
     ```json
     {
       "user_id": "string (UUID)",
       "task_id": "integer (required)"
     }
     ```
   - Returns:
     ```json
     {
       "success": true,
       "data": {
         "task_id": 123,
         "title": "buy groceries",
         "status": "complete",
         "completed_at": "ISO8601"
       },
       "message": "✓ Completed: buy groceries. Great job!"
     }
     ```

4. **Tool: update_task**
   - Parameters:
     ```json
     {
       "user_id": "string (UUID)",
       "task_id": "integer (required)",
       "title": "string (optional, max 500 chars)",
       "description": "string (optional)"
     }
     ```
   - Returns:
     ```json
     {
       "success": true,
       "data": {
         "task_id": 123,
         "title": "prepare keynote presentation",
         "description": "Updated description"
       },
       "message": "✓ Updated task: prepare keynote presentation"
     }
     ```

5. **Tool: delete_task**
   - Parameters:
     ```json
     {
       "user_id": "string (UUID)",
       "task_id": "integer (required)"
     }
     ```
   - Returns:
     ```json
     {
       "success": true,
       "data": {
         "task_id": 123,
         "title": "buy groceries (deleted)"
       },
       "message": "✓ Deleted task: buy groceries"
     }
     ```

**Error Response Format** (all tools):
```json
{
  "success": false,
  "error": {
    "type": "user_error | system_error",
    "message": "Friendly error message for agent to use",
    "details": "Technical details for logging (not shown to user)"
  }
}
```

---

### D4: Quickstart Guide

**Output**: `specs/001-todo-ai-chatbot/quickstart.md`

**Content**:

1. **Prerequisites**
   - Python 3.11+
   - Node.js 18+
   - PostgreSQL (or Neon account)
   - OpenAI API key

2. **Backend Setup**
   ```bash
   # Clone repo, navigate to backend/
   # Create virtual environment
   # Install dependencies: pip install -r requirements.txt
   # Copy .env.example to .env and fill in:
   #   DATABASE_URL=postgresql://...
   #   OPENAI_API_KEY=sk-...
   #   BETTER_AUTH_SECRET=...
   # Run migrations: alembic upgrade head
   # Start server: uvicorn src.main:app --reload
   ```

3. **Frontend Setup**
   ```bash
   # Navigate to frontend/
   # Install dependencies: npm install
   # Copy .env.example to .env and fill in:
   #   VITE_API_URL=http://localhost:8000
   #   VITE_BETTER_AUTH_URL=...
   # Start dev server: npm run dev
   ```

4. **Development Workflow**
   - Make changes to backend code in `backend/src/`
   - FastAPI auto-reloads on file changes
   - Make changes to frontend code in `frontend/src/`
   - Vite auto-reloads on file changes
   - Test API endpoints: `curl -X POST http://localhost:8000/api/chat`

5. **Testing**
   ```bash
   # Backend tests: pytest backend/tests/
   # Frontend tests: npm run test (in frontend/)
   ```

6. **Deployment** (overview)
   - Backend: Docker container deployed to AWS ECS / GCP Cloud Run / Azure Container Instances
   - Frontend: Static build deployed to Vercel / Netlify / S3 + CloudFront
   - Database: Neon Serverless PostgreSQL (managed)

---

## Phase 1 Completion Checklist

- [ ] `research.md` created with all technology integration patterns documented
- [ ] `data-model.md` created with 4 entities fully specified
- [ ] `contracts/api.openapi.yaml` created with OpenAPI spec for REST endpoints
- [ ] `contracts/mcp.schema.json` created with JSON schemas for 5 MCP tools
- [ ] `quickstart.md` created with setup and development instructions
- [ ] Agent context updated with new technology (OpenAI Agents SDK, MCP SDK)

---

# Phase 2: Architecture Decision Records (ADR)

**Note**: This section identifies architecturally significant decisions made during planning that should be documented as ADRs.

## Suggested ADRs

### ADR 001: Stateless Request Architecture with Full Conversation History Fetch

**Decision**: Every API request fetches the complete conversation history from PostgreSQL and provides it to the AI agent as context, rather than maintaining session state in memory.

**Significance**:
- Enables horizontal scaling without sticky sessions
- Simplifies backend deployment (no distributed cache needed)
- Increases database load as conversations grow
- Impacts response latency

**Alternatives Considered**:
- In-memory session cache with Redis: Adds infrastructure complexity, requires cache invalidation
- Sliding window (last N messages): Loses conversation context, impacts AI quality

**Recommendation**: Document with `/sp.adr stateless-conversation-architecture`

---

### ADR 002: MCP-Only Agent Interaction Pattern

**Decision**: AI agent interacts with task data exclusively through MCP tools; agent code never imports database modules or makes direct queries.

**Significance**:
- Enforces separation of concerns
- Prevents SQL injection via agent prompts
- Enables tool-level testing and mocking
- Requires well-designed tool interfaces

**Alternatives Considered**:
- Direct database access by agent: Simpler but violates security and testing principles
- Repository pattern with agent-aware ORM: Adds abstraction layer without clear benefit

**Recommendation**: Document with `/sp.adr mcp-only-agent-interaction`

---

### ADR 003: OpenAI Agents SDK for Intent Interpretation

**Decision**: Use OpenAI Agents SDK (not raw OpenAI API) for natural language intent interpretation and tool orchestration.

**Significance**:
- Agents SDK handles tool calling lifecycle
- Provides built-in retry and error handling
- Locks us into OpenAI ecosystem (migration to other LLMs requires SDK change)

**Alternatives Considered**:
- Raw OpenAI API with function calling: More control, more code to maintain
- LangChain agents: Feature-rich but heavyweight, overkill for our use case

**Recommendation**: Document with `/sp.adr openai-agents-sdk-for-intent`

---

## ADR Suggestion Output

After planning is complete, suggest these ADRs to the user:

```
📋 Architectural decisions detected. Document reasoning and tradeoffs?

1. Stateless Conversation Architecture - Run: /sp.adr stateless-conversation-architecture
2. MCP-Only Agent Interaction - Run: /sp.adr mcp-only-agent-interaction
3. OpenAI Agents SDK for Intent - Run: /sp.adr openai-agents-sdk-for-intent
```

---

# Post-Phase 1 Constitution Re-Check

**All gates re-evaluated after design phase:**

### Gate 1: MCP-Only Tool Interface ✅ PASS (confirmed)
- Design includes 5 MCP tools in `contracts/mcp.schema.json`
- Agent service will only invoke tools, never database

### Gate 2: Stateless Backend Architecture ✅ PASS (confirmed)
- API design shows conversation_id in request, full history fetched from DB
- No session state in FastAPI application

### Gate 3: Conversation Persistence ✅ PASS (confirmed)
- Data model includes Message entity with tool_calls/tool_results JSONB columns
- API contract shows messages stored before agent processing

### Gate 4: Database Isolation ✅ PASS (confirmed)
- MCP tools encapsulate all database logic (separate from agent service)
- Agent service only sees tool interfaces

### Gate 5: Error Handling ✅ PASS (confirmed)
- MCP tool contract includes friendly error messages
- API contract returns user-friendly errors

### Gate 6: Testing Discipline ⚠️ CONDITIONAL (not applicable yet)
- No tests written in planning phase (spec does not require tests)

**Final Status**: ✅ ALL GATES PASS

---

# Summary & Next Steps

## Deliverables Created

1. ✅ `plan.md` - This comprehensive implementation plan
2. 🔄 `research.md` - To be created in Phase 0 (technology integration research)
3. 🔄 `data-model.md` - To be created in Phase 1 (entity and schema design)
4. 🔄 `contracts/api.openapi.yaml` - To be created in Phase 1 (REST API specification)
5. 🔄 `contracts/mcp.schema.json` - To be created in Phase 1 (MCP tool schemas)
6. 🔄 `quickstart.md` - To be created in Phase 1 (development guide)

## Architectural Highlights

- **Three-tier architecture**: ChatKit (UI) → FastAPI (API) → MCP Tools (data)
- **Stateless backend**: Every request fetches full context from PostgreSQL
- **MCP-only agent**: AI never touches database, only calls tools
- **Persistent conversations**: All messages stored with tool_calls metadata
- **Horizontal scaling**: Stateless design enables load balancing across instances

## Key Design Decisions

1. **Full conversation history fetch per request** (enables stateless, impacts DB load)
2. **MCP tools return friendly error messages** (agent uses them in responses)
3. **OpenAI Agents SDK handles tool orchestration** (simpler than raw API)
4. **Neon Serverless PostgreSQL** (auto-scaling, connection pooling)
5. **Better Auth for authentication** (JWT tokens, user_id extraction)

## Performance Budgets

- **Response time**: <3 seconds (spec SC-006)
- **Concurrent users**: 100+ (spec SC-003)
- **Database query latency**: <200ms p95
- **Conversation history**: Up to 1000 messages (spec edge case)
- **Task count**: Up to 1000 per user

## Risks & Mitigations

1. **Risk**: Fetching large conversation histories impacts latency
   - **Mitigation**: Monitor conversation size, implement pagination if needed (research task R5)

2. **Risk**: Database connection limits with high concurrency
   - **Mitigation**: Connection pooling per backend instance, Neon auto-scaling (research task R2)

3. **Risk**: AI context window exceeded with long conversations
   - **Mitigation**: Conversation summarization strategy (research task R5)

## Next Command

Run `/sp.tasks` to generate implementation task breakdown from this plan.

**Prerequisites for /sp.tasks**:
- This plan.md
- specs/001-todo-ai-chatbot/spec.md (already exists)
- Constitution compliance confirmed (all gates pass)

The task breakdown will organize work by user story (P1, P2, P3) with parallel opportunities marked and dependencies specified.
