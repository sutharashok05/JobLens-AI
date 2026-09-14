from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.user import User
from app.models.candidate_profile import CandidateProfile


router = APIRouter(
    prefix="/api/profile",
    tags=["Profile"],
)


@router.get("")
async def get_candidate_profile(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(CandidateProfile)
        .join(
            User,
            CandidateProfile.user_id == User.id
        )
        .where(
            User.email == "demo@joblens.ai"
        )
    )

    profile = result.scalar_one_or_none()

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "No candidate profile found. "
                "Please upload a resume first."
            ),
        )

    return {
        "profile_id": profile.id,
        "user_id": profile.user_id,
        "resume_id": profile.resume_id,

        "skills": profile.skills or [],

        "core_skills": (
            profile.core_skills or []
        ),

        "supporting_skills": (
            profile.supporting_skills or []
        ),

        "experience_level": (
            profile.experience_level
        ),

        "projects": (
            profile.projects or []
        ),

        "certifications": (
            profile.certifications or []
        ),

        "preferred_roles": (
            profile.preferred_roles or []
        ),

        "career_keywords": (
            profile.career_keywords or []
        ),

        "updated_at": (
            profile.updated_at
        ),
    }