# Architecture

## High-Level Design
- `backend/app/agents`: autonomous task agents
- `backend/app/routes`: API surface for upload, parsing, generation, history, and verification
- `backend/app/database`: SQLAlchemy models and DB session
- `backend/app/services`: OpenAI integration, memory, ranking, recommendation
- `backend/app/utils`: logging and formatting utilities
- `frontend/src/app`: UI pages and user workflows

## Data Stores
- PostgreSQL for persistent entities (profiles, applications, generated artifacts, verification)
- Redis for short-lived agent memory and workflow state hints

## Orchestration
LangGraph router controls:
1. Generate resume + cover letter
2. Verify outputs
3. Retry improvement loop when score < 80
4. Return finalized artifacts and scores
