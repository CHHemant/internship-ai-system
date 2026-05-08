from app.models.schemas import JobDescriptionData, ResumeProfile
from app.services.openai_service import OpenAIService


class CoverLetterGeneratorAgent:
    def __init__(self) -> None:
        self._llm = OpenAIService()

    def generate(self, profile: ResumeProfile, job: JobDescriptionData, country: str) -> str:
        system_prompt = (
            "You write concise, professional, academic cover letters for research internships. "
            "Mention research alignment, technical strengths, motivation, and academic interests."
        )
        user_prompt = (
            f"Country: {country}\n"
            f"Candidate profile: {profile.model_dump_json()}\n"
            f"Job details: {job.model_dump_json()}"
        )
        return self._llm.complete(system_prompt, user_prompt)
