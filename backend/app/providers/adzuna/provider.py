from datetime import datetime

import httpx

from app.core.config import settings
from app.providers.base import JobSearchProvider
from app.schemas.job import JobResult, JobSearchFilters


class AdzunaProvider(JobSearchProvider):

    name = "adzuna"
    provider_type = "job_api"

    BASE_URL = "https://api.adzuna.com/v1/api"

    async def search(
        self,
        query: str,
        location: str | None = None,
        filters: JobSearchFilters | None = None,
    ) -> list[JobResult]:

        country = settings.ADZUNA_COUNTRY

        url = (
            f"{self.BASE_URL}/jobs/"
            f"{country}/search/1"
        )

        params = {
            "app_id": settings.ADZUNA_APP_ID,
            "app_key": settings.ADZUNA_APP_KEY,
            "results_per_page": 20,
            "what": query,
            "content-type": "application/json",
        }

        if location:
            params["where"] = location

        if filters:

            if filters.job_type == "full-time":
                params["full_time"] = 1

            if filters.job_type == "part-time":
                params["part_time"] = 1

            if filters.job_type == "permanent":
                params["permanent"] = 1

        try:

            async with httpx.AsyncClient(
                timeout=15.0
            ) as client:

                response = await client.get(
                    url,
                    params=params,
                )

                response.raise_for_status()

                data = response.json()

        except httpx.TimeoutException:
            raise RuntimeError(
                "Adzuna API request timed out."
            )

        except httpx.HTTPStatusError as exc:
            raise RuntimeError(
                f"Adzuna API returned "
                f"HTTP {exc.response.status_code}."
            )

        except httpx.RequestError as exc:
            raise RuntimeError(
                f"Could not connect to Adzuna: {exc}"
            )

        jobs = []

        for item in data.get("results", []):

            job = self._normalize_job(item)

            if job:
                jobs.append(job)

        return jobs

    def _normalize_job(
        self,
        item: dict,
    ) -> JobResult | None:

        title = item.get("title")

        redirect_url = item.get(
            "redirect_url"
        )

        if not title or not redirect_url:
            return None

        company_data = item.get(
            "company"
        ) or {}

        location_data = item.get(
            "location"
        ) or {}

        company = company_data.get(
            "display_name"
        )

        location = location_data.get(
            "display_name"
        )

        posted_at = self._parse_date(
            item.get("created")
        )

        contract_type = item.get(
            "contract_type"
        )

        contract_time = item.get(
            "contract_time"
        )

        return JobResult(
            source=self.name,

            external_id=str(
                item.get("id")
            ) if item.get("id") else None,

            title=title,

            company=company,

            location=location,

            description=item.get(
                "description"
            ),

            job_url=redirect_url,

            apply_url=redirect_url,

            posted_at=posted_at,

            employment_type=contract_type,

            work_mode=None,

            salary_min=item.get(
                "salary_min"
            ),

            salary_max=item.get(
                "salary_max"
            ),

            currency=None,

            source_metadata={
                "contract_type": contract_type,
                "contract_time": contract_time,
                "category": item.get(
                    "category"
                ),
                "salary_is_predicted": item.get(
                    "salary_is_predicted"
                ),
            },
        )

    @staticmethod
    def _parse_date(
        value: str | None,
    ) -> datetime | None:

        if not value:
            return None

        try:
            return datetime.fromisoformat(
                value.replace(
                    "Z",
                    "+00:00"
                )
            )

        except ValueError:
            return None