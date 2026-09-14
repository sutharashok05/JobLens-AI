from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
        index=True
    )

    resume_id: Mapped[int] = mapped_column(
        ForeignKey("resumes.id"),
        nullable=False,
        index=True
    )

    # Skills
    skills: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False
    )

    core_skills: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False
    )

    supporting_skills: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False
    )

    # Candidate information
    education: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False
    )

    experience: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False
    )

    experience_level: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    projects: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False
    )

    certifications: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False
    )

    # Job-search intelligence
    preferred_roles: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False
    )

    preferred_locations: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False
    )

    preferred_work_modes: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False
    )

    career_keywords: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )