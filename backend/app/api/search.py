from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.search import JobSearchRequest
from app.services.search_intent import parse_search_intent
from app.services.search_planner import create_search_plan
from app.services.profile_service import (
    get_active_candidate_profile,
)
from app.services.personalized_query import (
    create_personalized_queries,
)
from app.schemas.job import JobSearchFilters
from app.services.job_search import search_all_sources

router = APIRouter(
    prefix="/api/search",
    tags=["Search"],
)


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


@router.post("/personalized-plan")
async def personalized_search_plan(
    request: JobSearchRequest,
    db: AsyncSession = Depends(get_db),
):

    # ---------------------------------------------
    # 1. Parse user search intent
    # ---------------------------------------------

    intent = parse_search_intent(
        request.query
    )

    # ---------------------------------------------
    # 2. Get stored candidate profile
    # ---------------------------------------------

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

    # ---------------------------------------------
    # 3. Convert DB profile to dictionary
    # ---------------------------------------------

    profile_data = {
        "skills": profile.skills or [],
        "core_skills": profile.core_skills or [],
        "supporting_skills": (
            profile.supporting_skills or []
        ),
        "experience": profile.experience or [],
        "experience_level": (
            profile.experience_level
        ),
        "preferred_roles": (
            profile.preferred_roles or []
        ),
        "preferred_locations": (
            profile.preferred_locations or []
        ),
        "preferred_work_modes": (
            profile.preferred_work_modes or []
        ),
        "career_keywords": (
            profile.career_keywords or []
        ),
        "education": profile.education or [],
        "projects": profile.projects or [],
        "certifications": (
            profile.certifications or []
        ),
    }

    # ---------------------------------------------
    # 4. Generate personalized queries
    # ---------------------------------------------

    personalized_plan = create_personalized_queries(
        original_query=request.query,
        intent=intent,
        profile=profile_data,
    )

    return {
        "query": request.query,
        "intent": intent.model_dump(),
        "profile": profile_data,
        "personalized_plan": (
            personalized_plan.model_dump()
        ),
    }
    
@router.post("/jobs")
async def search_jobs(
    request: JobSearchRequest,
    db: AsyncSession = Depends(get_db),
):
    # -----------------------------------------------------
    # 1. Get candidate profile
    # -----------------------------------------------------

    profile = await get_active_candidate_profile(db)

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Candidate profile not found. Upload a resume first.",
        )

    # -----------------------------------------------------
    # 2. Parse search intent
    # -----------------------------------------------------

    intent = parse_search_intent(
        request.query
    )

    # -----------------------------------------------------
    # 3. Convert ORM profile -> dictionary
    # -----------------------------------------------------

    profile_data = {
    "skills": profile.skills or [],
    "core_skills": profile.core_skills or [],
    "supporting_skills": profile.supporting_skills or [],

    "preferred_roles": profile.preferred_roles or [],

    "preferred_locations": (
        profile.preferred_locations or []
    ),

    "requested_location": intent.location,

    "preferred_work_modes": (
        profile.preferred_work_modes or []
    ),

    "experience_level": profile.experience_level,

    "career_keywords": (
        profile.career_keywords or []
    ),

    "projects": profile.projects or [],

    "education": profile.education or [],

    "experience": profile.experience or [],

    "certifications": (
        profile.certifications or []
    ),

    "summary": profile.summary,
}

    # -----------------------------------------------------
    # 4. Personalized queries
    # -----------------------------------------------------

    personalized_queries = (
        create_personalized_queries(
            original_query=request.query,
            intent=intent,
            profile=profile_data,
        )
    )

    # -----------------------------------------------------
    # 5. Multi-source search + matching + ranking
    # -----------------------------------------------------

    jobs = await search_all_sources(
        search_plan=personalized_queries,
        profile_data=profile_data,
    )

    # -----------------------------------------------------
    # 6. Response
    # -----------------------------------------------------

    return {
        "query": request.query,
        "total_jobs": len(jobs),
        "jobs": [
            job.model_dump()
            for job in jobs
        ],
    }