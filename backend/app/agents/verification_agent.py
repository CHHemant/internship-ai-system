from app.models.schemas import JobDescriptionData, VerificationResult


class VerificationAgent:
    def verify(self, resume: str, cover_letter: str, job: JobDescriptionData) -> VerificationResult:
        lower_resume = resume.lower()
        lower_cover = cover_letter.lower()
        job_keywords = {k.lower() for k in job.keywords[:30]}

        matched = sum(1 for keyword in job_keywords if keyword in lower_resume or keyword in lower_cover)
        keyword_coverage = (matched / len(job_keywords) * 100) if job_keywords else 0.0
        ats_score = min(100.0, 55.0 + keyword_coverage * 0.45)
        grammar_score = 90.0 if len(resume.split()) > 100 and len(cover_letter.split()) > 80 else 75.0
        hallucination_risk = 10.0 if "lorem" not in lower_resume else 50.0
        relevance_score = min(100.0, (keyword_coverage + ats_score) / 2)

        score = round((ats_score + keyword_coverage + grammar_score + (100 - hallucination_risk) + relevance_score) / 5, 2)
        issues = []
        if keyword_coverage < 60:
            issues.append("Low keyword coverage")
        if grammar_score < 80:
            issues.append("Output too short for strong academic positioning")
        if hallucination_risk > 20:
            issues.append("Possible hallucination markers detected")

        return VerificationResult(
            score=score,
            ats_score=round(ats_score, 2),
            keyword_coverage=round(keyword_coverage, 2),
            grammar_score=round(grammar_score, 2),
            hallucination_risk=round(hallucination_risk, 2),
            relevance_score=round(relevance_score, 2),
            issues=issues,
        )
