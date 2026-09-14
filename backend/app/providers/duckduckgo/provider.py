from app.providers.base import JobSearchProvider
from app.schemas.job import JobResult, JobSearchFilters


class DuckDuckGoProvider(JobSearchProvider):
    name = "duckduckgo"
    provider_type = "web_search"

    async def search(
        self,
        query: str,
        location: str | None = None,
        filters: JobSearchFilters | None = None,
    ) -> list[JobResult]:

        # Real implementation will be added later.
        return []