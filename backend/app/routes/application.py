from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.agents.job_parser_agent import JobDescriptionParserAgent
from app.agents.resume_parser_agent import ResumeParserAgent
from app.agents.router_agent import RouterAgent
from app.database.models import Application, CandidateProfile
from app.database.session import get_db
from app.models.schemas import (
    ApplicationHistoryItem,
    CandidateCreateResponse,
    GenerateArtifactsRequest,
    ParseJobRequest,
    ResumeProfile,
    RecommendationRequest,
    RecommendationResponse,
    RunApplicationResponse,
    VerificationResponse,
)
from app.services.memory import AgentMemoryStore
from app.services.recommendation import InternshipRecommendationService

router = APIRouter(prefix="/api", tags=["applications"])

resume_parser = ResumeParserAgent()
job_parser = JobDescriptionParserAgent()
workflow_router = RouterAgent()
memory_store = AgentMemoryStore()


@router.post("/resume/upload", response_model=CandidateCreateResponse)
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)) -> CandidateCreateResponse:
    content = await file.read()
    profile = resume_parser.parse(content, file.filename or "resume.pdf")

    candidate = CandidateProfile(name=profile.name, email=profile.email, profile_json=profile.model_dump())
    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    memory_store.save(f"candidate:{candidate.id}:profile", profile.model_dump())
    return CandidateCreateResponse(candidate_id=candidate.id, profile=profile)


@router.post("/job/parse")
def parse_job(request: ParseJobRequest):
    return job_parser.parse(request.job_description)


def _resolve_profile(request: GenerateArtifactsRequest, db: Session):
    if request.profile:
        return request.profile
    if request.candidate_id is not None:
        candidate = db.get(CandidateProfile, request.candidate_id)
        if candidate is None:
            raise HTTPException(status_code=404, detail="Candidate profile not found")
        return candidate.profile_json
    raise HTTPException(status_code=400, detail="Provide either profile or candidate_id")


@router.post("/generate/resume")
def generate_resume(request: GenerateArtifactsRequest, db: Session = Depends(get_db)):
    profile_data = _resolve_profile(request, db)
    parsed_profile = ResumeProfile.model_validate(profile_data)
    parsed_job = job_parser.parse(request.job_description)
    state = workflow_router.run(parsed_profile, parsed_job, request.country)
    return {"resume": state["generated_resume"], "verification": state["verification"]}


@router.post("/generate/cover-letter")
def generate_cover_letter(request: GenerateArtifactsRequest, db: Session = Depends(get_db)):
    profile_data = _resolve_profile(request, db)
    parsed_profile = ResumeProfile.model_validate(profile_data)
    parsed_job = job_parser.parse(request.job_description)
    state = workflow_router.run(parsed_profile, parsed_job, request.country)
    return {"cover_letter": state["generated_cover_letter"], "verification": state["verification"]}


@router.post("/applications/run", response_model=RunApplicationResponse)
def run_application(request: GenerateArtifactsRequest, db: Session = Depends(get_db)) -> RunApplicationResponse:
    profile_data = _resolve_profile(request, db)
    profile = ResumeProfile.model_validate(profile_data)
    parsed_job = job_parser.parse(request.job_description)

    state = workflow_router.run(profile, parsed_job, request.country)
    verification = state["verification"]
    if verification is None:
        raise HTTPException(
            status_code=500,
            detail="Verification result was not produced by the workflow. Retry the request or check router/agent logs.",
        )

    app_record = Application(
        candidate_id=request.candidate_id,
        country=request.country,
        job_description=request.job_description,
        parsed_job_json=parsed_job.model_dump(),
        generated_resume=state["generated_resume"],
        generated_cover_letter=state["generated_cover_letter"],
        verification_score=verification.score,
        verification_json=verification.model_dump(),
    )
    db.add(app_record)
    db.commit()
    db.refresh(app_record)

    memory_store.save(
        f"application:{app_record.id}",
        {
            "candidate_id": app_record.candidate_id,
            "score": app_record.verification_score,
            "country": app_record.country,
        },
    )

    return RunApplicationResponse(
        application_id=app_record.id,
        resume=state["generated_resume"],
        cover_letter=state["generated_cover_letter"],
        verification=verification,
    )


@router.get("/applications/history", response_model=list[ApplicationHistoryItem])
def application_history(db: Session = Depends(get_db)) -> list[ApplicationHistoryItem]:
    rows = db.query(Application).order_by(Application.created_at.desc()).all()
    return [ApplicationHistoryItem.model_validate(row) for row in rows]


@router.get("/applications/{application_id}/verification", response_model=VerificationResponse)
def verification_result(application_id: int, db: Session = Depends(get_db)) -> VerificationResponse:
    app_record = db.get(Application, application_id)
    if app_record is None:
        raise HTTPException(status_code=404, detail="Application not found")

    from app.models.schemas import VerificationResult

    verification = VerificationResult.model_validate(app_record.verification_json)
    return VerificationResponse(application_id=application_id, verification=verification)


@router.post("/recommendations", response_model=RecommendationResponse)
def recommendations(request: RecommendationRequest) -> RecommendationResponse:
    return InternshipRecommendationService.rank(request.profile, request.internships)
