from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    # ============================================================
    # Primary Key
    # ============================================================

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    # ============================================================
    # Relationships
    # ============================================================

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    resume_id: Mapped[int] = mapped_column(
        ForeignKey("resumes.id"),
        nullable=False,
        index=True,
    )

    # ============================================================
    # Skills
    # ============================================================

    skills: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )

    core_skills: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )

    supporting_skills: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )

    # ============================================================
    # Experience Intelligence
    # ============================================================

    experience_level: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ============================================================
    # Resume Intelligence
    # ============================================================

    projects: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )

    certifications: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )

    # ============================================================
    # Job Search Intelligence
    # ============================================================

    preferred_roles: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )

    career_keywords: Mapped[list] = mapped_column(
        JSON,
        default=list,
        nullable=False,
    )

    # ============================================================
    # Timestamp
    # ============================================================

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )