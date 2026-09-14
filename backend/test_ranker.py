import asyncio

from app.db.database import AsyncSessionLocal
from app.services.profile_service import (
    get_active_candidate_profile,
)

from app.providers.google.provider import (
    GoogleProvider,
)

from app.services.job_matcher import (
    match_jobs,
)

from app.services.job_ranker import (
    rank_jobs,
)


async def main():

    async with AsyncSessionLocal() as db:

        profile = await get_active_candidate_profile(db)

        if not profile:
            print(
                "Candidate profile not found"
            )
            return

        profile_data = {
            "skills": profile.skills,
            "preferred_roles": profile.preferred_roles,
            "preferred_locations": (
                profile.preferred_locations
            ),
        }

        # ---------------------------------------------
        # Search
        # ---------------------------------------------

        provider = GoogleProvider()

        jobs = await provider.search(
            "AI Engineer",
            "Bangalore",
        )

        print(
            "Jobs found:",
            len(jobs),
        )

        # ---------------------------------------------
        # Matching
        # ---------------------------------------------

        matched_jobs = match_jobs(
            jobs,
            profile_data,
        )

        # ---------------------------------------------
        # Ranking
        # ---------------------------------------------

        ranked_jobs = rank_jobs(
            matched_jobs
        )

        print(
            "\n========== RANKED JOBS ==========\n"
        )

        for index, job in enumerate(
            ranked_jobs,
            start=1,
        ):

            ranking = (
                job.source_metadata
                .get("ranking", {})
            )

            matching = (
                job.source_metadata
                .get("matching", {})
            )

            print(
                f"#{index} {job.title}"
            )

            print(
                "COMPANY:",
                job.company,
            )

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
                "FINAL RANK:",
                ranking.get(
                    "ranking_score"
                ),
            )

            print(
                "VERIFIED:",
                ranking.get(
                    "verification_score"
                ),
            )

            print(
                "FRESHNESS:",
                ranking.get(
                    "freshness_score"
                ),
            )

            print(
                "JOB URL:",
                job.job_url,
            )

            print(
                "-" * 60
            )


if __name__ == "__main__":
    asyncio.run(main())