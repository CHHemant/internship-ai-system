# Workflow

## Agent Execution Order

```
ResumeParserAgent  ──┐
                     ├──▶ RouterAgent (LangGraph StateGraph)
JobDescParserAgent ──┘       │
                             ▼
                    ┌── generate node ──┐
                    │  ATSResumeGenerator│
                    │  CoverLetterAgent  │
                    └────────┬──────────┘
                             ▼
                    ┌── verify node ─────┐
                    │  VerificationAgent  │
                    └────────┬───────────┘
                             │
               score ≥ 80 ◄──┴──▶ score < 80 & retries left
                    │                       │
                    ▼                       ▼
               END (finalized)     improve node
                                   (FeedbackLoopAgent)
                                   regenerates & re-verifies
```

## Step-by-Step Reference

### 1. Resume Upload — `POST /api/resume/upload`

- **Input:** multipart file (PDF, DOCX, or plain text)
- **Agent:** `ResumeParserAgent`
  - PDF: extracted with PyMuPDF (`fitz`); falls back to Tesseract OCR when text layer is absent.
  - DOCX: extracted with `python-docx`.
  - Sections detected by keyword hints: education, experience, projects, certifications, research.
- **Output stored:** `CandidateProfile` row in PostgreSQL; `ResumeProfile` JSON cached in Redis under `candidate:{id}:profile`.
- **Response:** `{ candidate_id, profile }` — use `candidate_id` in subsequent requests.

### 2. Job Description Parsing — `POST /api/job/parse`

- **Input:** `{ "job_description": "<raw text>" }`
- **Agent:** `JobDescriptionParserAgent`
  - Regex tokenises the text; top 40 unique keywords extracted.
  - Lines with "required / must / qualification / eligibility" → `required_skills`.
  - Known tech names → `technologies`; known research domains → `research_domains`.
- **Output:** `JobDescriptionData` JSON (keywords, required_skills, technologies, research_domains, responsibilities, eligibility_requirements).

### 3. Full Application Run — `POST /api/applications/run`

- **Input:** `{ "candidate_id": <int>, "job_description": "<text>", "country": "<code>" }`
  - `profile` (inline `ResumeProfile`) may be used instead of `candidate_id`.
  - `country` accepts: `usa`, `canada`, `germany`, `uk`, `europe`, `global` (default).
- **Orchestrator:** `RouterAgent` (LangGraph `StateGraph`)
  - **generate node** — `ATSResumeGeneratorAgent` + `CoverLetterGeneratorAgent` call OpenAI in sequence.
  - **verify node** — `VerificationAgent` scores both documents.
  - **conditional edge** — routes to `improve` if `score < 80` and `retries < max_retries` (default 2), otherwise to `END`.
  - **improve node** — regenerates both documents, increments retry counter, returns to verify.
- **Output stored:** `Application` row in PostgreSQL; summary cached in Redis under `application:{id}`.
- **Response:** `{ application_id, resume, cover_letter, verification }`.

### 4. Generate Resume Only — `POST /api/generate/resume`

Same input as `/api/applications/run`; returns only the resume and verification result without persisting a full application record.

### 5. Generate Cover Letter Only — `POST /api/generate/cover-letter`

Same input as above; returns only the cover letter and verification result.

### 6. Application History — `GET /api/applications/history`

Returns all `Application` rows ordered by `created_at DESC`.  
Each item: `{ id, candidate_id, country, verification_score, created_at }`.

### 7. Verification Detail — `GET /api/applications/{id}/verification`

Returns the full `VerificationResult` for a specific application:
`{ score, ats_score, keyword_coverage, grammar_score, hallucination_risk, relevance_score, issues }`.

### 8. Internship Recommendations — `POST /api/recommendations`

- **Input:** `{ "profile": <ResumeProfile>, "internships": [<list of job objects>] }`
- **Service:** `InternshipRecommendationService`
  - Scores each listing by counting profile keywords (skills + research_interests) that appear in the listing text; normalises to 0–100.
  - Extracts `professor` / `lab` fields for suggested contact list.
- **Output:** `{ ranked_internships: [...], suggested_professors_or_labs: [...] }`.

## Verification Score Formula

| Dimension | Computation |
|-----------|-------------|
| `ats_score` | `min(100, 55 + keyword_coverage × 0.45)` |
| `keyword_coverage` | `matched / total_job_keywords × 100` |
| `grammar_score` | 90 if resume > 100 words and cover > 80 words, else 75 |
| `hallucination_risk` | 10 normally; 50 if "lorem" placeholder found |
| `relevance_score` | `(keyword_coverage + ats_score) / 2` |
| **composite `score`** | `(ats_score + keyword_coverage + grammar_score + (100 − hallucination_risk) + relevance_score) / 5` |

Issues flagged: `keyword_coverage < 60`, `grammar_score < 80`, `hallucination_risk > 20`.
