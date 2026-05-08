# Workflow

1. **Resume Upload**
   - `/api/resume/upload`
   - Resume Parser extracts structured profile JSON.
2. **Job Parsing**
   - `/api/job/parse`
   - JD Parser extracts keywords, skills, responsibilities, eligibility.
3. **Generation**
   - `/api/applications/run`
   - Router Agent triggers ATS Resume + Cover Letter generation.
4. **Verification**
   - Verification Agent scores ATS, coverage, grammar, hallucination risk, relevance.
5. **Feedback Loop**
   - If score < 80, workflow retries generation automatically.
6. **Persistence + History**
   - Result stored in PostgreSQL and available at `/api/applications/history`.
