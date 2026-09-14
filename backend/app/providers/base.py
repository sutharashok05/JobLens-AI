from abc import ABC, abstractmethod

from app.schemas.job import JobResult, JobSearchFilters


class JobSearchProvider(ABC):
    """
    Base interface for every job discovery provider.
    """

    name: str
    provider_type: str

    @abstractmethod
    async def search(
        self,
        query: str,
        location: str | None = None,
        filters: JobSearchFilters | None = None,
    ) -> list[JobResult]:
        """
        Search jobs using this provider.
        """
        raise NotImplementedError