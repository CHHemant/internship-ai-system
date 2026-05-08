# AI Agent Skill Instructions

## Global Rules

- **Never fabricate** skills, experience, publications, or achievements that are absent from the candidate's profile.
- **Preserve factual details** exactly: names, dates, institution names, technology names.
- **Prefer ATS-safe plain text** layout: no tables, no columns, no special Unicode characters.
- **Keep cover letters concise**, research-aligned, and professional (aim for 250–350 words).
- **Respect country formatting rules** injected by `utils/country_formatting.py`.

---

## Agent-Specific Behaviors

### Resume Parser Agent (`agents/resume_parser_agent.py`)

- **Priority:** extraction quality over speed. Use PyMuPDF first; fall back to Tesseract OCR only when the text layer is empty.
- **Section detection:** match lines against keyword hint lists (e.g. `["education", "university", "bachelor"]`). Take at most 6 lines per section.
- **Skills detection:** match against a fixed `SKILL_HINTS` vocabulary; return sorted list of confirmed matches only — do not infer unlisted skills.
- **Name heuristic:** first non-empty line of the extracted text.

### Job Description Parser Agent (`agents/job_parser_agent.py`)

- **Keyword extraction:** tokenise with `\b[a-zA-Z][a-zA-Z+.#-]{2,}\b`; deduplicate; cap at 40 entries, sorted alphabetically.
- **Required skills:** lines containing "required", "must", "qualification", or "eligibility"; cap at 10.
- **Technologies:** restrict to the known set `{python, pytorch, tensorflow, docker, postgresql, fastapi, react, next, redis}`.
- **Research domains:** restrict to `{nlp, vision, robotics, ml, ai, llm}`.

### ATS Resume Generator Agent (`agents/ats_resume_generator_agent.py`)

- **System prompt** includes the country formatting rule from `get_country_rule(country)`.
- **Required sections** in output: Summary, Skills, Education, Projects, Experience, Certifications, Research Interests.
- **No fabrication constraint** is explicit in the system prompt; the LLM must not invent content.
- Input: `ResumeProfile` JSON + `JobDescriptionData` JSON serialised via `model_dump_json()`.

### Cover Letter Generator Agent (`agents/cover_letter_generator_agent.py`)

- **Focus areas:** research alignment, technical strengths, motivation, and academic interests.
- **Country context** is included in the user prompt.
- Should mention specific technologies from `JobDescriptionData.technologies` and domain terms from `research_domains`.
- Avoid generic filler phrases; every paragraph must connect to the candidate's actual profile.

### Verification Agent (`agents/verification_agent.py`)

- **Keyword coverage** is computed against the first 30 keywords of the job description only (to avoid noise from long keyword lists).
- **ATS score** floor is 55.0 — even minimal keyword coverage is partially rewarded.
- **Grammar score** is a word-count proxy (90 if resume > 100 words and cover letter > 80 words, else 75); it does not perform linguistic grammar analysis.
- **Hallucination risk** is 10.0 by default; raises to 50.0 only if the literal string "lorem" appears (placeholder detection).
- **Issues list** is surfaced in the API response; use it to diagnose low-scoring outputs.
- **Score threshold for retry:** 80.0. This value is used by both `RouterAgent` and `FeedbackLoopAgent`.

### Feedback Loop Agent (`agents/feedback_loop_agent.py`)

- Calls `ATSResumeGeneratorAgent.generate` and `CoverLetterGeneratorAgent.generate` fresh on each retry (same inputs; the LLM sampling introduces variation).
- `max_retries` defaults to 2; configurable at call site.
- Returns the **last** generated pair and verification result when retries are exhausted, even if score < 80.

### Router Agent (`agents/router_agent.py`)

- Maintains a **compiled LangGraph `StateGraph`** with three nodes: `generate`, `verify`, `improve`.
- The conditional edge from `verify` calls `_needs_improvement`: returns `"improve"` if `score < 80` and `retries < max_retries`, else `"end"`.
- `max_retries` defaults to 2 (can be overridden at `RouterAgent(max_retries=N)` construction time).
- The `improve` node re-runs generation and increments `state["retries"]`; it then returns to `verify`.
- **State type** is `WorkflowState` (TypedDict): `profile`, `job`, `country`, `generated_resume`, `generated_cover_letter`, `verification`, `retries`.
