from app.schemas.search import JobSearchIntent
from app.schemas.search_plan import SearchPlan, SearchQuery


def build_search_queries(
    intent: JobSearchIntent,
) -> list[SearchQuery]:

    queries = []

    job_title = intent.job_title or "software developer"
    location = intent.location

    experience = intent.experience_level

    # Query 1 — direct search
    direct_query = job_title

    if experience:
        direct_query += f" {experience}"

    queries.append(
        SearchQuery(
            query=direct_query,
            location=location,
            priority=1,
        )
    )

    # Query 2 — Engineer variation
    if "engineer" not in job_title.lower():
        engineer_query = f"{job_title} engineer"

        if experience:
            engineer_query += f" {experience}"

        queries.append(
            SearchQuery(
                query=engineer_query,
                location=location,
                priority=2,
            )
        )

    # Query 3 — Developer variation
    if "developer" not in job_title.lower():
        developer_query = f"{job_title} developer"

        if experience:
            developer_query += f" {experience}"

        queries.append(
            SearchQuery(
                query=developer_query,
                location=location,
                priority=3,
            )
        )

    # Query 4 — junior variation
    if experience in ("fresher", "entry-level", "junior"):
        queries.append(
            SearchQuery(
                query=f"junior {job_title}",
                location=location,
                priority=4,
            )
        )

    return queries


def create_search_plan(
    original_query: str,
    intent: JobSearchIntent,
) -> SearchPlan:

    queries = build_search_queries(intent)

    return SearchPlan(
        original_query=original_query,
        job_title=intent.job_title,
        location=intent.location,
        experience_level=intent.experience_level,
        work_mode=intent.work_mode,
        job_type=intent.job_type,
        queries=queries,
    )