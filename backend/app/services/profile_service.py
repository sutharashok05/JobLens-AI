from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.candidate_profile import CandidateProfile


async def get_active_candidate_profile(
    db: AsyncSession,
) -> CandidateProfile | None:

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

    return result.scalar_one_or_none()