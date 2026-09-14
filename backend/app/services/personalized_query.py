from app.schemas.search import JobSearchIntent
from app.schemas.personalized_query import (
    PersonalizedQuery,
    PersonalizedQueryPlan,
)


def normalize_location(location: str | None) -> str | None:
    if not location:
        return None

    location_map = {
        "bangalore": "Bangalore",
        "bengaluru": "Bangalore",
        "hyderabad": "Hyderabad",
        "pune": "Pune",
        "mumbai": "Mumbai",
        "delhi": "Delhi",
        "new delhi": "Delhi",
        "gurgaon": "Gurgaon",
        "gurugram": "Gurgaon",
        "noida": "Noida",
        "chennai": "Chennai",
    }

    return location_map.get(
        location.lower().strip(),
        location.strip().title(),
    )


def create_personalized_queries(
    original_query: str,
    intent: JobSearchIntent,
    profile: dict,
) -> PersonalizedQueryPlan:

    location = normalize_location(
        intent.location
    )

    roles = profile.get(
        "preferred_roles",
        []
    )

    skills = profile.get(
        "skills",
        []
    )

    experience_level = profile.get(
        "experience_level"
    )

    queries: list[PersonalizedQuery] = []

    # --------------------------------------------------
    # 1. Direct user query
    # --------------------------------------------------

    direct_query = original_query.strip()

    if location:
        queries.append(
            PersonalizedQuery(
                query=direct_query,
                location=location,
                role=intent.job_title,
                priority=1,
                reason="Direct user search",
            )
        )

    else:
        queries.append(
            PersonalizedQuery(
                query=direct_query,
                role=intent.job_title,
                priority=1,
                reason="Direct user search",
            )
        )

    # --------------------------------------------------
    # 2. Role-based queries
    # --------------------------------------------------

    max_roles = 6

    for index, role in enumerate(
        roles[:max_roles],
        start=2,
    ):

        query = role

        if experience_level:
            query = f"{experience_level} {query}"

        if location:
            query = f"{query} {location}"

        queries.append(
            PersonalizedQuery(
                query=query,
                location=location,
                role=role,
                priority=index,
                reason="Resume-based role",
            )
        )

    # --------------------------------------------------
    # 3. Skill-based query
    # --------------------------------------------------

    if skills:

        important_skills = skills[:5]

        skill_query = " ".join(
            important_skills
        )

        if location:
            skill_query = (
                f"{skill_query} jobs {location}"
            )
        else:
            skill_query = (
                f"{skill_query} jobs"
            )

        queries.append(
            PersonalizedQuery(
                query=skill_query,
                location=location,
                priority=8,
                reason="Resume skill combination",
            )
        )

    # --------------------------------------------------
    # 4. Junior / Entry-level variation
    # --------------------------------------------------

    if experience_level in {
        "Entry Level",
        "Junior",
    }:

        selected_roles = roles[:3]

        for index, role in enumerate(
            selected_roles,
            start=9,
        ):

            query = f"Junior {role}"

            if location:
                query = f"{query} {location}"

            queries.append(
                PersonalizedQuery(
                    query=query,
                    location=location,
                    role=role,
                    priority=index,
                    reason="Entry-level resume profile",
                )
            )

    # --------------------------------------------------
    # Remove duplicate queries
    # --------------------------------------------------

    unique_queries = []
    seen = set()

    for item in queries:

        normalized = item.query.lower().strip()

        if normalized in seen:
            continue

        seen.add(normalized)
        unique_queries.append(item)

    return PersonalizedQueryPlan(
        original_query=original_query,
        queries=unique_queries,
    )