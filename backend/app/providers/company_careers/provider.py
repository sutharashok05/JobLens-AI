from app.providers.base import JobSearchProvider
from app.schemas.job import JobResult, JobSearchFilters


class CompanyCareerProvider(JobSearchProvider):
    name = "company_careers"
    provider_type = "company_careers"

    async def search(
        self,
        query: str,
        location: str | None = None,
        filters: JobSearchFilters | None = None,
    ) -> list[JobResult]:

        # Company career-page discovery will be added later.
        return []