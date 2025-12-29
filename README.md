# Todo AI Chatbot

A natural language task management application powered by OpenAI's GPT-4 with Model Context Protocol (MCP) architecture.

## Features

- **Natural Language Task Management**: Add, list, complete, update, and delete tasks using conversational language
- **AI-Powered Intent Recognition**: OpenAI GPT-4 interprets user intent and executes appropriate actions
- **Persistent Conversations**: Full conversation history maintained across sessions
- **MCP Architecture**: Agent never accesses database directly - all operations through well-defined tool interfaces
- **Friendly Error Handling**: User-friendly error messages for all failure scenarios

## Architecture

- **Backend**: FastAPI with async PostgreSQL (SQLModel + asyncpg)
- **Frontend**: React + TypeScript with ChatKit UI
- **AI Agent**: OpenAI Agents SDK with custom MCP tools
- **Authentication**: Better Auth with JWT tokens
- **Database**: PostgreSQL with Alembic migrations

## Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **PostgreSQL 14+** (or use Docker)
- **OpenAI API Key**

## Quick Start

### 1. Clone and Setup Environment

```bash
# Clone the repository
cd todo-ai-chatbot

# Copy backend environment template
cp backend/.env.example backend/.env

# Copy frontend environment template
cp frontend/.env.example frontend/.env
```

### 2. Configure Environment Variables

**Backend** (`backend/.env`):
```env
# Database
DATABASE_URL=postgresql+asyncpg://todo_user:todo_password@localhost:5432/todo_chatbot

# OpenAI
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4-turbo-preview

# Authentication (generate a random 32+ character string)
BETTER_AUTH_SECRET=your-secret-key-here-minimum-32-characters-long

# Environment
ENVIRONMENT=development

# Frontend
FRONTEND_ORIGIN=http://localhost:3000
```

**Frontend** (`frontend/.env`):
```env
# Backend API URL
VITE_API_BASE_URL=http://localhost:8000
```

### 3. Start PostgreSQL (Docker)

```bash
docker compose up -d
```

Or use your own PostgreSQL instance and create the database:
```sql
CREATE DATABASE todo_chatbot;
CREATE USER todo_user WITH PASSWORD 'todo_password';
GRANT ALL PRIVILEGES ON DATABASE todo_chatbot TO todo_user;
```

### 4. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start backend server
python -m src.main
```

Backend will start on `http://localhost:8000`

### 5. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will start on `http://localhost:3000`

## Usage Examples

### Natural Language Commands

```
"add buy groceries"
→ Creates task: "buy groceries"

"what tasks do I have?"
→ Lists all your tasks

"list incomplete tasks"
→ Shows only incomplete tasks

"mark task 5 as complete"
→ Marks task #5 as complete

"update task 3 title to buy organic groceries"
→ Updates task #3

"delete task 7"
→ Deletes task #7
```

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

- `POST /api/chat` - Send chat message and get AI response
- `GET /api/conversations` - List user's conversations
- `GET /api/conversations/{id}/messages` - Get conversation history
- `GET /health` - Health check

## Project Structure

```
todo-ai-chatbot/
├── backend/
│   ├── src/
│   │   ├── api/            # FastAPI routes and middleware
│   │   ├── db/             # Database connection and migrations
│   │   ├── mcp/            # MCP tools for task management
│   │   ├── models/         # SQLModel database models
│   │   ├── services/       # Business logic (agent, auth, conversation)
│   │   └── main.py         # FastAPI application entry point
│   ├── requirements.txt    # Python dependencies
│   └── alembic.ini         # Database migration config
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   └── services/       # API client
│   ├── package.json        # Node dependencies
│   └── vite.config.ts      # Vite configuration
├── docker-compose.yml      # PostgreSQL container
└── .env.example            # Environment variables template
```

## Development

### Database Migrations

```bash
# Create new migration
cd backend
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

### Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality

```bash
# Backend linting
cd backend
ruff check .
black .

# Frontend linting
cd frontend
npm run lint
npm run format
```

## Environment Variables Reference

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `DATABASE_URL` | Yes | PostgreSQL connection string | - |
| `OPENAI_API_KEY` | Yes | OpenAI API key | - |
| `BETTER_AUTH_SECRET` | Yes | JWT secret (32+ chars) | - |
| `OPENAI_MODEL` | No | OpenAI model to use | gpt-4-turbo-preview |
| `ENVIRONMENT` | No | Environment (development/production) | development |
| `FRONTEND_ORIGIN` | No | Frontend URL for CORS | http://localhost:3000 |

## Troubleshooting

### Backend won't start
- Check environment variables are set correctly
- Ensure PostgreSQL is running and accessible
- Verify OpenAI API key is valid

### Database connection errors
- Check `DATABASE_URL` format
- Ensure PostgreSQL is running: `docker compose ps`
- Verify database exists: `psql -U todo_user -d todo_chatbot`

### Frontend can't connect to backend
- Ensure backend is running on port 8000
- Check CORS configuration in backend
- Verify `VITE_API_BASE_URL` in frontend

## License

MIT

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request
