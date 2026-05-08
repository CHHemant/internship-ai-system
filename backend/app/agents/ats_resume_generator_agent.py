from app.models.schemas import JobDescriptionData, ResumeProfile
from app.services.openai_service import OpenAIService
from app.utils.country_formatting import get_country_rule


class ATSResumeGeneratorAgent:
    def __init__(self) -> None:
        self._llm = OpenAIService()

    def generate(self, profile: ResumeProfile, job: JobDescriptionData, country: str) -> str:
        system_prompt = (
            "You generate ATS-safe internship resumes. Do not invent skills/experience. "
            f"Formatting rule: {get_country_rule(country)}"
        )
        user_prompt = (
            f"Candidate profile: {profile.model_dump_json()}\n"
            f"Job requirements: {job.model_dump_json()}\n"
            "Return concise plain-text resume with sections: Summary, Skills, Education, Projects, Experience, Certifications, Research Interests."
        )
        return self._llm.complete(system_prompt, user_prompt)
