from app.models.schemas import JobDescriptionData, ResumeProfile


def score_application_fit(profile: ResumeProfile, job: JobDescriptionData) -> float:
    profile_tokens = {t.lower() for t in profile.skills + profile.research_interests}
    job_tokens = {t.lower() for t in job.required_skills + job.technologies + job.research_domains}
    if not job_tokens:
        return 0.0
    overlap = len(profile_tokens & job_tokens)
    return round((overlap / len(job_tokens)) * 100, 2)
