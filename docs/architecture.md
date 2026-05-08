# Architecture

## High-Level Design

```
┌──────────────────────────────────────────────────────┐
│  Frontend (Next.js + TailwindCSS)                    │
│  Pages: / · /upload · /dashboard · /results          │
│         /history · /settings                         │
└────────────────────┬─────────────────────────────────┘
                     │ HTTP / REST
┌────────────────────▼─────────────────────────────────┐
│  Backend (FastAPI)                                    │
│  routes/application.py — single router, /api prefix  │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │  Agents                                         │ │
│  │  ├── ResumeParserAgent       (PDF/DOCX/OCR)     │ │
│  │  ├── JobDescriptionParserAgent (regex/keyword)  │ │
│  │  ├── ATSResumeGeneratorAgent  (OpenAI)          │ │
│  │  ├── CoverLetterGeneratorAgent(OpenAI)          │ │
│  │  ├── VerificationAgent        (heuristic score) │ │
│  │  ├── FeedbackLoopAgent        (retry loop)      │ │
│  │  └── RouterAgent              (LangGraph)       │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │  Services                                       │ │
│  │  ├── OpenAIService        (chat completion)     │ │
│  │  ├── AgentMemoryStore     (Redis get/set)       │ │
│  │  ├── InternshipRecommendationService (ranking)  │ │
│  │  └── RankingService       (score helpers)       │ │
│  └─────────────────────────────────────────────────┘ │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │  Utils                                          │ │
│  │  ├── country_formatting   (per-country rules)   │ │
│  │  ├── text                 (normalise, split)    │ │
│  │  └── logging              (structured logs)     │ │
│  └─────────────────────────────────────────────────┘ │
└──────────────┬────────────────────────┬──────────────┘
               │                        │
   ┌───────────▼──────────┐  ┌─────────▼──────────────┐
   │  PostgreSQL           │  │  Redis                  │
   │  CandidateProfile     │  │  candidate:{id}:profile │
   │  Application          │  │  application:{id}       │
   └──────────────────────┘  └────────────────────────┘
```

## Data Stores

### PostgreSQL (SQLAlchemy ORM)
- **`CandidateProfile`** — candidate name, email, full `profile_json` (`ResumeProfile`).
- **`Application`** — links to candidate; stores country, raw job description, `parsed_job_json`, generated resume and cover letter, `verification_score`, full `verification_json`.

### Redis (AgentMemoryStore)
- Short-lived JSON blobs keyed by `candidate:{id}:profile` and `application:{id}`.
- Used by agents for lightweight cross-request state hints without hitting PostgreSQL.

## Orchestration (LangGraph StateGraph)

`RouterAgent` compiles a `StateGraph[WorkflowState]` at startup:

```
Entry ──▶ generate ──▶ verify ──▶ [conditional]
                          ▲              │
                          │     score < 80 & retries < max_retries
                          │              ▼
                          └────── improve
                                         │
                              score ≥ 80 or retries exhausted
                                         ▼
                                        END
```

`WorkflowState` carries: `profile`, `job`, `country`, `generated_resume`, `generated_cover_letter`, `verification`, `retries`.

## Country Formatting

`utils/country_formatting.py` maps country codes to prose formatting instructions injected into the ATS Resume Generator system prompt:

| Code | Instruction |
|------|-------------|
| `usa` | One-page, impact bullets, measurable outcomes |
| `canada` | Clear section headers with concise summary and skills matrix |
| `germany` | Structured chronology with technical depth and education details |
| `uk` | Achievement-focused bullets and concise project context |
| `europe` | Europass-compatible ordering with clarity in academic research |
| `global` | ATS-safe plain text layout with role-specific keywords |

## API Surface (`routes/application.py`)

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/resume/upload` | Parse resume file, store candidate profile |
| POST | `/api/job/parse` | Parse job description text |
| POST | `/api/generate/resume` | Generate resume only (no DB persist) |
| POST | `/api/generate/cover-letter` | Generate cover letter only (no DB persist) |
| POST | `/api/applications/run` | Full pipeline run, persist application record |
| GET | `/api/applications/history` | List all past applications |
| GET | `/api/applications/{id}/verification` | Verification scores for one application |
| POST | `/api/recommendations` | Rank internship listings against a profile |
