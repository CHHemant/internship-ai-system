from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    profile_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    candidate_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    country: Mapped[str] = mapped_column(String(64), default="global")
    job_description: Mapped[str] = mapped_column(Text, nullable=False)
    parsed_job_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    generated_resume: Mapped[str] = mapped_column(Text, nullable=False)
    generated_cover_letter: Mapped[str] = mapped_column(Text, nullable=False)
    verification_score: Mapped[float] = mapped_column(Float, nullable=False)
    verification_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
