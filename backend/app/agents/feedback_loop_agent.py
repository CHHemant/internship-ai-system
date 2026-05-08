from app.agents.ats_resume_generator_agent import ATSResumeGeneratorAgent
from app.agents.cover_letter_generator_agent import CoverLetterGeneratorAgent
from app.agents.verification_agent import VerificationAgent
from app.models.schemas import JobDescriptionData, ResumeProfile, VerificationResult


class FeedbackLoopAgent:
    def __init__(self) -> None:
        self._resume_agent = ATSResumeGeneratorAgent()
        self._cover_agent = CoverLetterGeneratorAgent()
        self._verification_agent = VerificationAgent()

    def improve(
        self,
        profile: ResumeProfile,
        job: JobDescriptionData,
        country: str,
        max_retries: int = 2,
    ) -> tuple[str, str, VerificationResult]:
        resume = self._resume_agent.generate(profile, job, country)
        cover = self._cover_agent.generate(profile, job, country)
        verification = self._verification_agent.verify(resume, cover, job)

        retries = 0
        while verification.score < 80 and retries < max_retries:
            resume = self._resume_agent.generate(profile, job, country)
            cover = self._cover_agent.generate(profile, job, country)
            verification = self._verification_agent.verify(resume, cover, job)
            retries += 1

        return resume, cover, verification
