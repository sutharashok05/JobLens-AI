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
        .join(User, CandidateProfile.user_id == User.id)
        .where(User.email == "demo@joblens.ai")
    )

    profile = result.scalar_one_or_none()

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="No candidate profile found. Please upload a resume first.",
        )

    return {
        "profile_id": profile.id,
        "user_id": profile.user_id,
        "resume_id": profile.resume_id,
        "skills": profile.skills,
        "education": profile.education,
        "experience": profile.experience,
        "projects": profile.projects,
        "certifications": profile.certifications,
        "preferred_roles": profile.preferred_roles,
        "preferred_locations": profile.preferred_locations,
        "summary": profile.summary,
    }