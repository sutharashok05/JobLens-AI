import asyncio

from app.db.database import AsyncSessionLocal
from app.services.profile_service import (
    get_active_candidate_profile,
)
from app.providers.google.provider import (
    GoogleProvider,
)
from app.services.job_matcher import match_jobs


async def main():

    async with AsyncSessionLocal() as db:

        profile = await get_active_candidate_profile(
            db
        )

        if not profile:
            print("Candidate profile not found")
            return

        profile_data = {
            "skills": profile.skills,
            "preferred_roles": profile.preferred_roles,
            "preferred_locations": profile.preferred_locations,
        }

        provider = GoogleProvider()

        jobs = await provider.search(
            "AI Engineer",
            "Bangalore",
        )

        matched = match_jobs(
            jobs,
            profile_data,
        )

        print(
            "Jobs:",
            len(matched),
        )

        for job in matched:

            matching = (
                job.source_metadata
                .get("matching", {})
            )

            print()
            print("JOB:", job.title)
            print("COMPANY:", job.company)
            print(
                "MATCH:",
                matching.get(
                    "match_score"
                ),
            )
            print(
                "SKILL MATCH:",
                matching.get(
                    "skill_match_score"
                ),
            )
            print(
                "MATCHED:",
                matching.get(
                    "matched_skills"
                ),
            )
            print(
                "MISSING:",
                matching.get(
                    "missing_skills"
                ),
            )


if __name__ == "__main__":
    asyncio.run(main())