import httpx

from app.core.config import settings
from app.providers.base import JobSearchProvider
from app.schemas.job import JobResult, JobSearchFilters


class GoogleProvider(JobSearchProvider):
    name = "google"
    provider_type = "search_engine"

    BASE_URL = "https://serpapi.com/search.json"

    async def search(
        self,
        query: str,
        location: str | None = None,
        filters: JobSearchFilters | None = None,
    ) -> list[JobResult]:

        params = {
            "engine": "google_jobs",
            "q": query,
            "api_key": settings.SERPAPI_KEY,
        }

        if location:
            params["location"] = location

        try:
            async with httpx.AsyncClient(
                timeout=60.0,
                follow_redirects=True,
            ) as client:

                response = await client.get(
                    self.BASE_URL,
                    params=params,
                )

                response.raise_for_status()

                data = response.json()

        except httpx.HTTPStatusError as e:
            status = e.response.status_code

            try:
                error_body = e.response.json()
            except Exception:
                error_body = e.response.text

            print(
                f"SerpApi Google Jobs HTTP error: "
                f"{status} | {error_body}"
            )

            return []

        except httpx.RequestError as e:
            print(
                f"SerpApi Google Jobs request error: "
                f"{type(e).__name__}: {e}"
            )

            return []

        except Exception as e:
            print(
                f"SerpApi Google Jobs unexpected error: "
                f"{type(e).__name__}: {e}"
            )

            return []

        jobs_data = data.get("jobs_results", [])

        if not isinstance(jobs_data, list):
            print("Google Jobs: jobs_results is not a list")
            return []

        results = []

        for job in jobs_data:

            title = job.get("title")

            if not title:
                continue

            company = job.get("company_name")
            location_value = job.get("location")

            description = job.get("description") or ""

            job_id = job.get("job_id")

            # Google Jobs provides share_link for the job
            job_url = (
                job.get("share_link")
                or job.get("link")
                or job.get("source_link")
            )

            if not job_url:
                continue

            detected = job.get(
                "detected_extensions",
                {},
            )

            if not isinstance(detected, dict):
                detected = {}

            apply_options = job.get(
                "apply_options",
                [],
            )

            if not isinstance(apply_options, list):
                apply_options = []

            apply_url = None

            for option in apply_options:

                if not isinstance(option, dict):
                    continue

                link = option.get("link")

                if link:
                    apply_url = link
                    break

            results.append(
                JobResult(
                    source="google",

                    external_id=job_id,

                    title=title,

                    company=company,

                    location=(
                        location_value
                        or location
                    ),

                    description=description,

                    job_url=job_url,

                    apply_url=apply_url or job_url,

                    posted_at=None,

                    employment_type=detected.get(
                        "schedule_type"
                    ),

                    work_mode=None,

                    salary_min=None,

                    salary_max=None,

                    currency=None,

                    source_metadata={
                        "via": job.get("via"),

                        "posted_at": detected.get(
                            "posted_at"
                        ),

                        "extensions": job.get(
                            "extensions",
                            [],
                        ),

                        "source_link": job.get(
                            "source_link"
                        ),

                        "share_link": job.get(
                            "share_link"
                        ),

                        "apply_options": apply_options,

                        "job_id": job_id,

                        "raw_job": job,
                    },
                )
            )

        print(
            f"Google Jobs found: "
            f"{len(results)}"
        )

        return results