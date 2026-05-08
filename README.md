# Multi-Agent AI Internship Application System

Production-oriented platform to automate global research internship applications using a modular multi-agent architecture.

## Stack
- **Backend:** FastAPI, Pydantic, LangGraph, OpenAI API, PostgreSQL, Redis
- **Frontend:** Next.js, TailwindCSS, Axios
- **Infra:** Docker, docker-compose, GitHub Actions CI

## Core Agents
1. Resume Parser Agent (PDF/DOCX + OCR fallback)
2. Job Description Parser Agent
3. ATS Resume Generator Agent
4. Cover Letter Generator Agent
5. Verification Agent (0-100 scoring)
6. Feedback Loop Agent
7. Router Agent (LangGraph orchestration)

## Quick Start
```bash
# Start all services
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
docker compose up --build
```

- Backend API docs: http://localhost:8000/docs
- Frontend: http://localhost:3000

## Local Development
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Testing
```bash
cd backend
pytest -q
```

## Documentation
- Architecture: `/docs/architecture.md`
- Workflow: `/docs/workflow.md`
- Agent instructions: `/docs/skill.md`
