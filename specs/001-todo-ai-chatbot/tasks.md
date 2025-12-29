---

description: "Task list for Todo AI Chatbot implementation"
---

# Tasks: Todo AI Chatbot

**Input**: Design documents from `/specs/001-todo-ai-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Tests are OPTIONAL - not explicitly required in the feature specification. If tests are added, follow TDD discipline (write test → verify it fails → implement → verify it passes).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Backend structure: `backend/src/{models, services, mcp/tools, api/routes, db}`
- Frontend structure: `frontend/src/{components, pages, services}`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend directory structure (backend/src/{models,services,mcp,api,db}, backend/tests/)
- [x] T002 Create frontend directory structure (frontend/src/{components,pages,services}, frontend/tests/)
- [x] T003 Initialize Python backend with FastAPI dependencies (fastapi, sqlmodel, openai, asyncpg, alembic)
- [x] T004 [P] Initialize TypeScript frontend with React, ChatKit, and Better Auth dependencies
- [x] T005 [P] Create .env.example with required environment variables (DATABASE_URL, OPENAI_API_KEY, BETTER_AUTH_SECRET)
- [x] T006 [P] Create docker-compose.yml for local PostgreSQL development database
- [x] T007 [P] Configure linting and formatting (black, ruff for Python; prettier, eslint for TypeScript)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T008 Create SQLModel database models in backend/src/models/user.py (User entity - id, email, created_at)
- [x] T009 [P] Create SQLModel database models in backend/src/models/conversation.py (Conversation entity - id, user_id FK, created_at, updated_at)
- [x] T010 [P] Create SQLModel database models in backend/src/models/message.py (Message entity - id, conversation_id FK, role enum, content, tool_calls JSONB, tool_results JSONB, timestamp)
- [x] T011 [P] Create SQLModel database models in backend/src/models/task.py (Task entity - id, user_id FK, title varchar(500), description, status enum, created_at, completed_at)
- [x] T012 Setup database connection pool in backend/src/db/connection.py (async PostgreSQL with SQLModel, connection pooling)
- [x] T013 Initialize Alembic for database migrations in backend/src/db/migrations/
- [x] T014 Generate initial migration for User, Conversation, Message, Task tables
- [x] T015 Implement Better Auth integration in backend/src/services/auth_service.py (JWT token validation, user_id extraction)
- [x] T016 [P] Create authentication middleware in backend/src/api/middleware/auth.py (validate tokens, attach user_id to request)
- [x] T017 [P] Create error handling middleware in backend/src/api/middleware/error_handler.py (catch exceptions, return friendly JSON errors)
- [x] T018 [P] Create CORS middleware configuration in backend/src/api/middleware/cors.py (allow frontend origin)
- [x] T019 Create FastAPI application entry point in backend/src/main.py (initialize app, register middleware, include routers)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Natural Language Task Management (Priority: P1) 🎯 MVP

**Goal**: Users can manage todos via natural language (add, list, update, complete, delete) with AI intent interpretation and friendly confirmations.

**Independent Test**: Send natural language messages like "add buy groceries", "what tasks do I have?", "mark groceries as done" and verify chatbot correctly interprets intent and executes task operations with friendly confirmations.

### Implementation for User Story 1

- [x] T020 [P] [US1] Implement add_task MCP tool in backend/src/mcp/tools/add_task.py (accepts user_id, title, description; creates Task in DB; returns success with friendly message)
- [x] T021 [P] [US1] Implement list_tasks MCP tool in backend/src/mcp/tools/list_tasks.py (accepts user_id, status filter; queries Tasks by user_id; returns task list with count and friendly message)
- [x] T022 [P] [US1] Implement complete_task MCP tool in backend/src/mcp/tools/complete_task.py (accepts user_id, task_id; updates status to 'complete', sets completed_at; returns success with congratulatory message)
- [x] T023 [P] [US1] Implement update_task MCP tool in backend/src/mcp/tools/update_task.py (accepts user_id, task_id, optional title, optional description; updates Task fields; returns success with confirmation)
- [x] T024 [P] [US1] Implement delete_task MCP tool in backend/src/mcp/tools/delete_task.py (accepts user_id, task_id; deletes Task from DB; returns success with confirmation)
- [x] T025 [US1] Register all 5 MCP tools in backend/src/mcp/server.py (create MCP server instance, register add_task, list_tasks, complete_task, update_task, delete_task with JSON schemas)
- [x] T026 [US1] Implement OpenAI Agents SDK integration in backend/src/services/agent_service.py (initialize agent with MCP tools, accept conversation history, invoke agent with user message, return agent response with tool_calls metadata)
- [x] T027 [US1] Implement POST /api/chat endpoint in backend/src/api/routes/chat.py (accept user_id, message, optional conversation_id; create/fetch conversation; store user message; invoke agent_service; store assistant message with tool_calls; return response)
- [x] T028 [US1] Add chat route to FastAPI application in backend/src/main.py (include chat router)
- [x] T029 [US1] Create API client service in frontend/src/services/api.ts (implement POST /api/chat with fetch, handle responses, extract message and tool_calls)
- [x] T030 [P] [US1] Create ChatInterface component in frontend/src/components/ChatInterface.tsx (main chat UI using ChatKit, handles message sending, displays responses)
- [x] T031 [P] [US1] Create MessageList component in frontend/src/components/MessageList.tsx (displays conversation history, shows tool call results as badges or tags)
- [x] T032 [P] [US1] Create InputField component in frontend/src/components/InputField.tsx (text input for user messages, send button, handle enter key)
- [x] T033 [US1] Create Chat page in frontend/src/pages/Chat.tsx (compose ChatInterface with MessageList and InputField, manage chat state)
- [x] T034 [US1] Connect Chat page to API client in frontend/src/pages/Chat.tsx (send messages via api.ts, update UI with responses)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Users can add, list, complete, update, and delete tasks using natural language.

---

## Phase 4: User Story 2 - Persistent Conversation Continuity (Priority: P2)

**Goal**: Conversation history persists across sessions and devices. Users can close the chat, return later, and see full history with AI maintaining context.

**Independent Test**: Have a conversation, close browser, reopen, and verify chat history is intact and AI can reference previous tasks/context without user repeating information.

### Implementation for User Story 2

- [x] T035 [P] [US2] Implement conversation_service in backend/src/services/conversation_service.py (create_conversation, get_conversation_by_id, get_conversations_by_user, fetch_conversation_history with all messages ordered by timestamp)
- [x] T036 [US2] Update POST /api/chat to fetch full conversation history before invoking agent in backend/src/api/routes/chat.py (call conversation_service.fetch_conversation_history, pass to agent_service as context)
- [x] T037 [P] [US2] Implement GET /api/conversations/{user_id} endpoint in backend/src/api/routes/conversations.py (fetch user conversations with message counts, support pagination with limit/offset)
- [x] T038 [US2] Add conversations route to FastAPI application in backend/src/main.py (include conversations router)
- [x] T039 [US2] Update api.ts to fetch conversation history in frontend/src/services/api.ts (implement GET /api/conversations/{user_id}, parse response)
- [x] T040 [US2] Update Chat page to load conversation history on mount in frontend/src/pages/Chat.tsx (call api.fetchConversations on component mount, display in MessageList)
- [x] T041 [US2] Implement conversation switching in frontend/src/pages/Chat.tsx (allow users to select previous conversations, load full message history when selected)
- [x] T042 [US2] Add conversation_id persistence in frontend (store active conversation_id in localStorage or state, send with each message to maintain thread)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Users can manage tasks AND see conversation history preserved across sessions.

---

## Phase 5: User Story 3 - Graceful Error Handling (Priority: P3)

**Goal**: All error conditions (database failures, invalid requests, ambiguous input) result in friendly, actionable error messages rather than technical stack traces or silent failures.

**Independent Test**: Simulate error conditions (database unavailable, malformed requests, ambiguous input like "update that" with multiple tasks) and verify users receive helpful, human-readable error messages with suggested next steps.

### Implementation for User Story 3

- [x] T043 [P] [US3] Add error response wrapper to all MCP tools in backend/src/mcp/tools/ (wrap database operations in try/catch, return {success: false, error: {type, message, details}} on failures)
- [x] T044 [US3] Implement friendly error message generation in MCP tools (user_error for not found/ambiguous, system_error for DB failures, include actionable suggestions in message field)
- [x] T045 [US3] Update agent_service to handle tool errors gracefully in backend/src/services/agent_service.py (detect tool error responses, instruct agent to craft friendly response based on error.message)
- [x] T046 [US3] Update error_handler middleware to catch all exceptions in backend/src/api/middleware/error_handler.py (catch DB connection errors, validation errors, unexpected exceptions; log details; return user-friendly JSON with actionable messages)
- [x] T047 [US3] Add database connection health check in backend/src/db/connection.py (implement ping/health check, raise exception with friendly message if DB unavailable)
- [x] T048 [US3] Add request validation to POST /api/chat in backend/src/api/routes/chat.py (validate user_id format, message not empty, return 400 Bad Request with helpful message on validation failure)
- [x] T049 [US3] Implement error display in frontend in frontend/src/components/ChatInterface.tsx (detect error responses from API, display error.message to user in chat UI with error styling)
- [x] T050 [US3] Add retry logic for transient errors in frontend/src/services/api.ts (implement exponential backoff retry for 500/503 errors, max 3 retries)
- [x] T051 [US3] Add loading and error states to Chat page in frontend/src/pages/Chat.tsx (show loading spinner while request pending, show error banner if request fails after retries)

**Checkpoint**: All user stories should now be independently functional with production-ready error handling. System gracefully handles all failure modes.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and production readiness

- [x] T052 [P] Create Better Auth login page in frontend/src/pages/Login.tsx (login form, integrate Better Auth, redirect to Chat on success)
- [x] T053 [P] Integrate Better Auth in frontend/src/services/auth.ts (implement login, logout, getUser, token refresh)
- [x] T054 [P] Add protected route wrapper for Chat page in frontend/src/App.tsx (redirect to Login if not authenticated)
- [x] T055 [P] Implement logging in backend (structured logging with user_id, request_id, log all API requests, tool calls, errors to stdout for container logging)
- [x] T056 [P] Add request_id generation and tracking in backend/src/api/middleware/ (generate UUID per request, attach to logs, return in API response metadata)
- [x] T057 [P] Create environment variable validation on backend startup in backend/src/main.py (check DATABASE_URL, OPENAI_API_KEY, BETTER_AUTH_SECRET are set, exit with clear error if missing)
- [x] T058 [P] Document setup instructions in README.md (prerequisites, backend setup, frontend setup, running locally, environment variables)
- [x] T059 [P] Create Dockerfile for backend (Python 3.11 base, install dependencies, run uvicorn)
- [x] T060 [P] Create Dockerfile for frontend (Node 18 base, build static assets, serve with nginx)
- [x] T061 [P] Add health check endpoint GET /health in backend/src/api/routes/health.py (return 200 OK if DB connection alive)
- [x] T062 [P] Implement conversation history pagination in backend (modify fetch_conversation_history to support offset/limit, avoid loading 1000+ messages at once)
- [x] T063 [P] Add input sanitization for task titles in backend/src/mcp/tools/add_task.py and update_task.py (trim whitespace, enforce 500 char max, strip potentially dangerous characters)
- [x] T064 Code cleanup and remove unused imports across backend and frontend
- [x] T065 Run final validation (start backend, start frontend, test all 3 user stories end-to-end)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds on US1 but is independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Enhances US1 and US2 but is independently testable

### Within Each User Story

- MCP tools (T020-T024) can run in parallel - different files, no dependencies
- MCP server registration (T025) depends on all 5 tools being complete
- Agent service (T026) can run in parallel with MCP tools
- API endpoint (T027-T028) depends on agent_service and MCP server
- Frontend components (T030-T032) can run in parallel - different files
- Frontend integration (T033-T034) depends on components and API client

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All MCP tools within a user story marked [P] can run in parallel
- All frontend components within a user story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all MCP tools together:
Task T020: "Implement add_task MCP tool in backend/src/mcp/tools/add_task.py"
Task T021: "Implement list_tasks MCP tool in backend/src/mcp/tools/list_tasks.py"
Task T022: "Implement complete_task MCP tool in backend/src/mcp/tools/complete_task.py"
Task T023: "Implement update_task MCP tool in backend/src/mcp/tools/update_task.py"
Task T024: "Implement delete_task MCP tool in backend/src/mcp/tools/delete_task.py"
Task T026: "Implement OpenAI Agents SDK integration in backend/src/services/agent_service.py"

# After tools complete, register MCP server:
Task T025: "Register all 5 MCP tools in backend/src/mcp/server.py"

# After MCP server + agent service complete, build API:
Task T027: "Implement POST /api/chat endpoint in backend/src/api/routes/chat.py"

# Launch all frontend components together:
Task T029: "Create API client service in frontend/src/services/api.ts"
Task T030: "Create ChatInterface component in frontend/src/components/ChatInterface.tsx"
Task T031: "Create MessageList component in frontend/src/components/MessageList.tsx"
Task T032: "Create InputField component in frontend/src/components/InputField.tsx"

# After components complete, integrate:
Task T033: "Create Chat page in frontend/src/pages/Chat.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

**MVP Deliverable**: Natural language todo management working end-to-end. Users can add, list, complete, update, delete tasks conversationally.

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo (adds conversation persistence)
4. Add User Story 3 → Test independently → Deploy/Demo (production-ready error handling)
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (backend MCP tools + agent service)
   - Developer B: User Story 1 (frontend components)
   - Developer C: User Story 2 (conversation persistence)
3. Stories complete and integrate independently

---

## Task Count Summary

- **Phase 1 (Setup)**: 7 tasks
- **Phase 2 (Foundational)**: 12 tasks
- **Phase 3 (User Story 1 - P1)**: 15 tasks
- **Phase 4 (User Story 2 - P2)**: 8 tasks
- **Phase 5 (User Story 3 - P3)**: 9 tasks
- **Phase 6 (Polish)**: 14 tasks

**Total Tasks**: 65

**Parallel Opportunities**: 38 tasks marked with [P] (can run concurrently with other [P] tasks in same phase)

**Independent Tests**:
- US1: Send "add buy groceries", verify task created with friendly confirmation
- US2: Close/reopen chat, verify full conversation history persists
- US3: Simulate DB error, verify friendly error message (not stack trace)

**Suggested MVP Scope**: Phase 1 + Phase 2 + Phase 3 (User Story 1 only) = 34 tasks

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Tests are optional per spec (not included in task list, but can be added following TDD if desired)
