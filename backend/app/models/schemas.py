from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ResumeProfile(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    skills: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    research_interests: list[str] = Field(default_factory=list)
    raw_text: str = ""


class JobDescriptionData(BaseModel):
    keywords: list[str] = Field(default_factory=list)
    required_skills: list[str] = Field(default_factory=list)
    technologies: list[str] = Field(default_factory=list)
    research_domains: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
    eligibility_requirements: list[str] = Field(default_factory=list)
    raw_text: str


class VerificationResult(BaseModel):
    score: float
    ats_score: float
    keyword_coverage: float
    grammar_score: float
    hallucination_risk: float
    relevance_score: float
    issues: list[str] = Field(default_factory=list)


class CandidateCreateResponse(BaseModel):
    candidate_id: int
    profile: ResumeProfile


class ParseJobRequest(BaseModel):
    job_description: str


class GenerateArtifactsRequest(BaseModel):
    profile: ResumeProfile | None = None
    candidate_id: int | None = None
    job_description: str
    country: str = "global"


class RunApplicationResponse(BaseModel):
    application_id: int
    resume: str
    cover_letter: str
    verification: VerificationResult


class ApplicationHistoryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    candidate_id: int | None
    country: str
    verification_score: float
    created_at: datetime


class VerificationResponse(BaseModel):
    application_id: int
    verification: VerificationResult


class RecommendationRequest(BaseModel):
    profile: ResumeProfile
    internships: list[dict[str, Any]]


class RecommendationItem(BaseModel):
    internship: dict[str, Any]
    score: float


class RecommendationResponse(BaseModel):
    ranked_internships: list[RecommendationItem]
    suggested_professors_or_labs: list[str]
