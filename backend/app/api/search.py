from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.search import JobSearchRequest
from app.services.search_intent import parse_search_intent
from app.services.search_planner import create_search_plan
from app.services.profile_service import get_active_candidate_profile
from app.services.personalized_query import create_personalized_queries
from app.services.job_search import search_all_sources


router = APIRouter(
    prefix="/api/search",
    tags=["Search"],
)


# =========================================================
# 1. SEARCH INTENT
# =========================================================

@router.post("/intent")
async def search_intent(
    request: JobSearchRequest,
):
    intent = parse_search_intent(
        request.query
    )

    return {
        "query": request.query,
        "intent": intent.model_dump(),
    }


# =========================================================
# 2. SEARCH PLAN
# =========================================================

@router.post("/plan")
async def search_plan(
    request: JobSearchRequest,
):
    intent = parse_search_intent(
        request.query
    )

    plan = create_search_plan(
        request.query,
        intent,
    )

    return plan.model_dump()


# =========================================================
# 3. PERSONALIZED SEARCH PLAN
# =========================================================

@router.post("/personalized-plan")
async def personalized_search_plan(
    request: JobSearchRequest,
    db: AsyncSession = Depends(get_db),
):
    try:

        # -------------------------------------------------
        # 1. Parse user search intent
        # -------------------------------------------------

        intent = parse_search_intent(
            request.query
        )

        # -------------------------------------------------
        # 2. Get active candidate profile
        # -------------------------------------------------

        profile = await get_active_candidate_profile(
            db
        )

        if profile is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    "No candidate profile found. "
                    "Please upload a resume first."
                ),
            )

        # -------------------------------------------------
        # 3. Convert ORM profile -> dictionary
        #
        # IMPORTANT:
        # Only fields that currently exist in
        # CandidateProfile are used.
        # -------------------------------------------------

        profile_data = {
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
        }

        # -------------------------------------------------
        # 4. Generate personalized search queries
        # -------------------------------------------------

        personalized_plan = create_personalized_queries(
            original_query=request.query,
            intent=intent,
            profile=profile_data,
        )

        # -------------------------------------------------
        # 5. Response
        # -------------------------------------------------

        return {
            "query": request.query,

            "intent": (
                intent.model_dump()
            ),

            "profile": profile_data,

            "personalized_plan": (
                personalized_plan.model_dump()
            ),
        }

    except HTTPException:
        raise

    except Exception as e:
        print(
            "========== PERSONALIZED PLAN ERROR =========="
        )
        print(
            "ERROR TYPE:",
            type(e).__name__,
        )
        print(
            "ERROR:",
            str(e),
        )

        raise HTTPException(
            status_code=500,
            detail=f"{type(e).__name__}: {str(e)}",
        )


# =========================================================
# 4. JOB SEARCH
# =========================================================

@router.post("/jobs")
async def search_jobs(
    request: JobSearchRequest,
    db: AsyncSession = Depends(get_db),
):
    try:

        # -------------------------------------------------
        # 1. Get active candidate profile
        # -------------------------------------------------

        profile = await get_active_candidate_profile(
            db
        )

        if profile is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    "Candidate profile not found. "
                    "Upload a resume first."
                ),
            )

        # -------------------------------------------------
        # 2. Parse search intent
        # -------------------------------------------------

        intent = parse_search_intent(
            request.query
        )

        # -------------------------------------------------
        # 3. Convert ORM profile -> dictionary
        #
        # Only current CandidateProfile fields.
        # -------------------------------------------------

        profile_data = {
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

            # Location comes from user's search query,
            # NOT from CandidateProfile.
            "requested_location": (
                intent.location
            ),
        }

        # -------------------------------------------------
        # 4. Create personalized search queries
        # -------------------------------------------------

        personalized_queries = (
            create_personalized_queries(
                original_query=request.query,
                intent=intent,
                profile=profile_data,
            )
        )

        # -------------------------------------------------
        # 5. Search jobs from configured providers
        # -------------------------------------------------

        jobs = await search_all_sources(
            search_plan=personalized_queries,
            profile_data=profile_data,
        )

        # -------------------------------------------------
        # 6. Return results
        # -------------------------------------------------

        return {
            "query": request.query,

            "total_jobs": len(jobs),

            "jobs": [
                job.model_dump()
                for job in jobs
            ],
        }

    except HTTPException:
        raise

    except Exception as e:
        print(
            "========== JOB SEARCH ERROR =========="
        )
        print(
            "ERROR TYPE:",
            type(e).__name__,
        )
        print(
            "ERROR:",
            str(e),
        )

        raise HTTPException(
            status_code=500,
            detail=f"{type(e).__name__}: {str(e)}",
        )