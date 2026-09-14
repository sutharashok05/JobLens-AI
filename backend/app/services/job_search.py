import asyncio

from app.providers import provider_registry
from app.schemas.job import JobResult, JobSearchFilters
from app.schemas.personalized_query import PersonalizedQueryPlan
from app.services.job_normalizer import normalize_jobs
from app.services.job_verifier import verify_jobs
from app.services.job_deduplicator import deduplicate_jobs
from app.services.job_matcher import match_jobs
from app.services.job_ranker import rank_jobs


async def search_provider(
    provider_name: str,
    query: str,
    location: str | None = None,
    filters: JobSearchFilters | None = None,
) -> list[JobResult]:

    provider = provider_registry.get(provider_name)

    if not provider:
        return []

    try:
        return await provider.search(
            query=query,
            location=location,
            filters=filters,
        )

    except Exception as e:
        print(
            f"Provider {provider_name} failed: {e}"
        )
        return []


async def search_all_sources(
    search_plan: PersonalizedQueryPlan,
    profile_data: dict | None = None,
    filters: JobSearchFilters | None = None,
) -> list[JobResult]:

    providers = [
        "adzuna",
        "google",
        #"ats",
        #"company_careers",
    ]

    tasks = []

    # -----------------------------------------------------
    # Search first 3 personalized queries
    # across all providers in parallel
    # -----------------------------------------------------

    for personalized_query in search_plan.queries[:3]:

        for provider_name in providers:

            tasks.append(
                search_provider(
                    provider_name=provider_name,
                    query=personalized_query.query,
                    location=personalized_query.location,
                    filters=filters,
                )
            )

    if not tasks:
        return []

    # -----------------------------------------------------
    # Parallel provider search
    # -----------------------------------------------------

    results = await asyncio.gather(
        *tasks,
        return_exceptions=False,
    )

    all_jobs: list[JobResult] = []

    for provider_jobs in results:
        all_jobs.extend(provider_jobs)

    print(
        f"Total raw jobs: {len(all_jobs)}"
    )

    # -----------------------------------------------------
    # NORMALIZATION
    # -----------------------------------------------------

    normalized_jobs = normalize_jobs(
        all_jobs
    )

    print(
        f"After normalization: "
        f"{len(normalized_jobs)}"
    )

    # -----------------------------------------------------
    # VERIFICATION
    # -----------------------------------------------------

    verified_jobs = await verify_jobs(
        normalized_jobs
    )

    print(
        f"After verification: "
        f"{len(verified_jobs)}"
    )

    # -----------------------------------------------------
    # DEDUPLICATION
    # -----------------------------------------------------

    unique_jobs = deduplicate_jobs(
        verified_jobs
    )

    print(
        f"After deduplication: "
        f"{len(unique_jobs)}"
    )

    # -----------------------------------------------------
    # RESUME MATCHING
    # -----------------------------------------------------

    if profile_data:

        matched_jobs = match_jobs(
            unique_jobs,
            profile_data,
        )

    else:

        matched_jobs = unique_jobs

    print(
        f"After matching: "
        f"{len(matched_jobs)}"
    )

    # -----------------------------------------------------
    # INTELLIGENT RANKING
    # -----------------------------------------------------

    ranked_jobs = rank_jobs(
        matched_jobs
    )

    print(
        f"Final ranked jobs: "
        f"{len(ranked_jobs)}"
    )

    return ranked_jobs