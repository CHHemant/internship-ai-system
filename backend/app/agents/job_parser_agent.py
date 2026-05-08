import re

from app.models.schemas import JobDescriptionData
from app.utils.text import normalize_whitespace, split_bullets


class JobDescriptionParserAgent:
    def parse(self, description: str) -> JobDescriptionData:
        text = normalize_whitespace(description)
        lines = split_bullets(description)
        lower = text.lower()

        keyword_candidates = re.findall(r"\b[a-zA-Z][a-zA-Z+.#-]{2,}\b", lower)
        keywords = sorted(set(keyword_candidates))[:40]

        required = [l for l in lines if any(k in l.lower() for k in ["required", "must", "qualification", "eligibility"])]
        responsibilities = [l for l in lines if any(k in l.lower() for k in ["responsibil", "work", "develop", "research"])][:10]
        technologies = [k for k in keywords if k in {"python", "pytorch", "tensorflow", "docker", "postgresql", "fastapi", "react", "next", "redis"}]
        research_domains = [k for k in keywords if k in {"nlp", "vision", "robotics", "ml", "ai", "llm"}]

        return JobDescriptionData(
            keywords=keywords,
            required_skills=required[:10],
            technologies=technologies,
            research_domains=research_domains,
            responsibilities=responsibilities,
            eligibility_requirements=required[:10],
            raw_text=text,
        )
