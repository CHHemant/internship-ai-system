from app.agents.job_parser_agent import JobDescriptionParserAgent
from app.agents.resume_parser_agent import ResumeParserAgent
from app.models.schemas import ResumeProfile


def test_resume_parser_extracts_structured_fields() -> None:
    content = b"""
    Jane Doe
    jane.doe@example.com
    Skills: Python, FastAPI, Docker
    Projects: NLP Internship Matching System
    Education: B.Tech CSE
    Research Interests: NLP, LLMs
    """
    parser = ResumeParserAgent()

    profile = parser.parse(content, "resume.txt")

    assert profile.name == "Jane Doe"
    assert profile.email == "jane.doe@example.com"
    assert "python" in profile.skills


def test_job_parser_extracts_keywords_and_sections() -> None:
    jd = """
    Required: Python, FastAPI, Redis
    Responsibilities: Build research internship recommendation engine.
    Eligibility: Final year student.
    """
    parser = JobDescriptionParserAgent()
    data = parser.parse(jd)

    assert "python" in data.keywords
    assert len(data.required_skills) > 0
    assert len(data.responsibilities) > 0


def test_profile_model_has_defaults() -> None:
    profile = ResumeProfile()
    assert profile.skills == []
